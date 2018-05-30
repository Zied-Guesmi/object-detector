FROM ubuntu:16.04

LABEL maintainer="Zied Guesmi <guesmy.zied@gmail.com>"
LABEL version="1.0"

RUN apt-get update && apt-get install -y --no-install-recommends \
        # libsm6 \
        libgtk2.0-dev \
        python3 \
        python3-pip \
        python3-setuptools \
        && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir /iexec

COPY ./app /object-detector

WORKDIR /object-detector

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/object-detector/docker-start" ]