from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_subjects_markup(subjects):
    mk = InlineKeyboardMarkup(row_width=1)
    for v in subjects:
        mk.add(InlineKeyboardButton(v.name, callback_data=f"subject_{v.id}"))
    mk.add(InlineKeyboardButton("<<<", callback_data="menu"))
    return mk


def get_deadlines_markup(deadlines):
    mk = InlineKeyboardMarkup(row_width=1)
    for v in deadlines:
        mk.add(InlineKeyboardButton(f"{v.subject.name}: {v.name} ({v.dead_str})", callback_data=f"deadline_{v.id}"))
    mk.add(InlineKeyboardButton("<<<", callback_data="menu"))
    return mk


def get_back_markup(data, title=None):
    if not title:
        title = "<<<"
    mk = InlineKeyboardMarkup(row_width=1)
    mk.add(InlineKeyboardButton(f"{title}", callback_data=data))
    return mk


def get_main_menu():
    mk = InlineKeyboardMarkup(row_width=1)
    mk.add(InlineKeyboardButton("Предметы", callback_data="all_subjects"))
    mk.add(InlineKeyboardButton("Дедлайны", callback_data="all_deadlines"))
    mk.add(InlineKeyboardButton("Раздел редактора", callback_data="open_editorial"))
    return mk


def get_editorial_markup():
    mk = InlineKeyboardMarkup(row_width=3)
    mk.add(InlineKeyboardButton("Предметы", callback_data="*"),
           InlineKeyboardButton("Добавить", callback_data="add_subject"),
           InlineKeyboardButton("Удалить", callback_data="del_subject"))
    mk.add(InlineKeyboardButton("Дедлайны", callback_data="*"),
           InlineKeyboardButton("Добавить", callback_data="add_deadline"),
           InlineKeyboardButton("Удалить", callback_data="del_deadline"))
    return mk
