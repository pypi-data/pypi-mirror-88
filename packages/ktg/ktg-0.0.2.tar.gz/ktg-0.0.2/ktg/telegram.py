# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional
import json

# Pip
from kcu import request

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------------- class: Telegram ------------------------------------------------------------ #

class Telegram:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        token: str,
        chat_id: Optional[str] = None,
        debug: bool = False
    ):
        self.token = token
        self.chat_id = chat_id
        self.debug = debug


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def send(
        self,
        message: str,
        chat_id: Optional[str] = None
    ) -> bool:
        chat_id = chat_id or self.chat_id

        if not chat_id:
            if debug:
                print('ERROR: No chat id')

            return False

        res = request.get(
            'https://api.telegram.org/bot{}/sendMessage'.format(self.token),
            params={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
        )

        return res is not None and res.status_code == 200

    @classmethod
    def send_cls(
        cls,
        token: str,
        message: str,
        chat_id: str,
        debug: bool = False
    ) -> bool:
        return cls(token, chat_id, debug).send(message)


# ---------------------------------------------------------------------------------------------------------------------------------------- #