# Example of building a Docker container for Tesseract4 and convert it to a Singularity container


Build a Tesseract container, push it to Dockerhub, and convert it 
to run as a Singularity container on Jetstream, Savio, or anyehwere
else that you have the Singularity container runtime installed.

```bash
git clone https://github.com/ucberkeley/brc-cyberinfrastructure/tesseract-containerized
cd tesseract-containerized
docker build --rm --tag tesseract .
docker tag tesseract:latest mmmanning/tesseract:latest
docker push mmmanning/tesseract:latest
singularity pull docker://mmmanning/tesseract:latest
```
