PYTHON=`which python3`
NAME=`python3 setup.py --name`
VERSION=`python3 setup.py --version`
SDIST=dist/$(NAME)-$(VERSION).tar.gz
VENV=/tmp/venv

dist: clean build upload

build: 
	$(PYTHON) -m build

upload:
	$(PYTHON) -m twine upload --repository pypi dist/*        

clean:
	rm -rf dist/*

test:
	unit2 discover -s tests -t .