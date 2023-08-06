from __future__ import annotations

from enum import Enum, auto


class OptionType(Enum):
    CALL = auto()
    PUT = auto()

    @staticmethod
    def to_enum(value: str) -> OptionType:
        v: str = value.upper().replace(' ', '-').replace('-', '_')
        return OptionType[v]

    def value(self) -> str:
        return self.name.lower()


def main() -> None:
    print(OptionType.to_enum("call"))
    print(OptionType.to_enum("put"))
    print(OptionType.to_enum("CALL"))
    print(OptionType.CALL.value())


if __name__ == "__main__":
    main()
