#start from ubuntu 18.04 LTS
FROM ubuntu:bionic
#Arg is build time envrioment variable, that wont persist inside the docker
#its just here for the build process
ARG DEBIAN_FRONTEND=noninteractive

#setting up locale for smother installing and les errors
# from https://hub.docker.com/_/ubuntu/
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

#installing python and seting as default version
RUN apt-get update && apt-get install python3.7 python3-pip python3-psycopg2 -y
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

#voice support
RUN apt-get update && apt-get install libffi-dev python3.6-dev -y
#installing default reqs
COPY kingfisher/requirements.txt /tmp/
RUN python -m pip install -r /tmp/requirements.txt

#setting default work directory
RUN mkdir -p /workspace/kingfisher
COPY ./kingfisher /workspace/kingfisher
WORKDIR /workspace/kingfisher

CMD ["python", "kingfisher.py"]
