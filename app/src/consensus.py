import os
import sys
import hashlib

import custom_exceptions as customExceptions


class Consensus:

    '''
    this class creates the consensus.iexec file used to verify the PoCo (proof of contribution).
    this file contains hashes of every text file produced as output.
    '''

    _CONSENSUS_FILENAME = 'consensus.iexec'

    def __init__(self, datadir, target):
        path = '{}/{}'.format(datadir, self._CONSENSUS_FILENAME)
        self.create(consensusFilePath=path, target=target)

    def create(self, consensusFilePath, target):
        try:
            with open(consensusFilePath, 'w+') as consensus:
                consensus.write(self.hashFile(target))
        except Exception as e:
            raise customExceptions.Fatal(e + ' - ' + target)
        finally:
            consensus.close()

    def hashFile(self, path):
        md5 = hashlib.md5()
        try:
            with open(path, 'rb') as f:
                buffer = f.read()
                md5.update(buffer)
            return md5.hexdigest()
        except Exception as e:
            raise customExceptions.Fatal(e)