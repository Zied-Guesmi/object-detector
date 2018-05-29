import sys


def messages(key, param=None):
    return {
        # warnings
        'InputConfigNotFound': 'can not load input config file - {} \n defaulting to confidence = 0.2 (20%)',
        # errors
        'CantLoadModel': 'can not load network model',
        'CantLoadImage': 'can not load image to network',
        'DnnNetworkError': 'can not forward image throw network',
        'CantGetClassIndex': 'can not get class index',
        'CantGetObjCoordinates': 'can not get object coordinates',
        'CantAddLabelToImage': 'can not add box & label to image',
        'CantSaveOutputImage': 'can not save output image',
        'CantDetectObjects': '',
        'CantRenameInputFiles': 'can not rename input files to avoid removing them by the sdk',
        'CantCreateConsensusFile': 'can not create consensus file - {}',
        # fatal
        'AppConfigNotFound': 'can not load app config file - {}',
        'IllegalAppConfigFormat': 'can not parse app config file',
        'IllegalInputConfigFormat': 'can not parse input config file - required format is "confidence:<number>"',
    }[key].format(param)


class CustomException(Exception):

    def __init__(self):
        pass
    
    def message(self, category, key=None, param=None):
        # print('key: ' + key)
        # print('param: ' + str(param))
        message = messages(key, param) if key is not None else ''
        return '[{}] {}'.format(category, message)

class Warning(CustomException):

    def __init__(self, err=None, key=None, param=None):
        print(super().message('WARNING', key=key, param=param))
        if err is not None: print(err)


class Error(CustomException):

    def __init__(self, err=None, key=None, param=None):
        print(super().message('ERROR', key=key, param=param))
        if err is not None: print(err)


class Fatal(CustomException):

    def __init__(self, err=None, key=None, param=None):
        print(super().message('FATAL', key=key, param=param))
        if err is not None: print(err)
        sys.exit()