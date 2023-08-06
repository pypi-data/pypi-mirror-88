from dataclasses import dataclass
from typing import Dict

EXAMPLE: Dict[str, str] = {'email_address': '12344565@gmail.com', 'google_client_id': 'mh112233',
                           'google_client_secret': '234578', 'google_refresh_token': '7890'}


@dataclass(frozen=True)
class AuthInfo:
    email_address: str
    google_client_id: str
    google_client_secret: str
    google_refresh_token: str


def main() -> None:
    auth_info = AuthInfo(**EXAMPLE)
    print(auth_info)


if __name__ == '__main__':
    main()
