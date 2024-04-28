from math import ceil
from functools import cache

from requests import post

from get_logger import get_logger
from settings import (
    STT_API_KEY,
    STT_FOLDER_ID,
    STT_SECONDS_IN_BLOCK,
    STT_URL,
    STT_LANGUAGE,
    USER_FRIENDLY_REQUEST_ERROR_MESSAGE,
    LOGGING_REQUEST_UNKNOWN_ERROR_TEMPLATE,
    LOGGING_REQUEST_BAD_STATUS_ERROR_TEMPLATE,
)


class STT:

    def __init__(self):
        self.logger = get_logger('main')

    @staticmethod
    @cache
    def get_second_blocks(duration: float | int) -> int:
        return ceil(duration / STT_SECONDS_IN_BLOCK)

    def ask(self, audio: bytes) -> tuple[bool, str]:
        """
        Return a bool (True if success, else False) and a string (error message or STT result).
        """

        try:
            response = post(
                STT_URL,
                headers={
                    'Authorization': f'Api-Key {STT_API_KEY}',
                },
                params={
                    'lang': STT_LANGUAGE,
                    'folderId': STT_FOLDER_ID,
                },
                data=audio,
            )

        except Exception as e:

            self.logger.error(LOGGING_REQUEST_UNKNOWN_ERROR_TEMPLATE.format(service_name='STT', error=e, context=''))

            return False, USER_FRIENDLY_REQUEST_ERROR_MESSAGE

        response_status_code = response.status_code

        if response_status_code != 200:

            self.logger.error(LOGGING_REQUEST_BAD_STATUS_ERROR_TEMPLATE.format(
                service_name='STT', status_code=response_status_code, context=''
            ))

            return False, USER_FRIENDLY_REQUEST_ERROR_MESSAGE

        self.logger.info('STT request success')

        return True, response.json()['result']


stt = STT()
