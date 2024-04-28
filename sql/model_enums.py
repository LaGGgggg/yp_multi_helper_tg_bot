from enum import Enum


class RolesEnum(Enum):

    ASSISTANT = 'assistant'
    USER = 'user'

    def __str__(self):
        return self.value
