This directory contains the definition file and instructions for using RStudio vai RStudio Server on Savio. It builds on the Rocker Dockerfile for RStudio/RStudio server, modified such that the RStudio server can start when not running as root.

## Instructions for users

To run RStudio Server on a compute node and connect via your browser here are the steps:

  1) Using either `srun` or `sbatch`, start a Savio job on one or more compute nodes. In the job script (or in the interactive session), execute one of the following (depending on whether you want RStudio to require you to enter a password)to start RStudio server:
     - `singularity run /global/scratch/paciorek/rstudio_server_0.1.img`
     - `PASSWORD=foo singularity run /global/scratch/paciorek/rstudio_server_0.1.img --auth-pam-helper-path /usr/lib/rstudio-server/bin/pam-helper --auth-none 0`

     Note the name of the Savio node, e.g, `n0070.savio2`, on which the job started.

  2) Login to the Savio visualization node, start a vncserver session, and connect to a VNC Viewer window (i.e., a remote desktop session) following [these instructions](https://research-it.berkeley.edu/services/high-performance-computing/using-brc-visualization-node-realvnc).

  3) From a terminal in the remote desktop session run the following (changing n0070.savio2 as needed):
     - `/global/scratch/kmuriki/otterbrowser http://n0070.savio2:8787`

     That should connect you to an RStudio session within a browser window. If you required authentication in step 1, you'll need to authenticate with your Savio user name and the password specified in step 1.
      
  4) When you are done with RStudio, make sure to kill your `srun` or `sbatch` session so you are not charged for time you don't need.
  

## Build notes (for Savio admins and user consultants)

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
