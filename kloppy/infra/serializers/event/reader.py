from abc import ABC, abstractmethod
from typing import Any, Dict

from kloppy.utils import Readable


class Reader(ABC):
    @abstractmethod
    def read(self, inputs: Dict[str, Readable]) -> Any:
        raise NotImplementedError
