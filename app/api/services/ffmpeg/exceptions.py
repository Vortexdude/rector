
class BaseFFMPEGException(Exception):
    def __init__(self, message):
        super().__init__(message)


class FilenameMissingException(BaseFFMPEGException):
    pass
