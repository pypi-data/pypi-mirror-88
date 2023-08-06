from dataclasses import dataclass, field
from typing import List, Optional, Set

from robinhood_commons.strategy.investment_strategy import InvestmentStrategy
from robinhood_commons.util.currency_utils import num_to_currency

from robinhood_commons.entity.investor_stats import Stats
from robinhood_commons.entity.lot import Lot
from robinhood_commons.util.num_utils import float_to_percentage_str


@dataclass
class Investor:
    name: str
    investment_strategy: InvestmentStrategy
    holdings: List[Lot]
    stats: Stats
    available_funds: float = 0
    cash_percentage: float = 0
    realized_profit_loss: float = 0.00
    default_stocks: Set[str] = field(default_factory=set)
    tracking_stocks: Set[str] = field(default_factory=set)

    def change_strategy(self, new_investment_strategy: InvestmentStrategy) -> None:
        print(f"{self.name} is changing strategy from {self.investment_strategy} to {new_investment_strategy}")
        self.investment_strategy = new_investment_strategy

    def summary(self) -> str:
        return ', '.join(self.summary_cols())

    def summary_cols(self, prefix: Optional[bool] = True) -> List[str]:
        cols = [self.name, num_to_currency(value=self.stats.starting_funds),
                num_to_currency(value=self.available_funds), num_to_currency(value=self.realized_profit_loss),
                float_to_percentage_str(self.cash_percentage * 100),
                num_to_currency(value=self.stats.starting_funds * self.cash_percentage),
                '-'.join([f"{lot.symbol}{lot.shares}" for lot in self.holdings])]

        if not prefix:
            return cols

        return [cols[0], f'S: {cols[1]}', f'A: {cols[2]}', f'RPL: {cols[3]}', f'CH: {cols[4]}', f'Reserve: {cols[5]}',
                f'HS: {cols[6]}']

    @staticmethod
    def summary_header() -> List[str]:
        return ['Name', 'Starting Funds', 'Available Funds', 'Profit/Loss', 'Cash Holding %', 'Cash Holding',
                'Holdings']


if __name__ == '__main__':
    investment_strategy = InvestmentStrategy()

    investor = Investor(name='Matt', available_funds=10000, realized_profit_loss=0.00,
                        investment_strategy=investment_strategy,
                        cash_percentage=0.00, holdings=[], stats=Stats(),
                        default_stocks=set(), tracking_stocks=set())
    print(investor.summary())
    investor.change_strategy(investment_strategy)
    print(investor.summary())

    investor = Investor(name='Marnie', available_funds=40000, realized_profit_loss=0.00,
                        investment_strategy=investment_strategy,
                        cash_percentage=0.00, holdings=[], stats=Stats(),
                        default_stocks=set(), tracking_stocks=set())
    print(investor.summary())
