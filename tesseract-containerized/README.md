# Build a Docker container for Tesseract4 and convert it to a Singularity container


Build a Tesseract container, push it to Dockerhub, and convert it 
to run as a Singularity container on Jetstream, Savio, or anyehwere
else that you have the Singularity container runtime installed.

```bash
$ git clone https://github.com/ucberkeley/brc-cyberinfrastructure
$ cd brc-cyberinfrastructure/tesseract-containerized
$ docker build --rm --tag tesseract .
$ docker tag tesseract:latest ucbrit/tesseract:latest
$ docker push ucbrit/tesseract:latest
$ singularity pull docker://ucbrit/tesseract:latest
```

To test, shell into the Singularity container and check that Tesseract is running in the container:

```bash
$ singularity shell tesseract-lastest.simg
Singularity: Invoking an interactive shell within container...
[...] > tesseract --version
tesseract 4.0.0.beta.1
[...]
```

As of 08 August 2018, these instructions have been tested using Singularity version 2.6.0.
