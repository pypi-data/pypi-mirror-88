import os

from robinhood_commons.util.io_utils import ensure_exists

MAIN_EMAIL: str = 'mhowell234@gmail.com'
USERS_KEY: str = 'users'
DEFAULT_DELIMITER: str = ':'

TESTING: bool = True
DEBUG: bool = False
F_IT_MODE: bool = False
PROFILE_INFO: bool = False
BUY_ONE_SELL_ONE_MODE: bool = True

RANDOM_INVESTORS: int = 7
ERROR_SLEEP_TIME: int = 30  # in seconds


def get_base_dir(name: str = 'daytrader', base_dir: str = '/code/robinhood', append_user_base: bool = True) -> str:
    base: str = os.path.expanduser(f'~{base_dir}') if append_user_base else base_dir
    base_dir: str = f'{base}-{name}'

    ensure_exists(file_path=base_dir)
    return base_dir


OUTPUT_DIR: str = f'{get_base_dir()}/output'
LOG_DIR: str = f'{OUTPUT_DIR}/logs'
TMP_DIR: str = f'{get_base_dir()}/tmp'

STOCKS_FILE_PATH: str = f'{TMP_DIR}/stocks.json'

if __name__ == '__main__':
    print(get_base_dir())
    print(get_base_dir(base_dir='/Documents'))
    print(STOCKS_FILE_PATH)
