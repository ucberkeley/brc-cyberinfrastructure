#!/bin/bash

docker run -d -p 5000:5000 --name registry registry:2 # Start your local registry
docker login nvcr.io # Log in with your NVIDIA NGC account token (ngc.nvidia.com)
docker pull nvcr.io/nvidia/tensorflow:18.02-py3 # Pull the container
docker tag nvcr.io/nvidia/tensorflow:18.02-py3 localhost:5000/tensorflow
docker push localhost:5000/tensorflow # Push the container to your local registry

# Build the Singularity container
sudo SINGULARITY_NOHTTPS=true singularity build tensorflow-gpu-savio.simg TensorFlowGPU_savio

# Run the Singularity container (probably after moving it to the cluster)
singularity run --nv tensorflow-gpu-savio.simg $YOUR_PYTHON_SCRIPT
