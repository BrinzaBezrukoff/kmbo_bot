from enum import IntEnum, unique


@unique
class Role (IntEnum):
    Guest = 0
    User = 1
    Editor = 2
    Admin = 3
