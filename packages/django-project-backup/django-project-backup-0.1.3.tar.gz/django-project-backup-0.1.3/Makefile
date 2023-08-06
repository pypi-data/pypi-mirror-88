DOCKER=docker
DPATH=${CURDIR}
IMAGE_NAME="django-project-backup"
VERSION=$(shell python setup.py --version | sed 's/\.post.*//' | sed 's/\+g.*//')

export DPATH
.PHONY:	clean build publish

clean:
	rm -rf ./dist/*
	rm -rf ./build/*
	rm -rf  ./src/django_project_backup.egg-info
	find ./src -name *.pyc -exec rm {} \;

build-release: clean
	python setup.py sdist bdist_wheel

publish:
	twine upload dist/* --verbose

