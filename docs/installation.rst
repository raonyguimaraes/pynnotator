Installation
############

Installation using Docker and Docker-Compose
********************************************

    sudo apt install docker.io docker-compose
    sudo usermod -aG docker $(whoami)
    exec sudo su ${USER}
    docker-compose build
    docker-compose run pynnotator -i sample.vcf

Installation without Docker
***************************

    sudo apt-get install -y software-properties-common python3 python3-dev python3-pip
    pip3 install pynnotator
    pynnotator install

