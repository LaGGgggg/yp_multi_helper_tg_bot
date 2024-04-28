from math import ceil
from functools import cache

from requests import post

from get_logger import get_logger
from settings import (
    TTS_API_KEY,
    TTS_FOLDER_ID,
    TTS_CHARACTERS_IN_BLOCK,
    TTS_URL,
    TTS_LANGUAGE,
    TTS_VOICE,
    USER_FRIENDLY_REQUEST_ERROR_MESSAGE,
    LOGGING_REQUEST_UNKNOWN_ERROR_TEMPLATE,
    LOGGING_REQUEST_BAD_STATUS_ERROR_TEMPLATE
)


class TTS:

    def __init__(self):
        self.logger = get_logger('main')

    @staticmethod
    @cache
    def get_character_blocks(characters_amount: int) -> int:
        return ceil(characters_amount / TTS_CHARACTERS_IN_BLOCK)

    def ask(self, text: str) -> bytes | str:
        """
        Return bytes if success and string with an error message else.
        """

        try:
            response = post(
                TTS_URL,
                headers={
                    'Authorization': f'Api-Key {TTS_API_KEY}',
                },
                data={
                    'text': text,
                    'lang': TTS_LANGUAGE,
                    'voice': TTS_VOICE,
                    'folderId': TTS_FOLDER_ID,
                },
            )

        except Exception as e:

            self.logger.error(LOGGING_REQUEST_UNKNOWN_ERROR_TEMPLATE.format(service_name='TTS', error=e, context=text))

            return USER_FRIENDLY_REQUEST_ERROR_MESSAGE

        response_status_code = response.status_code

        if response_status_code != 200:

            self.logger.error(LOGGING_REQUEST_BAD_STATUS_ERROR_TEMPLATE.format(
                service_name='TTS', status_code=response_status_code, context=text
            ))

            return USER_FRIENDLY_REQUEST_ERROR_MESSAGE

        self.logger.info('TTS request success')

        return response.content


tts = TTS()
