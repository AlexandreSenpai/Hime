from typing import Union

from werkzeug.exceptions import HTTPException

from manga_translator.infra.entrypoints.rest.app import APP, log
from manga_translator.utils.handlers.error.api_error import ApiError

@APP.errorhandler(Exception)
def api_error(err: Union[Exception, ApiError]):
    if isinstance(err, ApiError):
        log.error(message=err.message, stack_trace=err.stack_trace)
        return err.to_dict(), err.status_code[0]
    
    if isinstance(err, HTTPException):
        log.error(message=err.description, stack_trace=None)
        return ApiError.internal_server_error(message=err.description, stack_trace=err.description).to_dict(), err.code
    
    log.error(message="Something Went Wrong", stack=str(err))
    return ApiError.internal_server_error(message="Something Went Wrong", stack=err.description).to_dict(), 500
