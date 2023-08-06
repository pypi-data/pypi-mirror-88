from django.core.serializers.json import Serializer as JSONSerializer


class Serializer(JSONSerializer):
    def start_object(self, obj):
        return super(Serializer, self).start_object(obj)

    def end_object(self, obj):
        return super(Serializer, self).end_object(obj)

    def get_dump_object(self, obj):
        dump_object = super(Serializer, self).get_dump_object(obj)

        # Get object id
        try:
            object_id = str(obj.natural_key())
        except AttributeError:
            object_id = obj.pk

        dump_object_id = '{}:{}'.format(dump_object['model'], object_id)
        dump_object['_id'] = dump_object_id

        return dump_object
