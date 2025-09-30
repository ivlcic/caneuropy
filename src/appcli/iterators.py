from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional, Callable, Iterator, Union, List, Dict, Any

from .date_time import to_datetime


@dataclass
class State:
    progress: float
    control: "MutableControl"


@dataclass
class DateTimeState(State):
    current: datetime
    start: datetime
    end: datetime
    step_start: datetime
    step_end: datetime


@dataclass
class RuntimeData:
    num_items_per_file: int = 10000
    file_num: int = 0
    items: List[Dict[str, Any]] = field(default_factory=list)


class MutableControl:
    def __init__(self):
        self.stop = False


class DateTimeIterator(Iterator[DateTimeState]):
    def __init__(
        self,
        start: Union[str, date, datetime],
        end: Union[str, date, datetime],
        step: timedelta = timedelta(hours=1),
        callback: Optional[Callable[[DateTimeState], None]] = None,
        **kwargs
    ):
        self.start = to_datetime(start)
        self.end = to_datetime(end)
        self.step = step
        self.callback = callback
        self._current = self.start
        self._total = (self.end - self.start).total_seconds()
        self._control = MutableControl()
        self._dynamic_args = kwargs

    def __iter__(self) -> "DateTimeIterator":
        self._current = self.start
        self._control = MutableControl()
        return self

    def __next__(self) -> DateTimeState:
        if self._current > self.end or self._control.stop:
            raise StopIteration
        step_start = self._current
        step_end = min(self._current + self.step, self.end)
        progress = ((self._current - self.start).total_seconds() / self._total) if self._total > 0 else 1.0
        state = DateTimeState(
            progress=progress,
            current=self._current,
            start=self.start,
            end=self.end,
            step_start=step_start,
            step_end=step_end,
            control=self._control
        )
        # Attach dynamic attributes if desired
        for k, v in self._dynamic_args.items():
            setattr(state, k, v)
        if self.callback:
            self.callback(state)
        self._current += self.step
        return state
