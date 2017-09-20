from fabric.api import local


def build():
    local('python setup.py install')
    local('pynnotator build')


def install():
    local('python setup.py install')
    local('pynnotator install')


def pack_data():
    local('cd pynnotator;tar -czvf pynnotator-data.latest.tar.gz data')
    local('gsutil cp pynnotator-data.latest.tar.gz gs://mendelmd/')


def pack_libs():
    local('cd pynnotator;tar -czvf pynnotator-libs.latest.tar.gz libs')
    local('gsutil cp pynnotator-libs.latest.tar.gz gs://mendelmd/')


def publish():
    # local('python setup.py sdist')
    local('python setup.py build sdist upload')
