# Standard library imports
from abc import abstractmethod, ABCMeta
from typing import List, Dict


class TubeInterface(metaclass=ABCMeta):
    def __init__(self, succeeding=None):
        self._succeeding = succeeding

    @abstractmethod
    def handle(self, data: Dict[str, str]) -> bool:
        raise NotImplementedError("handle method is not implemented!")


class ServiceInterface(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, data: Dict[str, str], context) -> bool:
        raise NotImplementedError("execute method is not implemented!")
