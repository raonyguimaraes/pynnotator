############################################################
# Dockerfile to build Pynnotator
# Based on Ubuntu LTS
############################################################

# Set the base image to Ubuntu
FROM ubuntu:xenial

# File Author / Maintainer
MAINTAINER Raony Guimaraes

# Update the repository sources list

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
	apt-get install -y apt-utils && \
    apt-get upgrade -y && \
    apt-get install -y make software-properties-common python3 python3-dev python3-pip libcurl4-openssl-dev sed python3-setuptools vcftools bcftools tabix zlib1g-dev liblzma-dev libpq-dev libbz2-dev build-essential zlib1g-dev liblocal-lib-perl cpanminus curl unzip wget pkg-config cython3 python-pysam sudo && \
    apt-get install -y libclass-dbi-mysql-perl libfile-copy-recursive-perl libarchive-extract-perl libarchive-zip-perl libwww-perl libcrypt-ssleay-perl libbio-perl-perl libcgi-pm-perl && \
	add-apt-repository ppa:webupd8team/java -y && \
	apt-get update && \
	echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections && \
	apt-get install -y oracle-java8-installer && \
	apt-get clean
#RUN	cpanm DBI File::Copy::Recursive Archive::Extract Archive::Zip LWP::Simple Bio::Root::Version LWP::Protocol::https Bio::DB::Fasta CGI

################## BEGIN INSTALLATION ######################
# Create the default software directory

#RUN git clone http://github.com/raonyguimaraes/pynnotator

COPY . /pynnotator
WORKDIR /pynnotator
RUN python3.5 setup.py develop
RUN pynnotator install
ENTRYPOINT ["pynnotator"]
