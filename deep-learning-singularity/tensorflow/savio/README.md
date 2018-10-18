# Running GPU TensorFlow in Singularity Containers using NVIDIA's Docker containers

Since this is coming from NVIDIA instead of the normal Docker registry, we need to do a few additional steps to get it into Singularity. On your own machine, you will need to set up your own Docker registry. You need to do this on a computer on which you have `sudo` access and then transfer the final Singularity image to Savio.

```bash
docker run -d -p 5000:5000 --name registry registry:2 # Start your local registry
docker login nvcr.io # Log in with your NVIDIA NGC account token (ngc.nvidia.com)
docker pull nvcr.io/nvidia/tensorflow:18.02-py3 # Pull the container
docker tag nvcr.io/nvidia/tensorflow:18.02-py3 localhost:5000/tensorflow 
docker push localhost:5000/tensorflow # Push the container to your local registry
```

Now, the build file is very similar to the previous except we are using our own local registry. I save it as TensorflowGPU_savio.

```bash
Bootstrap: docker 
From: localhost:5000/tensorflow

%post
    mkdir -p /global/home/users
    mkdir -p /global/scratch
    touch /bin/nvidia-smi

%runscript
    python "$@"
```

```bash
sudo SINGULARITY_NOHTTPS=true singularity build tensorflow-gpu-savio.simg TensorFlowGPU_savio
```

You should now have `tensorflow-gpu-savio.simg`. Move it to Savio (sftp or scp) and then run it on a 1080ti node with:

```bash
singularity run --nv tensorflow-gpu-savio.simg $YOUR_PYTHON_FILE
```

