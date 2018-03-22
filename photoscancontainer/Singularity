Bootstrap:docker
From:mmmanning/photoscan:latest

%environment
SHELL=/bin/bash
PATH=/opt/photoscan-pro:$PATH
SINGULARITY_SHELL="/bin/bash --norc"

%post
export SHELL PATH SINGULARITY_SHELL 

exec mkdir /opt/photoscan-pro
exec mkdir /scratch/
