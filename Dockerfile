############################################################
# Dockerfile to build Pynnotator
# Based on Ubuntu LTS
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Raony Guimaraes

# Update the repository sources list

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y software-properties-common python3 python3-dev python3-pip \
    python3-setuptools vcftools bcftools tabix zlib1g-dev libpq-dev build-essential \
    zlib1g-dev libbz2-dev liblocal-lib-perl cpanminus curl unzip wget sudo git gcc \
    wget make zip htop vim liblzma-dev screen less perl unzip libcurl4-openssl-dev && \
    add-apt-repository ppa:webupd8team/java -y && \
    apt-get update && \
    echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections && \
    apt-get install -y oracle-java8-installer && \
    apt-get clean

################## BEGIN INSTALLATION ######################
# Create the default software directory

#RUN pip3 install pynnotator
#RUN pynnotator install
RUN git clone http://github.com/raonyguimaraes/pynnotator
WORKDIR /pynnotator
RUN python3 setup.py install

RUN pynnotator install

ENTRYPOINT ["pynnotator"]