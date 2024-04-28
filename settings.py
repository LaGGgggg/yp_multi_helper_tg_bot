from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    # logging
    LOGS_DIR: Path = Path(__file__).resolve().parent / 'logs'

    WARNING_LOG_FILE_PATH: Path = LOGS_DIR / 'warning.log'
    INFO_LOG_FILE_PATH: Path = LOGS_DIR / 'info.log'

    # error messages
    USER_FRIENDLY_REQUEST_ERROR_MESSAGE: str = \
        'Произошла ошибка, пожалуйста, повторите попытку или обратитесь в поддержку'
    LOGGING_REQUEST_UNKNOWN_ERROR_TEMPLATE: str = \
        'An exception occurred while requesting {service_name} answer: {error}\n\nContext: "{context}"'
    LOGGING_REQUEST_BAD_STATUS_ERROR_TEMPLATE: str = \
        'Incorrect {service_name} answer status code: {status_code} (context: "{context}")'

    # TTS (text to speech)
    TTS_CHARACTERS_IN_BLOCK: int = 250
    TTS_URL: str = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    TTS_LANGUAGE: str = 'ru-RU'
    TTS_VOICE: str = 'filipp'

    # STT (speech to text)
    STT_SECONDS_IN_BLOCK: int = 15
    STT_URL: str = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
    STT_LANGUAGE: str = 'ru-RU'

    # GPT
    GPT_URL: str = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    GPT_TOKENIZE_URL: str = 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize'
    GPT_MODEL: str = 'yandexgpt-lite'
    GPT_TEMPERATURE: float = 1
    GPT_SYSTEM_PROMPT: str = (
        'Ты должен оказать поддержку. Общайся вежливо и создавай хорошее настроение. Будь краток.'
        ' Не пиши НИЧЕГО про готовность оказать поддержку или создать хорошее настроение'
    )
    GPT_RESPONSE_MAX_TOKENS: int = 300

    # request limits
    REQUEST_MAX_SECOND_BLOCKS: int = 2
    REQUEST_MAX_CHARACTER_BLOCKS: int = 5
    REQUEST_MAX_TOKENS: int = 300

    # user limits
    SECOND_BLOCKS_LIMIT_BY_USER: int = 25  # calculation by: ceil(seconds / STT_SECONDS_IN_BLOCK)
    CHARACTER_BLOCKS_LIMIT_BY_USER: int = 20  # calculation by: ceil(characters / TTS_CHARACTERS_IN_BLOCK)
    TOKENS_LIMIT_BY_USER: int = 2500
    MAX_USERS_AMOUNT_LIMIT: int = 10

    # must only be environment variables
    DB_URL: str
    BOT_TOKEN: str
    STT_API_KEY: str
    STT_FOLDER_ID: str
    TTS_API_KEY: str
    TTS_FOLDER_ID: str
    GPT_API_KEY: str
    GPT_FOLDER_ID: str
    DEBUG_USER_ID: int


_SETTINGS = Settings()

_SETTINGS.LOGS_DIR.mkdir(exist_ok=True)


def __getattr__(name: str) -> Any:
    return getattr(_SETTINGS, name)
