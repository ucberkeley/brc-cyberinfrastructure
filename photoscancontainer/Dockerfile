# docker build --rm --tag photoscan13 .

##
## Dockerfile for photoscan13
##

## Built using Ubuntu 16.04 LTS (xenial) since that is one of the
## targets available in PPA and is a Long Term Support (LTS)
## https://wiki.ubuntu.com/Releases

FROM ubuntu:xenial

RUN apt-get update && \
    apt-get install -y software-properties-common libglib2.0 libqt5gui5 libglu1-mesa libgomp1 zlib1g wget vim && \
    apt-get update

## install Agisoft Photoscan 1.3
RUN wget --directory-prefix=/usr/local http://download.agisoft.com/photoscan-pro_1_3_0_amd64.tar.gz ;\
(cd /usr/local && tar zxvf photoscan-pro_1_3_0_amd64.tar.gz) ;\
(cd /usr/local/bin && ln -s ../photoscan-pro/photoscan-pro.sh) ;\
rm -f /usr/local/photoscan-pro_1_3_0_amd64.tar.gz

ENTRYPOINT ["photoscan13"]
CMD ["-h"]
