from random import choice
from pathlib import Path

from telebot import TeleBot, types, custom_filters
from telebot.storage import StateMemoryStorage
from sqlalchemy.orm import Session

from services.stt import stt
from services.tts import tts
from services.gpt import gpt
from settings import (
    BOT_TOKEN,
    TTS_CHARACTERS_IN_BLOCK,
    STT_SECONDS_IN_BLOCK,
    SECOND_BLOCKS_LIMIT_BY_USER,
    CHARACTER_BLOCKS_LIMIT_BY_USER,
    TOKENS_LIMIT_BY_USER,
    WARNING_LOG_FILE_PATH,
    INFO_LOG_FILE_PATH,
    DEBUG_USER_ID,
)
from sql.database import SessionLocal, create_all_tables
from sql.models import User
from sql.crud import UserCrud, UserMessageCrud
from sql.model_enums import RolesEnum
from bot_support_modules.markups import MAIN_MARKUP, DEBUG_MARKUP
from bot_support_modules.states import DebugStates
from bot_support_modules.validators import (
    max_users_amount_limit_validator,
    request_character_blocks_limit_validator,
    request_second_blocks_limit_validator,
    request_tokens_limit_validator,
    user_character_blocks_limit_validator,
    user_second_blocks_limit_validator,
    user_tokens_limit_validator,
)


def run_bot() -> None:

    bot = TeleBot(BOT_TOKEN, state_storage=StateMemoryStorage())

    bot.add_custom_filter(custom_filters.StateFilter(bot))

    def get_state_markup(message: types.Message) -> types.ReplyKeyboardMarkup:

        if bot.get_state(message.from_user.id) == DebugStates.inactive.name:
            return MAIN_MARKUP

        else:
            return DEBUG_MARKUP

    @bot.message_handler(commands=['help', 'start'])
    def help_handler(message: types.Message):

        if bot.get_state(message.from_user.id) is None:
            bot.set_state(message.from_user.id, DebugStates.inactive)

        reply_message = (
            'Привет, я - бот-поддержатор! Буду стараться тебя поддерживать, чтобы ты не грустил. Ты можешь просто'
            ' написать что-то или сказать, а я отвечу!'
            ' (На каждого пользователя есть лимиты использования бота, без этого никак)\n\n'
            'Если тебе хочется больше узнать о моих командах, то вот они:\n'
            '/help или /start - список всех команд (ты уже тут)\n'
            '/stats - статистика (потраченные токены и т.д.)\n\n'
            'Далее начинается зона отладки, если ты не уверен в том, что должен писать эти команды, то не пиши их:\n'
            '/toggle_debug - переход в режим отладки'
            ' (доступны команды для отладки, отключаются автоматические ответы на сообщения)\n'
            'Доступно только в режиме отладки:\n'
            '/stt - тест перевода голоса в текст\n'
            '/tts - тест перевода текста в голос\n'
            'Получение логов по следующим командам доступно не всем:\n'
            '/get_logs_warning - получение файла с логами (с уровня "предупреждение" и выше)\n'
            '/get_logs_info - получение файла с логами (с уровня "информация" и выше)\n'
        )

        bot.reply_to(message, reply_message, reply_markup=get_state_markup(message))

    @bot.message_handler(commands=['stats'])
    def stats_handler(message: types.Message):
        with SessionLocal() as session:

            user = UserCrud(session).get_or_create(telegram_id=message.from_user.id)

            bot.reply_to(
                message,
                f'Потрачено блоков символов ({TTS_CHARACTERS_IN_BLOCK} символов в каждом):'
                f' {user.character_blocks_spent} из {CHARACTER_BLOCKS_LIMIT_BY_USER}\n'
                f'Потрачено блоков секунд ({STT_SECONDS_IN_BLOCK} символов в каждом): {user.second_blocks_spent} из'
                f' {SECOND_BLOCKS_LIMIT_BY_USER}\n'
                f'Потрачено токенов: {user.tokens_spent} из {TOKENS_LIMIT_BY_USER}',
            )

    @bot.message_handler(commands=['toggle_debug'])
    @max_users_amount_limit_validator(bot)
    def toggle_debug(message: types.Message):

        if bot.get_state(message.from_user.id) == DebugStates.active.name:
            bot.set_state(message.from_user.id, DebugStates.inactive)

        else:
            bot.set_state(message.from_user.id, DebugStates.active)

        bot.reply_to(message, 'Debug режим переключён', reply_markup=get_state_markup(message))

    @request_character_blocks_limit_validator(bot)
    @user_character_blocks_limit_validator(bot)
    def ask_tts(_: types.Message, prompt: str, user: User, session: Session) -> bytes | str:
        """
        Return a byte voice message if success else an error message string.
        """
        tts_answer = tts.ask(prompt)

        if isinstance(tts_answer, bytes):

            user.character_blocks_spent += tts.get_character_blocks(len(prompt))

            session.commit()

        return tts_answer

    @request_second_blocks_limit_validator(bot)
    @user_second_blocks_limit_validator(bot)
    def ask_stt(message: types.Message, user: User, session: Session) -> tuple[bool, str]:
        """
        Return a recognized string and True if success else an error message string and False.
        """

        stt_prompt: bytes = bot.download_file(bot.get_file(message.voice.file_id).file_path)

        is_success, stt_answer = stt.ask(stt_prompt)

        if is_success:

            user.second_blocks_spent += stt.get_second_blocks(message.voice.duration)

            session.commit()

        return is_success, stt_answer

    def _debug_stt(message: types.Message):
        with SessionLocal() as session:

            user = UserCrud(session).get_or_create(telegram_id=message.from_user.id)

            stt_answer = ask_stt(message, user, session)

            if stt_answer is not None:
                bot.reply_to(message, stt_answer[1], reply_markup=DEBUG_MARKUP)

    @bot.message_handler(commands=['stt'], state=DebugStates.active)
    @max_users_amount_limit_validator(bot)
    def debug_stt(message: types.Message):

        bot.reply_to(message, 'Отправьте голосовое сообщение для теста')

        bot.register_next_step_handler(message, _debug_stt)

    def _debug_tts(message: types.Message):
        with SessionLocal() as session:

            user = UserCrud(session).get_or_create(telegram_id=message.from_user.id)

            tts_answer = ask_tts(message, message.text, user, session)

            if tts_answer is not None:

                if isinstance(tts_answer, bytes):
                    bot.send_voice(message.from_user.id, tts_answer, reply_markup=DEBUG_MARKUP)

                else:
                    bot.reply_to(message, tts_answer, reply_markup=DEBUG_MARKUP)

    @bot.message_handler(commands=['tts'], state=DebugStates.active)
    @max_users_amount_limit_validator(bot)
    def debug_tts(message: types.Message):

        bot.reply_to(message, 'Отправьте текстовое сообщение для теста')

        bot.register_next_step_handler(message, _debug_tts)

    def _get_logs_file_handler(message: types.Message, log_file_path: Path, visible_file_name: str) -> None:
        with open(log_file_path, 'rb') as f:

            file_data = f.read()

            if not file_data:

                bot.reply_to(message, 'Файл с логами пуст!')

                return

            bot.send_document(message.chat.id, file_data, visible_file_name=visible_file_name)

    @bot.message_handler(commands=['get_logs_warning'], func=lambda message: message.from_user.id == DEBUG_USER_ID)
    def get_logs_warning_handler(message: types.Message):
        _get_logs_file_handler(message, WARNING_LOG_FILE_PATH, 'logs_warning.log')

    @bot.message_handler(commands=['get_logs_info'], func=lambda message: message.from_user.id == DEBUG_USER_ID)
    def get_logs_info_handler(message: types.Message):
        _get_logs_file_handler(message, INFO_LOG_FILE_PATH, 'logs_info.log')

    @request_tokens_limit_validator(bot)
    @user_tokens_limit_validator(bot)
    def ask_gpt(_: types.Message, prompt: str, user: User, session: Session) -> tuple[bool, str]:
        """
        Return gpt response and True if success else an error message string and False.
        """

        gpt_answer, tokens_spent = gpt.ask(prompt, user.messages[:10])

        if tokens_spent:

            user.tokens_spent += tokens_spent

            user_message_crud = UserMessageCrud(session)

            user_message_crud.create(user=user, text=prompt, role=RolesEnum.USER)
            user_message_crud.create(user=user, text=gpt_answer, role=RolesEnum.ASSISTANT)

            session.commit()

        return bool(tokens_spent), gpt_answer

    @bot.message_handler(content_types=['text'], state=DebugStates.inactive)
    @max_users_amount_limit_validator(bot)
    def process_text_message(message: types.Message):
        with SessionLocal() as session:

            user = UserCrud(session).get_or_create(telegram_id=message.from_user.id)

            gpt_answer = ask_gpt(message, message.text, user, session)

            if gpt_answer is not None:
                bot.reply_to(message, gpt_answer[1])

    @bot.message_handler(content_types=['voice'], state=DebugStates.inactive)
    @max_users_amount_limit_validator(bot)
    def process_voice_message(message: types.Message):
        with SessionLocal() as session:

            user = UserCrud(session).get_or_create(telegram_id=message.from_user.id)

            stt_result = ask_stt(message, user, session)

            if stt_result is None:
                return

            elif not stt_result[0]:

                bot.reply_to(message, stt_result[1])

                return

            gpt_answer = ask_gpt(message, stt_result[1], user, session)

            if gpt_answer is None:
                return

            elif not gpt_answer[0]:

                bot.reply_to(message, gpt_answer[1])

                return

            tts_answer = ask_tts(message, gpt_answer[1], user, session)

            if isinstance(tts_answer, bytes):
                bot.send_voice(message.from_user.id, tts_answer)

            else:
                bot.reply_to(message, tts_answer)

    @bot.message_handler(content_types=['text'])
    def unknown_messages_handler(message: types.Message):

        replies = (
            'О, круто!',
            'Верно подмечено!',
            'Как с языка снял',
            'Какой ты всё-таки умный',
            'По-любому что-то умное написал',
            'Как лаконично-то!',
        )

        help_message = (
            '\n\nЕсли ты хотел, чтобы я что-то сделал, то я не распознал твою команду, пожалуйста, сверься с /help'
        )

        bot.reply_to(message, choice(replies) + help_message, reply_markup=get_state_markup(message))

    bot.infinity_polling()


if __name__ == '__main__':

    create_all_tables()

    run_bot()
