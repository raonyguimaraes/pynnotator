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
    apt-get install -y software-properties-common python3 python3-dev python3-pip git

################## BEGIN INSTALLATION ######################
# Create the default software directory

#RUN pip3 install pynnotator
#RUN pynnotator install
RUN git clone http://github.com/raonyguimaraes/pynnotator
WORKDIR /pynnotator
RUN python3 setup.py install
RUN pynnotator install

ENTRYPOINT ["pynnotator"]