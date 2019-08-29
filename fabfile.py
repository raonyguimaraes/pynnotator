from fabric.api import local


def build():
    local('python setup.py install')
    local('pynnotator build')


def install():
    local('python setup.py install')
    local('pynnotator install')


def pack_data():
    local('cd pynnotator;tar -cvf pynnotator-data.$(date +"%Y%m%d").tar data')


def pack_libs():
    local('cd pynnotator;tar -czvf pynnotator-libs.latest.tar.gz libs')


def publish():
    # local('python setup.py sdist')
    local('python setup.py sdist bdist_wheel upload')


def save():
    local('docker image save pynnotator_pynnotator -o pynnotator.tar')
def load():
    local('docker load -i pynnotator.tar')
