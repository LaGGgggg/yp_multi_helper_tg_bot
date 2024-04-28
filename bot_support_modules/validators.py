from typing import Callable, Any
from functools import wraps

from telebot import TeleBot
from telebot.types import Message

from services.stt import stt
from services.tts import tts
from services.gpt import gpt
from sql.crud import UserCrud
from sql.database import SessionLocal
from settings import (
    REQUEST_MAX_SECOND_BLOCKS,
    REQUEST_MAX_CHARACTER_BLOCKS,
    REQUEST_MAX_TOKENS,
    SECOND_BLOCKS_LIMIT_BY_USER,
    CHARACTER_BLOCKS_LIMIT_BY_USER,
    TOKENS_LIMIT_BY_USER,
    MAX_USERS_AMOUNT_LIMIT,
)


def validator_factory(
        validation_function: Callable[[Message], bool], bot: TeleBot, validation_error_message: str
) -> Callable:
    """
    Return a decorator that wraps the given function with a validation function. If the validation function returns
    False, send the validation error message to the user and DO NOT call wrapped function.
    """

    def validator(func: Callable) -> Callable:

        @wraps(func)
        def _validator(message: Message, *args, **kwargs) -> Any:

            if validation_function(message):
                return func(message, *args, **kwargs)

            else:

                bot.reply_to(message, validation_error_message)

                return

        return _validator

    return validator


def validator_factory_extended(
        validation_function: Callable[[Message, Any], bool], bot: TeleBot, validation_error_message: str
) -> Callable:
    """
    Return a decorator that wraps the given function with a validation function. If the validation function returns
    False, send the validation error message to the user and DO NOT call wrapped function. This factory passes all args
    and kwargs into validation function.
    """

    def validator(func: Callable) -> Callable:

        @wraps(func)
        def _validator(message: Message, *args, **kwargs) -> Any:

            if validation_function(message, *args, **kwargs):
                return func(message, *args, **kwargs)

            else:

                bot.reply_to(message, validation_error_message)

                return

        return _validator

    return validator


def max_users_amount_limit_validator(bot: TeleBot) -> Callable:
    """
    If the number of users in the database is greater than MAX_USERS_AMOUNT_LIMIT, return
    the error message and DO NOT call the target function.
    """

    def _validator(_) -> bool:
        with SessionLocal() as session:
            return len(UserCrud(session).get_many()) <= MAX_USERS_AMOUNT_LIMIT

    return validator_factory(
        _validator, bot, 'К сожалению, в боте есть лимит на максимальное число пользователей, он превышен('
    )


def request_character_blocks_limit_validator(bot: TeleBot) -> Callable:
    """
    If the number of characters (in blocks) in the message is greater than REQUEST_MAX_CHARACTER_BLOCKS, return
    the error message and DO NOT call the target function.
    """

    def _validator(___: Message, prompt: str, *_, **__) -> Any:
        return tts.get_character_blocks(len(prompt)) <= REQUEST_MAX_CHARACTER_BLOCKS

    return validator_factory_extended(
        _validator, bot, 'Вы превысили лимит символов на сообщение, пожалуйста, сократите запрос'
    )


def request_second_blocks_limit_validator(bot: TeleBot) -> Callable:
    """
    If the duration (in blocks) of the message voice is greater than REQUEST_MAX_SECOND_BLOCKS, return
    the error message and DO NOT call the target function.
    """

    def _validator(message: Message) -> Any:
        return stt.get_second_blocks(message.voice.duration) <= REQUEST_MAX_SECOND_BLOCKS

    return validator_factory(
        _validator, bot, 'Вы превысили лимит длительности голосового сообщения, пожалуйста, сократите запрос'
    )


def request_tokens_limit_validator(bot: TeleBot) -> Callable:
    """
    If the number of tokens in the message is greater than REQUEST_MAX_TOKENS, return
    the error message and DO NOT call the target function.
    """

    def _validator(___: Message, prompt: str, *_, **__) -> Any:
        return gpt.get_prompt_tokens_amount(prompt) <= REQUEST_MAX_TOKENS

    return validator_factory_extended(
        _validator, bot, 'Вы превысили лимит токенов на сообщение, пожалуйста, сократите запрос'
    )


def user_character_blocks_limit_validator(bot: TeleBot) -> Callable:
    """
    If the number of characters (in blocks) in the message + user spent character blocks is greater than
    CHARACTER_BLOCKS_LIMIT_BY_USER, return the error message and DO NOT call the target function.
    """

    def _validator(message: Message, prompt: str, *_, **__) -> bool:
        with SessionLocal() as session:

            user = UserCrud(session).get_or_create(telegram_id=message.from_user.id)
            message_character_blocks = tts.get_character_blocks(len(prompt))

            return user.character_blocks_spent + message_character_blocks <= CHARACTER_BLOCKS_LIMIT_BY_USER

    return validator_factory_extended(
        _validator,
        bot,
        'К сожалению, в боте есть лимит на максимальное число символов текстовых сообщений на пользователя,'
        ' он превышен(\nВы более не можете пользоваться этим функционалом',
    )


def user_second_blocks_limit_validator(bot: TeleBot) -> Callable:
    """
    If the duration (in blocks) of the message voice + user spent second blocks is greater than
    SECOND_BLOCKS_LIMIT_BY_USER, return the error message and DO NOT call the target function.
    """

    def _validator(message: Message) -> bool:
        with SessionLocal() as session:

            user = UserCrud(session).get_or_create(telegram_id=message.from_user.id)
            message_second_blocks = stt.get_second_blocks(message.voice.duration)

            return user.second_blocks_spent + message_second_blocks <= SECOND_BLOCKS_LIMIT_BY_USER

    return validator_factory(
        _validator,
        bot,
        'К сожалению, в боте есть лимит на максимальное число голосовых сообщений (считается по общей длительности)'
        ' на пользователя, он превышен(\nВы более не можете пользоваться этим функционалом',
    )


def user_tokens_limit_validator(bot: TeleBot) -> Callable:
    """
    If the number of tokens in the message + user spent tokens is greater than
    TOKENS_LIMIT_BY_USER, return the error message and DO NOT call the target function.
    """

    def _validator(message: Message, prompt, *_, **__) -> bool:
        with SessionLocal() as session:

            user_tokens_spent = UserCrud(session).get_or_create(telegram_id=message.from_user.id).tokens_spent

            # prevent an extra API request if the limit is already exceeded
            if user_tokens_spent > TOKENS_LIMIT_BY_USER:
                return False

            return user_tokens_spent + gpt.get_prompt_tokens_amount(prompt) <= TOKENS_LIMIT_BY_USER

    return validator_factory_extended(
        _validator,
        bot,
        'К сожалению, в боте есть лимит на максимальное число токенов на пользователя,'
        ' он превышен(\nВы более не можете пользоваться этим функционалом',
    )
