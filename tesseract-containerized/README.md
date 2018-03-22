# Example of building a Docker container for Tesseract4 and convert it to a Singularity container


Build a Tesseract container, push it to Dockerhub, and convert it 
to run as a Singularity container on Jetstream, Savio, or anyehwere
else that you have the Singularity container runtime installed.

```bash
git clone https://github.com/mauricemanning/tesseract-containerized
cd tesseract-containerized
docker build --rm --tag tesseract .
docker tag tesseract:latest mauricemanning/tesseract:latest
docker push mauricemanning/tesseract:latest
docker images
sudo singularity create --size 375 tesseract.img
sudo singularity import tesseract.img docker://mauricemanning/tesseract:latest
singularity exec tesseract.img tesseract -v
```
