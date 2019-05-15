FROM ubuntu:18.04


RUN apt-get update && apt-get install -y --no-install-recommends \
        libgtk2.0-dev \
        python3 \
        python3-pip \
        python3-setuptools \
        && \
    pip3 install opencv-python --no-cache-dir && \
    apt-get remove -y python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /iexec_in /iexec_out

COPY object_detector.py /object_detector.py

ENTRYPOINT [ "python3", "/object_detector.py" ]