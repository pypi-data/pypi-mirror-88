from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict

from robinhood_commons.util.num_utils import convert_floats


@dataclass(frozen=True)
class Tick:
    above_tick: float
    below_tick: float
    cutoff_price: float


def clean_tick(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data = convert_floats(data, ['above_tick', 'below_tick', 'cutoff_price'])

    return data


def main() -> None:
    tick = Tick(**clean_tick({'above_tick': '1.0', 'below_tick': '0.5', 'cutoff_price': '44.5'}))
    print(tick)


if __name__ == '__main__':
    main()
