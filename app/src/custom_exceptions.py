import sys


messages = {
    # app errors
    'AppConfigNotFound': 'can not load app config file - {}',
    'IllegalAppConfigFormat': 'can not parse app config file\n{}',
    'InputConfigNotFoundWarning': 'can not load input config file - {} \n defaulting to confidence = 0.2 (20%)',
    'IllegalInputConfigFormat': 'can not parse input config file - required format is "confidence:<number>"\n{}',
    'FileTypeNotSupported': 'File type not supported - {}',
    'FileNotFound': 'File not found - {}',
    # object detection errors
    'CantLoadModel': 'can not load network model',
    'CantLoadImage': 'can not load image to network',
    'DnnNetwork': 'can not forward image throw network',
    'CantGetClassIndex': 'can not get class index',
    'CantGetObjCoordinates': 'can not get object coordinates',
    'CantAddLabelToImage': 'cannot add box & label to image',
    'CantSaveOutputImage': 'cannnot save output image',
    'CantDetectObjects': '',
    'CantCreateConsensusFile': 'can not create consensus file - {}\n{}',
}

class Warning(Exception):

    def __init__(self, message):
        print('[Warning] ' + message)


class Error(Exception):

    def __init__(self, message):
        print('[Error] ' + message)


class Fatal(Exception):

    def __init__(self, message):
        sys.exit('[FATAL] ' + message)


class InputConfigNotFoundWarning(Warning):

    message = 

    def __init__(self, filename):
        super().__init__(self.message.format(filename))


class AppConfigNotFoundError(Fatal):

    message = ''

    def __init__(self, filename):
        super().__init__(self.message.format(filename))


class IllegalAppConfigFormatError(Fatal):

    message = ''

    def __init__(self, err):
        super().__init__(self.message.format(err))


class IllegalInputConfigFormatError(Fatal):

    message = ''

    def __init__(self, err):
        super().__init__(self.message.format(err))


# class FileNotFoundError(Error):

#     message = ''

#     def __init__(self, filename):
#         super().__init__(self.message.format(filename))


class FileTypeNotSupportedError(Error):

    message = ''

    def __init__(self, filename):
        super().__init__(self.message.format(filename))


CantLoadModelError
CantLoadImageError
DnnNetworkError
CantGetClassIndexError
CantGetObjCoordinatesError
CantAddLabelToImageError


class CanNotDetectObjectsError(Error):

    message = 'can not extracte text from image - {}\n{}'

    def __init__(self, err, filename):
        super().__init__(self.message.format(filename, err))


class CanNotCreateConsensusFile(Fatal):

    message = ''

    def __init__(self, err, filename):
        super().__init__(self.message.format(filename, err))