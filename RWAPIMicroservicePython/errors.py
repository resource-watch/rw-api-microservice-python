"""ERRORS"""


class Error(Exception):

    def __init__(self, message):
        self.message = message

    @property
    def serialize(self):
        return {
            'message': self.message
        }


class NotFound(Error):
    pass


class ApiKeyError(Error):
    pass


class ValidationError(Error):

    def __init__(self, message, code):
        super().__init__(message)
        self.code = code
