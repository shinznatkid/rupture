from fabric.api import local


def upload():
    local('python setup.py sdist bdist_wheel --universal upload')
