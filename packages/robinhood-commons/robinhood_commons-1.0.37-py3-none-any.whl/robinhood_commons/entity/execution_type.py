from __future__ import annotations

from enum import Enum, auto
from typing import Optional


class ExecutionType(Enum):
    BUY = auto()
    SELL = auto()
    WAIT = auto()

    @staticmethod
    def to_enum(value: str) -> Optional[ExecutionType]:
        v: str = value.upper().replace(' ', '-').replace('-', '_')
        return ExecutionType[v]

    def value(self) -> str:
        return self.name.lower()


def main() -> None:
    print(ExecutionType.to_enum("buy"))
    print(ExecutionType.to_enum("sell"))
    print(ExecutionType.BUY.value())


if __name__ == "__main__":
    main()
