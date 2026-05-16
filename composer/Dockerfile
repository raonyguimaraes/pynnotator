FROM ubuntu:jammy

LABEL maintainer="Raony Guimaraes"

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        python3 python3-dev python3-pip python3-venv \
        build-essential gcc git make \
        zlib1g-dev libbz2-dev liblzma-dev libssl-dev libcurl4-openssl-dev \
        bcftools tabix htslib \
        curl wget unzip \
        perl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /pynnotator
WORKDIR /pynnotator

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -e .[export]

VOLUME ["/pynnotator/pynnotator/data", "/pynnotator/pynnotator/libs"]

ENTRYPOINT ["pynnotator"]
