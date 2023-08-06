from robinhood_commons.entity.auth_info import AuthInfo
from robinhood_commons.util.aws_utils import AwsUtils
from robinhood_commons.util.secret_utils import SecretUtils

EMAIL_NOTIFIER_KEY: str = 'email-notifier'


def get_auth_info(auth_key: str = EMAIL_NOTIFIER_KEY) -> AuthInfo:
    return AuthInfo(**SecretUtils.get_secret(client=AwsUtils.get_client(),
                                             secret_name=auth_key))
