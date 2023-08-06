from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from robinhood_commons.util.date_utils import convert_dates
from robinhood_commons.util.num_utils import convert_floats

EXAMPLE: Dict[str, Any] = {'url': 'https://api.robinhood.com/portfolios/5PY78241/',
                           'account': 'https://api.robinhood.com/accounts/5PY78241/', 'start_date': '2015-01-20',
                           'market_value': '58974.7162', 'equity': '45441.9162',
                           'extended_hours_market_value': '57351.8149', 'extended_hours_equity': '45380.2749',
                           'extended_hours_portfolio_equity': '45380.2749', 'last_core_market_value': '58974.7162',
                           'last_core_equity': '45441.9162', 'last_core_portfolio_equity': '45441.9162',
                           'excess_margin': '13767.0327', 'excess_maintenance': '25338.8665',
                           'excess_margin_with_uncleared_deposits': '13767.0327',
                           'excess_maintenance_with_uncleared_deposits': '25338.8665',
                           'equity_previous_close': '45177.1802', 'portfolio_equity_previous_close': '45177.1802',
                           'adjusted_equity_previous_close': '45177.1802',
                           'adjusted_portfolio_equity_previous_close': '45177.1802', 'withdrawable_amount': '0.0000',
                           'unwithdrawable_deposits': '0.0000', 'unwithdrawable_grants': '0.0000'}


@dataclass(frozen=True)
class Portfolio:
    url: str
    account: str
    start_date: datetime
    market_value: float
    equity: float
    extended_hours_market_value: float
    extended_hours_equity: float
    extended_hours_portfolio_equity: float
    last_core_market_value: float
    last_core_equity: float
    last_core_portfolio_equity: float
    excess_margin: float
    excess_maintenance: float
    excess_margin_with_uncleared_deposits: float
    excess_maintenance_with_uncleared_deposits: float
    equity_previous_close: float
    portfolio_equity_previous_close: float
    adjusted_equity_previous_close: float
    adjusted_portfolio_equity_previous_close: float
    withdrawable_amount: float
    unwithdrawable_deposits: float
    unwithdrawable_grants: float


def clean_portfolio(input_data: Dict[str, Any]) -> Dict[str, Any]:
    data = deepcopy(input_data)

    data = convert_floats(data, ['market_value', 'equity', 'extended_hours_market_value', 'extended_hours_equity',
                                 'extended_hours_portfolio_equity', 'last_core_market_value', 'last_core_equity',
                                 'last_core_portfolio_equity', 'excess_margin', 'excess_maintenance',
                                 'excess_margin_with_uncleared_deposits', 'excess_maintenance_with_uncleared_deposits',
                                 'equity_previous_close', 'portfolio_equity_previous_close',
                                 'adjusted_equity_previous_close', 'adjusted_portfolio_equity_previous_close',
                                 'withdrawable_amount', 'unwithdrawable_deposits', 'unwithdrawable_grants'])
    data = convert_dates(data, ['start_date'])

    return data


def main() -> None:
    portfolio = Portfolio(**clean_portfolio(EXAMPLE))
    print(portfolio)


if __name__ == '__main__':
    main()
