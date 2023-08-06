#!/bin/bash
#
# The simplest way is
# $ python3 setup.py sdist bdist_wheel upload -r pypiantfin

set -e

rm -fr ./dist/*
python3 setup.py sdist bdist_wheel

twine upload dist/*
command -v twine || pip3 install twine
#twine upload dist/*

# Recommend to put username and password here
# twine upload --repository-url https://pypi.antfin-inc.com/simple/ -u your-username -p your-password dist/*
