FROM ziedguesmi/opencv-raspbian:1.0

LABEL maintainer="Zied Guesmi <guesmy.zied@gmail.com>"
LABEL version="1.0"

RUN [ "cross-build-start" ]

RUN apt-get update && apt-get install -y --no-install-recommends \
        libgtk2.0-dev \
        python3 \
        python3-pip \
        python3-setuptools \
        && \
    pip3 install --no-cache-dir PyYAML yamlordereddictloader && \
    apt-get remove -y python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /iexec

RUN [ "cross-build-end" ]

WORKDIR /object-detector

COPY ./app /object-detector

ENTRYPOINT [ "/object-detector/entrypoint" ]