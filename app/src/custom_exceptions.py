import sys


class CustomException(Exception):

    def messages(self, key, param=None):
        return {
            # Warning
            'InputConfigNotFound': 'can not load input config file - {} \n defaulting to confidence = 0.2 (20%)',
            # Error
            'CantLoadModel': 'can not load network model',
            'CantLoadImage': 'can not load image to network',
            'DnnNetworkError': 'can not forward image throw network',
            'CantGetClassIndex': 'can not get class index',
            'CantGetObjCoordinates': 'can not get object coordinates',
            'CantAddLabelToImage': 'can not add box & label to image',
            'CantSaveOutputImage': 'can not save output image',
            'CantWriteJsonFiles': 'can not write object infos to json file',
            'CantRenameInputFiles': 'can not rename input files to avoid removing them by the sdk',
            'CantCreateConsensusFile': 'can not create consensus file - {}',
            # Fatal
            'AppConfigNotFound': 'can not load app config file - {}',
            'IllegalAppConfigFormat': 'can not parse app config file',
            'IllegalInputConfigFormat': 'can not parse input config file - required format is "confidence:<number>"',
        }[key].format(param)

    def __init__(self, category, key=None, param=None):
        message = self.messages(key, param) if key is not None else ''
        print('[{}] {}'.format(category, message))


class Warning(CustomException):

    def __init__(self, err=None, key=None, param=None):
        super().__init__('WARNING', key=key, param=param)
        if err is not None: print(err)


class Error(CustomException):

    def __init__(self, err=None, key=None, param=None):
        super().__init__('ERROR', key=key, param=param)
        if err is not None: print(err)


class Fatal(CustomException):

    def __init__(self, err=None, key=None, param=None):
        super().__init__('FATAL', key=key, param=param)
        if err is not None: print(err)
        sys.exit()