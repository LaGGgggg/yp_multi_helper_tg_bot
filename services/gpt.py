from functools import lru_cache

from requests import post

from get_logger import get_logger
from sql.models import UserMessage
from settings import (
    GPT_API_KEY,
    GPT_FOLDER_ID,
    GPT_URL,
    GPT_TOKENIZE_URL,
    GPT_MODEL,
    GPT_TEMPERATURE,
    GPT_SYSTEM_PROMPT,
    GPT_RESPONSE_MAX_TOKENS,
    USER_FRIENDLY_REQUEST_ERROR_MESSAGE,
    LOGGING_REQUEST_UNKNOWN_ERROR_TEMPLATE,
    LOGGING_REQUEST_BAD_STATUS_ERROR_TEMPLATE,
)


class GPT:

    def __init__(self) -> None:

        self.logger = get_logger('main')
        self.model_uri = f'gpt://{GPT_FOLDER_ID}/{GPT_MODEL}'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Api-Key {GPT_API_KEY}',
        }

    @lru_cache(maxsize=25)  # cannot use just "cache" because tokenization is not static
    def get_prompt_tokens_amount(self, prompt: str) -> int | None:

        try:
            response = post(
                GPT_TOKENIZE_URL,
                headers=self.headers,
                json={
                    'modelUri': self.model_uri,
                    'text': prompt,
                },
            )

        except Exception as e:

            self.logger.error(LOGGING_REQUEST_UNKNOWN_ERROR_TEMPLATE.format(
                service_name='GPT', error=e, context=prompt
            ))

            return

        response_status_code = response.status_code

        if response_status_code != 200:

            self.logger.error(LOGGING_REQUEST_BAD_STATUS_ERROR_TEMPLATE.format(
                service_name='GPT', status_code=response_status_code, context=prompt
            ))

            return

        return len(response.json()['tokens'])

    def ask(self, prompt: str, previous_messages: list[UserMessage]) -> tuple[str, int | None]:
        """
        Return a GPT answer text and a total number of tokens spent on this request if success else an error message
        and None.
        """

        messages = [
            {'role': 'system', 'text': GPT_SYSTEM_PROMPT},
            *({'role': str(message.role), 'text': message.text} for message in previous_messages),
            {'role': 'user', 'text': prompt},
        ]

        try:
            response = post(
                GPT_URL,
                headers=self.headers,
                json={
                    'modelUri': self.model_uri,
                    'completionOptions': {
                        'temperature': GPT_TEMPERATURE,
                        'maxTokens': GPT_RESPONSE_MAX_TOKENS,
                        'stream': False,
                    },
                    'messages': messages,
                },
            )

        except Exception as e:

            self.logger.error(LOGGING_REQUEST_UNKNOWN_ERROR_TEMPLATE.format(
                service_name='GPT', error=e, context=prompt
            ))

            return USER_FRIENDLY_REQUEST_ERROR_MESSAGE, None

        response_status_code = response.status_code

        if response_status_code != 200:

            self.logger.error(LOGGING_REQUEST_BAD_STATUS_ERROR_TEMPLATE.format(
                service_name='GPT', status_code=response_status_code, context=prompt
            ))

            return USER_FRIENDLY_REQUEST_ERROR_MESSAGE, None

        response_json = response.json()['result']

        answer = response_json['alternatives'][0]['message']['text']
        tokens_spent = int(response_json['usage']['completionTokens'])

        self.logger.info('GPT request success')

        return answer, tokens_spent


gpt = GPT()
