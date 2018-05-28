FROM ubuntu:16.04

LABEL maintainer="Zied Guesmi <guesmy.zied@gmail.com>"
LABEL version="1.0"

RUN apt-get update && apt-get install -y \
    --no-install-recommends \
        libtesseract-dev \
        libsm6 \
        python3 \
        python3-pip \
        && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir /iexec

COPY ./app /object-detection

WORKDIR /object-detection

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/object-detection/docker-start" ]