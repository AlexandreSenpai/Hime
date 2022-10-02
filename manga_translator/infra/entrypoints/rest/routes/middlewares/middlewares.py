import functools
from typing import Callable

from flask import request

from src.utils.error import ApiError
from src.app import log

def capture_json_middleware(function: Callable):
    """This middleware validates the request body against the GeneratePDFSchema and
    creates an "request.data" property with inputed validated data.
    """
    @functools.wraps(function)
    async def wrapper(*args, **kwargs):
        try:
            request.data = request.get_json(force=True)
            return await function(*args, **kwargs)
        except Exception as err:
            if isinstance(err, ApiError):
                log.error(f'{err.message}')
                err.status_code = 200
                raise err
            else:
                log.error(f'Error parsing json structure\nbody: {request.json}\nstack: {err}')
                raise ApiError.bad_request(message='Invalid JSON body', status_code=200, stack=str(err))
    return wrapper