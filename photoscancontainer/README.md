# Build a Singularity container that includes Photoscan, using a Singularity recipe file

Build a Photoscan container using Singularity to run on Jetstream, Savio, or anyehwere else the Singularity container runtime is installed.

*These instructions are current as of 18 July 2018, for Photoscan v1.4.2; as of this date, the `Singularity` file in this repo folder builds this version of Photoscan. It's a good idea to include the Photoscan version used in the name the Singularity container, as in `photoscan_1_4_2.simg`, below.*

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

A simple functional test (which requires access to a license server that serves a valid Photoscan license) is included in the subdirectory "container-test" (a Python script and a set of images that the script references). Invocation of the script would look something like this (replacing, as appropriate: the /global/scratch... paths; as well as the reference to a license server on UC Berkeley's shared HPC cluster, Savio, with another license server):

```SINGULARITYENV_RLM_LICENSE=5053@lmgr0@brc.berkeley.edu singularity exec -B /global/scratch/username/photoscan/:/opt /global/scratch/username/containers/photoscan_1_4_2.simg /usr/local/photoscan-pro/photoscan.sh -r /opt/ps.py -platform offscreen
```

A successful response will look something like this:

```AddPhotos: filenames = /opt/images/coffeecup-1.jpg;/opt/images/coffeecup-2.jpg;/opt/images/coffeecup-3.jpg;/opt/images/coffeecup-4.jpg
SaveProject: chunks = 0, path = /opt/photoscan-test.psz
saved project in 0.014898 sec
```



**Note**: *These instructions supercede a previous set that involved building a Docker container and pulling it into Singularity. As of Singularity v2.4.6 and Photoscan 1.4.2, the method given here is the one that works (and is faster besides).*
