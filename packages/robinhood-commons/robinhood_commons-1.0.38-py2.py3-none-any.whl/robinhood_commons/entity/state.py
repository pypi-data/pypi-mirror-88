from __future__ import annotations

from enum import Enum, auto
from typing import Optional


class State(Enum):
    ACTIVE = auto()
    CANCELLED = auto()
    COMPLETED = auto()
    CONFIRMED = auto()
    FAILED = auto()
    FILLED = auto()
    PARTIALLY_FILLED = auto()
    PENDING = auto()
    QUEUED = auto()
    SUBMITTED = auto()
    UNCONFIRMED = auto()
    UNKNOWN = auto()
    ALL = auto()

    @staticmethod
    def to_enum(value: str) -> Optional[State]:
        if value is None:
            return State.UNKNOWN
        v: str = value.upper().replace(' ', '-').replace('-', '_')
        return State[v]

    def value(self) -> str:
        return self.name.lower()


def main() -> None:
    print(State.to_enum("active"))
    print(State.to_enum("cancelled"))
    print(State.ACTIVE.value())


if __name__ == "__main__":
    main()
