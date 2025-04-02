from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, BinaryIO

from .Header.request_header import RequestHeader
from ..utils.logger import get_logger

@dataclass
class AbstractRequest(ABC):
    header: RequestHeader
    
    def __post_init__(self):
        self._logger = get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        self._logger.debug(f"Created {self.__class__.__name__} with header correlation ID: {self.header.correlation_id}")

    @classmethod
    @abstractmethod
    def decode_body(cls, request_buffer : BinaryIO):
        logger = get_logger(f"{cls.__module__}.{cls.__name__}")
        logger.debug(f"Decoding request body for {cls.__name__}")
        return NotImplementedError