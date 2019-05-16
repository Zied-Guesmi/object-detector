#!/bin/sh

unzip   /iexec_in/$DATASET_FILENAME -d /iexec_in    && \
rm      /iexec_in/$DATASET_FILENAME                 && \
python3 /object_detector.py $@