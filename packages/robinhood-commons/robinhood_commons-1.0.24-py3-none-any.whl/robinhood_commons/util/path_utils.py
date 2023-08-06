BASE_PATH: str = '/robinhood_data'


def get_output_dir(base_path: str = BASE_PATH) -> str:
    return f'{base_path}/output'


def get_log_dir(base_path: str = BASE_PATH) -> str:
    return f'{get_output_dir(base_path=base_path)}/logs'


def get_tmp_dir(base_path: str = BASE_PATH) -> str:
    return f'{get_output_dir(base_path=base_path)}/tmp'


def stocks_file_path(base_path: str = BASE_PATH) -> str:
    return f'{get_tmp_dir(base_path=base_path)}/stocks.json'

