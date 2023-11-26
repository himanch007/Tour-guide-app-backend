from urllib.request import Request
from fastapi.responses import JSONResponse


class HTTPError(Exception):
    '''
    Http Error exception can be extended for various Http Error status codes
    '''
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        self.response_json = {
            # 'status_code': self.status_code,
            'message': self.message
        }


async def http_error_handler(request: Request, exc: HTTPError) ->JSONResponse:
    '''
    Method to return response for http error
    '''
    return JSONResponse(
        content=exc.response_json,
        status_code=exc.status_code
    )


class Unauthorized(HTTPError):
    '''
    Exception for error 401
    '''
    def __init__(
        self, 
        message='Request is not authorized. Please log in', 
        status_code:int = 401
    ):
        super().__init__(message, status_code)


class Conflict(HTTPError):
    '''
    Exception for error 409
    '''
    def __init__(
        self, 
        message='User already exists', 
        status_code:int = 409
    ):
        super().__init__(message, status_code)


class Unprocessable(HTTPError):
    '''
    Exception for error 422
    '''
    def __init__(
        self, 
        message='Request cannot be processed', 
        status_code:int = 422
    ):
        super().__init__(message, status_code)
