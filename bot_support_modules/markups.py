from telebot.types import ReplyKeyboardMarkup, KeyboardButton


HELP_BUTTON = KeyboardButton(text='/help')
TOGGLE_DEBUG_BUTTON = KeyboardButton(text='/toggle_debug')

MAIN_MARKUP = ReplyKeyboardMarkup(resize_keyboard=True)

MAIN_MARKUP.add(KeyboardButton(text='/stats'))
MAIN_MARKUP.row(HELP_BUTTON, TOGGLE_DEBUG_BUTTON)

DEBUG_MARKUP = ReplyKeyboardMarkup(resize_keyboard=True)

DEBUG_MARKUP.row(KeyboardButton(text='/stt'), KeyboardButton(text='/tts'))
DEBUG_MARKUP.row(KeyboardButton(text='/get_logs_warning'), KeyboardButton(text='/get_logs_info'))
DEBUG_MARKUP.row(HELP_BUTTON, TOGGLE_DEBUG_BUTTON)
