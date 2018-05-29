import os
import sys
import subprocess

import imghdr
import yaml
import yamlordereddictloader

from object_detector import ObjectDetector
import custom_exceptions as customExceptions
from consensus import Consensus


class Flag:

    taskStarted = '[INFO] processing file {}'
    taskEnded = '[INFO] done..\n'
    executionEnded = '[INFO] Supported images have been moved to "{}" folder.\n' \
                   + '[INFO] Text files are saved in "{}" folder.'


class App:

    _SUPPORTED_IMAGES = [ 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png' ]
    _PREFIX = 'original'
    _EXTENSION = '.txt'
    _appConfigFile = '{}/app-config.yml'
    minConfidence = 0.2

    def __init__(self):
        self._paths = {}
        self.flag = Flag()
        self.readAppConfigFile()
        try: self.readInputConfigFile()
        except customExceptions.CustomException: pass
        try: self.prepareDatadir()
        except Exception as e: raise customExceptions.Fatal(err=e)

    @property
    def datadir(self):
        return self._paths['/']

    @property
    def out(self):
        return self._paths['/out']

    def readAppConfigFile(self):
        dirname = os.path.dirname
        path = self._appConfigFile.format(dirname(dirname(os.path.realpath(__file__))))
        if not os.path.isfile(path):
            raise customExceptions.Fatal(key='AppConfigNotFound', param=path)
        try:
            yml = yaml.load(open(path), yamlordereddictloader.SafeLoader)
            self._paths['/'] = yml['datadir']
            self._paths['/in'] = '{}/{}'.format(yml['datadir'], yml['input-dir'])
            self._paths['/out'] = '{}/{}'.format(yml['datadir'], yml['output-dir'])
            self._paths['conf'] = '{}/{}'.format(yml['datadir'], yml['input-config'])
            self.flag.executionEnded = self.flag.executionEnded.format(yml['input-dir'], yml['output-dir'])
        except Exception as e:
            raise customExceptions.Fatal(err=e, key='IllegalAppConfigFormat')

    def readInputConfigFile(self):
        if not os.path.isfile(self._paths['conf']):
            raise customExceptions.Warning(key='InputConfigNotFound', param=self._paths['conf'])
        try:
            inputConfig = yaml.load(open(self._paths['conf']), yamlordereddictloader.SafeLoader)
            self.minConfidence = float(inputConfig['confidence'])
        except Exception as e:
            raise customExceptions.Fatal(err=e, key='IllegalInputConfigFormat')

    def getAbsPath(self, dirname, filename, extension=''):
        return '{}/{}{}'.format(self._paths[dirname], filename, extension)

    def isNotConfigFile(self, filename):
        return self.getAbsPath('/', filename) != self._paths['conf']

    def isSupportedImageType(self, filename):
        return ( os.path.isfile(self.getAbsPath('/', filename)) and
            self.isNotConfigFile(filename) and
            imghdr.what( self.getAbsPath('/', filename) ) in self._SUPPORTED_IMAGES )

    def prepareDatadir(self):
        datadirContent = os.listdir(self._paths['/'])
        os.mkdir(self._paths['/in'])
        os.mkdir(self._paths['/out'])
        for filename in [ f for f in datadirContent if self.isSupportedImageType(f) ]:
            subprocess.call([ 'mv', self.getAbsPath('/', filename), self._paths['/in'] ])

    def renameInputFiles(self):
        for filename in os.listdir(self._paths['/in']):
            oldPath = self.getAbsPath('/in', filename)
            newName = '{}-{}'.format(self._PREFIX, filename)
            newPath = self.getAbsPath('/in', newName)
            subprocess.call([ 'mv', oldPath, newPath ])

    def main(self):
        objectDetector = ObjectDetector()
        for imagename in os.listdir(self._paths['/in']):
            print(self.flag.taskStarted.format(imagename))
            imagepath = self.getAbsPath('/in', imagename)
            saveTo = self.getAbsPath('/out', imagename)
            try: objectDetector.run(imagepath, saveTo, self.minConfidence)
            except customExceptions.CustomException: pass
            except Exception as e: print(e)
            print(self.flag.taskEnded)
        try: self.renameInputFiles()
        except Exception as e:
            raise customExceptions.Error(err=e, key='CantRenameInputFiles')
        print(self.flag.executionEnded)


if __name__ == '__main__':
    app = App()
    app.main()
    Consensus(datadir=app.datadir, outputdir=app.out)