# Build a Photoscan container, push it to Dockerhub, and convert it to run as a Singularity container

Build a Photoscan container using Singularity to run on Jetstream, Savio, or anyehwere else the Singularity container runtime is installed.

*These instructions are current as of 26 April 2018, for Photoscan v1.4.2; as of this date, the `Singularity` file in this repo folder builds this version of Photoscan. It's a good idea to include the Photoscan version used in the name the Singularity container, as in `photoscan_1_4_2.simg`, below.

```bash
$ git clone https://github.com/ucberkeley/brc-cyberinfrastructure
$ cd brc-cyberinfrastructure/photoscancontainer
$ sudo singularity build photoscan_1_4_2.simg Singularity
```
For a simple test that Photoscan runs in the container, it is not necessary to have a license:

```bash
$ singularity exec -B /home/masover/:/opt photoscan_1_4_2.simg /usr/local/photoscan-pro/photoscan.sh --version -platform offscreen
```
The smoke-test passes if you get something like this:

```bash
Agisoft PhotoScan Professional Version: 1.4.2 build 6185 (64 bit)
Copyright (C) 2017 Agisoft LLC.
```


**Note**: *These instructions supercede a previous set that involved building a Docker container and pulling it into Singularity. As of Singularity v2.4.6 and Photoscan 1.4.2, the method given here is the one that works (and is faster besides).*
