import functools
from typing import Callable
import ast

from flask import request
import requests

from src.app import log
from src.utils.error import ApiError

def sns_subscription_confirmation(function: Callable):
    """This middleware validates the request body against the GeneratePDFSchema and
    creates an "request.data" property with inputed validated data.
    """
    @functools.wraps(function)
    async def wrapper(*args, **kwargs):
        payload = request.data
        try:
            if payload.get('Type') == 'SubscriptionConfirmation':
                url = payload.get('SubscribeURL')
                confirmationRequest = requests.get(url)
                if confirmationRequest.status_code == 200:
                    return await function(*args, **kwargs)
                else:
                    log.error(f'Subscription confirmation from url {url} has failed with status code {confirmationRequest.status_code}')
                    raise ApiError.internal_server_error(message='Subscription confirmation failed', stack=confirmationRequest)
            else:
                return await function(*args, **kwargs)
        except Exception as err:
            if isinstance(err, ApiError):
                log.error(f'{err.message}')
                err.status_code = 200
                raise err
            else:
                raise ApiError.internal_server_error(message='Something went wrong while trying to confirm the subscription', stack=err)
    return wrapper

def sns_body_handler(function: Callable):
    @functools.wraps(function)
    async def wrapper(*args, **kwargs):
        try:
            request.data = ast.literal_eval(request.data.get('Message').strip())
            return await function(*args, **kwargs)
        except Exception as err:
            if isinstance(err, ApiError):
                log.error(f'{err.message}')
                err.status_code = 200
                raise err
            else:
                log.error(f'Error parsing sns message\nbody: {request.json}\nstack: {err}')
                raise ApiError.bad_request(message='Invalid JSON body', status_code=200, stack=str(err))
    return wrapper