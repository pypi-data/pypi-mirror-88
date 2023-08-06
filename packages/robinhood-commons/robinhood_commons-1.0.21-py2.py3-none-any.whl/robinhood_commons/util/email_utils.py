from typing import List

import yagmail

from util.constants import MAIN_EMAIL


def send_email(subject: str, contents: str, attachments: List[str], to: str = MAIN_EMAIL) -> None:
    yag = yagmail.SMTP()

    yag.send(to=to, subject=subject, contents=contents, attachments=attachments)


if __name__ == '__main__':
    send_email(subject='Test Email', contents='Test content', attachments=[])
