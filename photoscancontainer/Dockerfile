# docker build --rm --tag photoscan .

##
## Dockerfile for caiman
##

## Built using Ubuntu 16.04 LTS (xenial) since that is one of the
## targets available in PPA and is a Long Term Support (LTS)
## https://wiki.ubuntu.com/Releases

FROM ubuntu:xenial

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get update
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing && apt-get install -y gcc libgl1-mesa-dev libgeos-dev libglu1-mesa-dev libgtk2.0-0 wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 vim \
    git mercurial subversion

RUN /bin/bash -c 'mkdir /scratch/'
RUN /bin/bash -c 'mkdir /global/'

ENV PATH /opt/photoscan-pro:$PATH

ENV SHELL=/bin/bash
