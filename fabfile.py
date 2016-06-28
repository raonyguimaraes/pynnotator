from fabric.api import local

def build():
    local('python setup.py install')

def install():
    local('python setup.py install')
    local('pynnotator install')

def pack():
    # local('python setup.py sdist')
    local('python setup.py sdist upload')