from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

from kloppy.domain import EventDataset
from kloppy.utils import Readable


class EventDataSerializer(ABC):
    @abstractmethod
    def _load_raw_events(
        self, inputs: Dict[str, Readable], options: Dict = None
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    def _parse_raw_events(
        self, raw_events: Any, options: Dict = None
    ) -> EventDataset:
        raise NotImplementedError

    def deserialize(
        self, inputs: Dict[str, Readable], options: Dict = None
    ) -> EventDataset:
        raw_events = self._load_raw_events(inputs, options)
        return self._parse_raw_events(raw_events, options)

    @abstractmethod
    def serialize(self, dataset: EventDataset) -> Tuple[str, str]:
        raise NotImplementedError
