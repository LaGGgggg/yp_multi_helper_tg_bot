from telebot.handler_backends import State, StatesGroup


class DebugStates(StatesGroup):

    active = State()
    inactive = State()
