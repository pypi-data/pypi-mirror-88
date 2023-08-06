from dataclasses import dataclass


@dataclass(frozen=True)
class Stock:
    symbol: str
    company_name: str


def main() -> None:
    print([Stock(**{'symbol': 'AAPL', 'company_name': 'Apple Inc.'}),
           Stock(**{'symbol': 'WMS', 'company_name': 'Advanced Drainage Systems Inc.'})])


if __name__ == "__main__":
    main()
