import json


class HTTPException(Exception):
    message: str
    code: int

    def __init__(self, msg=None):
        if msg:
            self.msg = msg

    def with_traceback(self, tb) -> BaseException:
        return True

    def pack(self):
        return dict(error=self.message, msg=getattr(self, 'msg', '')), self.code

    def __str__(self):
        return self.message

    def __dict__(self):
        return self.pack()


class HTTPClientError(HTTPException):
    pass


class HTTPNotAcceptable(HTTPException):
    code = 406
    message = 'This request is not acceptable'


class HTTPNotProcessable(HTTPException):
    code = 422
    message = 'Request cannot be processed.'


class HTTPNotFound(HTTPException):
    code = 404
    message = 'Resource does not exist'


class HTTPConflict(HTTPException):
    code = 409
    message = 'A resource with this ID already exists'


class HTTPForbidden(HTTPException):
    code = 403
    message = 'You have insufficient permissions to access this resource.'


class HTTPDenied(HTTPException):
    code = 401
    message = 'Access to this resource is denied.'


class HTTPBadRequest(HTTPException):
    code = 400
    message = 'This request can not be fulfilled.'
