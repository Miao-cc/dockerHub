1 pulsarENV
We had installed python environment and linux environment for puslar search
and timing.

# build pulsar base image
docker build -f Dockerfile_pulsar.env -t pulsar-env:base .

# create container
./start.py docker-compose.yml

Note:
If you want to build this image. You need to download the python module
pakages.

mkdir modulePy
pip download -d modulePy -r pythonENV.txt
