from typing import Dict

from robinhood_commons.entity.auth_info import AuthInfo
from robinhood_commons.util.aws_utils import AwsUtils
from robinhood_commons.util.secret_utils import SecretUtils

AUTH_KEY_SUFFIX: str = '-auth'


def get_auth_key(username: str) -> str:
    return f'{username}{AUTH_KEY_SUFFIX}'


def get_auth_info(username: str) -> AuthInfo:
    return AuthInfo(**SecretUtils.get_secret(client=AwsUtils.get_client(),
                                             secret_name=get_auth_key(username=username)))


def auth_dict(sender: str) -> Dict[str, str]:
    username = sender.split('@')[0]
    auth_info: AuthInfo = get_auth_info(username=username)
    return {"email_address": sender,
            "google_client_id": auth_info.client_id,
            "google_client_secret": auth_info.secret,
            "google_refresh_token": auth_info.refresh_token}

