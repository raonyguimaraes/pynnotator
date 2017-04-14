############################################################
# Dockerfile to build Pynnotator
# Based on Ubuntu LTS
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Raony Guimaraes

# Update the repository sources list
WORKDIR /pynnotator/

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git python3 python3-dev python3-pip && \
    apt-get clean

################## BEGIN INSTALLATION ######################
# Create the default software directory

RUN pip3 install pynnotator
RUN pynnotator install

ENTRYPOINT ["pynnotator"]