from typing import Dict, List

import yagmail
from yagmail import SMTP

from robinhood_commons.util.constants import MAIN_EMAIL

EMAIL_ACTORS: Dict[str, SMTP] = {}


def retrive_yag(sender: str, oauth2_file: str) -> SMTP:
    if sender in EMAIL_ACTORS:
        return EMAIL_ACTORS[sender]

    new_sender: SMTP = yagmail.SMTP(user=sender, oauth2_file=oauth2_file)
    EMAIL_ACTORS[sender] = new_sender
    return new_sender


def send_email(yag: SMTP, subject: str, contents: str, attachments: List[str], to: str = MAIN_EMAIL) -> None:
    yag.send(to=to, subject=subject, contents=contents, attachments=attachments)


if __name__ == '__main__':

    sender_email: str = 'test_email@gmail.com'
    from robinhood_commons.util.random_utils import random_float
    auth_file_path: str = f'/tmp/data.{random_float(0, 100)}'

    import json
    from robinhood_commons.util.auth_utils import auth_dict
    with open(auth_file_path, 'w') as auth_file:
        auth_file.write(json.dumps(auth_dict(sender=sender_email)))

    yag_mailer = retrive_yag(sender=sender_email, oauth2_file=auth_file_path)
    send_email(yag=yag_mailer, subject='Test Email', contents='Test content', attachments=[])

    import os
    os.remove(auth_file_path)
