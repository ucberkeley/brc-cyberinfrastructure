# Build a Photoscan container, push it to Dockerhub, and convert it to run as a Singularity container

Build a Photoscan container, push it to Dockerhub, and convert it to run as a Singularity container on Jetstream, Savio, or anyehwere else that you have the Singularity container runtime installed.

```bash
$ git clone https://github.com/ucberkeley/brc-cyberinfrastructure
$ cd brc-cyberinfrastructure/photoscancontainer
$ docker build --rm --tag photoscan .
$ docker tag photoscan:latest mmmanning/photoscan:latest
$ docker push mmmanning/photoscan:latest
$ singularity pull docker://mmmanning/photoscan:latest
```
