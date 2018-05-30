FROM ziedguesmi/opencv-raspbian:1.0

LABEL maintainer="Zied Guesmi <guesmy.zied@gmail.com>"
LABEL version="1.0"

RUN [ "cross-build-start" ]

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir /iexec

COPY ./app /object-detector

WORKDIR /object-detector

RUN pip3 install PyYAML yamlordereddictloader

RUN [ "cross-build-end" ]

ENTRYPOINT [ "/object-detector/docker-start" ]