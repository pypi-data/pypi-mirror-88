import os
import json
import ijson

import tempfile
from collections import OrderedDict

from django.apps import apps
from django.core import serializers

from .adapter import DBAdapter


class CouchdbStream:
    def __init__(self):
        self.db = DBAdapter()
        self.output = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.sent_ids = []
        self.loaded_ids = 0

    def __del__(self):
        del self.db
        os.remove(self.output.name)

    def write(self, val):
        self.output.write(bytes(val, encoding='utf-8'))

    def read(self):
        """
        with open(self.output.name, 'r') as fd:
            return json.load(fd)
        """
        with open(self.output.name, 'r') as fd:
            for i in ijson.items(fd, 'item', use_float=True):
                yield i

    def get_output_name(self):
        return self.output.name

    def send(self):
        for obj in self.read():
            # send to couchdb
            self.db.put_document(obj)
            self.sent_ids.append(obj['_id'])

    def retrieve(self):
        """
        Objects must be imported following the right order
        """
        def _clean(doc):
            d = doc['doc']
            _doc_id = d.pop('_id')
            _doc_rev = d.pop('_rev')
            return d

        _docs = self.db.get_documents()['rows']
        app_labels = set(list(map(lambda x: x['doc']['model'], _docs)))

        app_list = OrderedDict()
        for label in app_labels:
            app_label, model_label = label.split('.')
            try:
                app_config = apps.get_app_config(app_label)
            except LookupError as e:
                raise Exception(str(e))

            try:
                model = app_config.get_model(model_label)
            except LookupError:
                raise Exception("Unknown model: %s.%s" % (app_label, model_label))

            app_list_value = app_list.setdefault(app_config, [])

            # We may have previously seen a "all-models" request for
            # this app (no model qualifier was given). In this case
            # there is no need adding specific models to the list.
            if app_list_value is not None:
                if model not in app_list_value:
                    app_list_value.append(model)

        sorted_models = serializers.sort_dependencies(app_list.items())

        """
        docs = []
        for model in sorted_models:
            model_label = model._meta.label.lower()

            model_docs = list(map(lambda d: _clean(d), filter(lambda x: x['doc']['model'] == model_label, _docs)))
            model_docs.sort(key=lambda x: x['pk'], reverse=False)

            docs += model_docs
            self.loaded_ids += len(model_docs)

        with open(self.output.name, 'w') as fd:
            json.dump(docs, fd)
        """

        with open(self.output.name, 'w') as fd:
            fd.write('[')

            first_doc = True
            for model in sorted_models:
                model_label = model._meta.label.lower()

                model_docs = list(map(lambda x: _clean(x), filter(lambda x: x['doc']['model'] == model_label, _docs)))
                model_docs.sort(key=lambda x: x['pk'], reverse=False)

                # write docs sorted by id
                for doc in model_docs:
                    if first_doc:
                        first_doc = False
                    else:
                        fd.write(',')

                    fd.write(json.dumps(doc))

                self.loaded_ids += len(model_docs)

            fd.write(']')
