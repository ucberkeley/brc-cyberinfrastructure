# docker build --rm --tag tesseract .

##
## Dockerfile for tesseract
##

## With Tesseract4 installed from the unofficial Ubuntu PPA (Personal Package Archive)
## mentioned on the wiki: https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-LSTM
## See https://launchpad.net/~alex-p/+archive/ubuntu/tesseract-ocr

## Built using Ubuntu 16.04 LTS (xenial) since that is one of the
## targets available in PPA and is a Long Term Support (LTS)
## https://wiki.ubuntu.com/Releases

FROM ubuntu:xenial

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y -u ppa:alex-p/tesseract-ocr 

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y tesseract-ocr && \
    apt-get install -y tesseract-ocr-all && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["tesseract"]
CMD ["-h"]
