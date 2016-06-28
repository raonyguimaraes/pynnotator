FROM ubuntu:16.04
MAINTAINER Raony Guimarães
WORKDIR /root/annotator
RUN echo 'we are running some # of cool things'
RUN apt -y update;apt -y install python3 python3-pip sudo dialog python-setuptools