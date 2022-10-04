FROM ubuntu:focal

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update 
RUN apt-get install --no-install-recommends -y software-properties-common gpg-agent
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get install --no-install-recommends -y git python3.8 python3-pip python3-dev gcc
RUN python3.8 -m pip install covalent
RUN git clone https://github.com/AgnostiqHQ/covalent-aws-plugins
