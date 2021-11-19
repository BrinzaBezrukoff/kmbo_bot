from enum import IntEnum, unique


@unique
class Role (IntEnum):
    GUEST = 0
    USER = 1
    EDITOR = 2
    ADMIN = 3
