import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

from kloppy.domain import EventDataset
from kloppy.utils import Readable, performance_logging

logger = logging.getLogger(__name__)


class EventDataSerializer(ABC):
    def _validate_inputs(self, inputs: Dict[str, Readable]) -> None:
        pass

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
        self._validate_inputs(inputs)

        if not options:
            options = {}

        raw_events = None
        with performance_logging("load data", logger=logger):
            raw_events = self._load_raw_events(inputs, options)

        with performance_logging("load data", logger=logger):
            dataset = self._parse_raw_events(raw_events, options)

        return dataset

    @abstractmethod
    def serialize(self, dataset: EventDataset) -> Tuple[str, str]:
        raise NotImplementedError
