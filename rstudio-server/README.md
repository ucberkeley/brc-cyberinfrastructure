This directory contains the definition file and instructions for using RStudio vai RStudio Server on Savio. It builds on the Rocker Dockerfile for RStudio/RStudio server, modified such that the RStudio server can start when not running as root.

## Key things for this to work on Savio:

  1) don't use /init (that tries to write to /var); use rserver instead
  2)  make sure you have pam-helper.sh copied into container (the Rocker/rstudio dockerfile does this as long as pam-helper.sh is in the build directory (https://github.com/rocker-org/rocker-versioned/blob/master/rstudio/pam-helper.sh); that allows authentication to work by overriding usual pam authentication, which won't work on Savio: see https://github.com/nickjer/singularity-rstudio/issues/1

## Build container

```
sudo singularity build /tmp/rstudio_server_0.1.img rstudio_server_0.1.def
```

## Running RStudio Server

To run via singularity, tell the user to run one of the following via srun or sbatch and then connect to <nodename>:8787 and (if authenticating) use the user's own username and whatever password is used as below (foo in this case).

Run without authentication:
```
singularity run rstudio_server_0.1.img
```

Run with authentication:
```
PASSWORD=foo singularity run rstudio_server_0.1.img --auth-pam-helper-path /usr/lib/rstudio-server/bin/pam-helper --auth-none 0
```

Note that @paciorek can't figure out how to run as a service, using instance.start.
If I try to run with just rserver, it gives a login page, and I'm not sure why it is asking for authentication.

If I try to run with rserver --auth-pam-helper-path /usr/lib/rstudio-server/bin/pam-helper --auth-none 0, I don't know how to pass PASSWORD into instance.start.
