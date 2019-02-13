Installation
############

Installation using Docker and Docker-Compose
############################################

```
    sudo apt install docker.io docker-compose
    sudo usermod -aG docker $(whoami)
    exec sudo su ${USER}
    docker-compose build
    docker-compose run pynnotator -i sample.vcf
```


Installation on Ubuntu 18.04
############################


```
    sudo apt-get install -y software-properties-common python3 python3-dev python3-pip
    pip3 install pynnotator
    pynnotator install
```    
    

Installation on Centos 7
#########################

```
    yum -y install gcc python36-devel python36-setuptools python36-pip zlib-devel bzip2-devel xz-devel
    git clone https://github.com/raonyguimaraes/pynnotator/
    cd pynnotator
    python3.6 -m venv venv
    source venv/bin/activate
    python setup.py develop
     
```
