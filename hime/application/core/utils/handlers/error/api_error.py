from dataclasses import dataclass, asdict
from typing import Any, Dict, Union

from hime.application.core.utils.logging import logger

@dataclass()
class ApiError(Exception):
    message: str = None,
    status_code: int = None,
    payload: Dict[Union[str, int], Any] = None,
    stack_trace: Any = None

    def __init__(self, message: str, status_code: int, payload: dict = None, stack_trace: str = None):
        super().__init__()
        self.message=message,
        self.status_code=status_code,
        self.payload=payload,
        self.stack_trace=stack_trace
    
    def to_dict(self):
        return asdict(self)

    @staticmethod
    def resource_not_found(message: str, payload: dict = None, stack_trace: str = None):
        logger.error(message=message)
        return ApiError(message=message, status_code=404, payload=payload, stack_trace=stack_trace)
    
    @staticmethod
    def internal_server_error(message: str, payload: dict = None, stack_trace: str = None):
        return ApiError(message=message, status_code=500, payload=payload, stack_trace=stack_trace)
    
    @staticmethod
    def comunication_error(message: str, payload: dict = None, stack_trace: str = None):
        return ApiError(message=message, status_code=500, payload=payload, stack_trace=stack_trace)