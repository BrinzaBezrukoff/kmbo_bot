from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from config import BOT_TOKEN, ALLOW_ID, DEFAULT_ROLE
from models import db_required, Subject, Deadline
from perms import role_required, user_required
from enums import Role
from markups import *


bot = TeleBot(BOT_TOKEN)


def permission_deny(message, user):
    if isinstance(message, Message):
        bot.reply_to(message, "У вас нет прав для выполнения этого действия!")
    elif isinstance(message, CallbackQuery):
        bot.answer_callback_query(message.id, "У вас нет прав для выполнения этого действия!")


@bot.message_handler(commands=["start"])
def command_start(message):
    bot.reply_to(message, ("Привет, этот бот помогает упростить учёт дедлайнов!\n"
                           "Для начала представься с помощью /id\n"
                           "Используй /menu, чтобы открыть меню бота"))


@bot.message_handler(commands=["id"])
@user_required
def command_id(message, user):
    if user.role != Role.Guest:
        bot.reply_to(message, "Вы уже представлялись ранее =)")
        return
    if not ALLOW_ID:
        bot.reply_to(message, "Увы! Возможность представиться была закрыта.")
        return
    bot.send_message(message.chat.id, "Напиши своё имя и фамилию через пробел:")
    bot.register_next_step_handler(message, identify_user, user=user)


@db_required
def identify_user(message, user, db):
    try:
        name, surname = message.text.split()
    except ValueError:
        bot.send_message(message.chat.id, "Не удалось представиться. Не был соблюден формат ввода.")
        return
    user.name = name
    user.surname = surname
    user.role = max(user.role, DEFAULT_ROLE)
    db.add(user)
    db.commit()
    bot.send_message(message.chat.id, (f"Вы успешно представиилсь, как {user.name} {user.surname}.\n"
                                       f"Ваша роль {user.role_name}."))


@bot.message_handler(commands=["menu"])
@user_required
def command_menu(message, user):
    if user.role < DEFAULT_ROLE:
        bot.reply_to(message, ("Увы, но ваших прав недостаточно для использования меню.\n"
                               "Не забывайте представиться с помощью /id"))
        return
    bot.send_message(message.chat.id, "<b>Вот список доступных разделов</b>",
                     parse_mode="html", reply_markup=get_main_menu())


@bot.callback_query_handler(lambda call: call.data == "menu")
@role_required(DEFAULT_ROLE, permission_deny)
def callback_menu(call):
    bot.edit_message_text("<b>Вот список доступных разделов</b>",
                          call.message.chat.id,
                          call.message.id,
                          parse_mode="html",
                          reply_markup=get_main_menu())


@bot.callback_query_handler(lambda call: call.data in ["all_subjects", "all_deadlines"])
@role_required(Role.User, permission_deny)
@db_required
def process_lists(call, db):
    if call.data == "all_subjects":
        all_subjects = db.query(Subject).all()
        title = "Доступные предметы:"
        mk = get_subjects_markup(all_subjects)
    else:
        all_deadlines = db.query(Deadline).order_by(Deadline.dead_date)
        title = "Актуальные дедлайны:"
        mk = get_deadlines_markup(all_deadlines)
    bot.edit_message_text(title, call.message.chat.id, call.message.id, reply_markup=mk)


@bot.callback_query_handler(lambda call: call.data.startswith("subject"))
@role_required(Role.User, permission_deny)
@db_required
def subject_info(call, db):
    try:
        subj_id = int(call.data.split("_")[1])
    except (ValueError, IndexError):
        bot.edit_message_text("Непредвиденная ошибка!", call.message.chat.id, call.message.id)
        return
    subj = db.query(Subject).get(subj_id)
    if not subj:
        bot.edit_message_text("Такой предмет не найден, возможно это ошибка!", call.message.chat.id, call.message.id)
        return
    bot.edit_message_text("Нет подробной информации для предмета...",
                          call.message.chat.id,
                          call.message.id,
                          reply_markup=get_back_markup("all_subjects"))


@bot.callback_query_handler(lambda call: call.data.startswith("deadline"))
@role_required(Role.User, permission_deny)
@db_required
def deadline_info(call, db):
    try:
        deadline_id = int(call.data.split("_")[1])
    except (ValueError, IndexError):
        bot.edit_message_text("Непредвиденная ошибка!", call.message.chat.id, call.message.id)
        return
    dl = db.query(Deadline).get(deadline_id)
    if not dl:
        bot.edit_message_text("Такой дедлайн не найден, возможно это ошибка!", call.message.chat.id, call.message.id)
        return
    bot.edit_message_text((f"<u>{dl.name}</u>\n"
                           f"Предмет: {dl.subject.name}\n"
                           f"Дата: <b>{dl.dead_str}</b>\n\n"
                           f"Описание:\n{dl.description}"),
                          call.message.chat.id,
                          call.message.id,
                          parse_mode="html",
                          reply_markup=get_back_markup("all_deadlines"))


@bot.callback_query_handler(lambda call: call.data == "open_editorial")
@role_required(Role.Editor, permission_deny)
def callback_editorial(call):
    bot.edit_message_text("Раздел редактора",
                          call.message.chat.id,
                          call.message.id,
                          reply_markup=get_editorial_markup())
