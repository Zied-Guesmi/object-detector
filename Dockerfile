FROM ubuntu:16.04

LABEL maintainer="Zied Guesmi <guesmy.zied@gmail.com>"
LABEL version="1.0"

COPY requirements.txt /object-detector/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
        libgtk2.0-dev \
        python3 \
        python3-pip \
        python3-setuptools \
        && \
    pip3 install -r /object-detector/requirements.txt  --no-cache-dir && \
    rm /object-detector/requirements.txt && \
    apt-get remove -y python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /iexec

WORKDIR /object-detector

COPY ./app /object-detector

ENTRYPOINT [ "/object-detector/entrypoint" ]