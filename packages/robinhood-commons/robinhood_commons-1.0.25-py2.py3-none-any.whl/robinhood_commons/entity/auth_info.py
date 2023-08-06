from dataclasses import dataclass
from typing import Dict, Optional

EXAMPLE: Dict[str, str] = {'client_id': 'mh112233', 'secret': '234578', 'refresh_token': ''}


@dataclass(frozen=True)
class AuthInfo:
    client_id: str
    secret: str
    refresh_token: str


def main() -> None:
    auth_info = AuthInfo(**EXAMPLE)
    print(auth_info)


if __name__ == '__main__':
    main()
