from telebot import TeleBot

from config import BOT_TOKEN, ALLOW_ID, DEFAULT_ROLE
from models import db_required, Subject, Deadline
from perms import role_required, user_required
from enums import Role


bot = TeleBot(BOT_TOKEN)


def permission_deny_cb(message, user):
    bot.reply_to(message, "У вас нет прав для выполнения этого действия!")


@bot.message_handler(commands=["start"])
def command_start(message):
    bot.reply_to(message, ("Привет, этот бот помогает упростить учёт дедлайнов!\n"
                           "Для начала представься, если ты еще не сделал этого. Используй /id\n"
                           "Используй /subjects, чтобы открыть список предметов\n"
                           "Используй /deadlines, чтобы посмотреть дедлайны по конкретному предмету"))


@bot.message_handler(commands=["id"])
@user_required
def command_id(message, user):
    if user.role != Role.Guest:
        bot.reply_to(message, "Вы уже проходили идентификацию =)")
        return
    if not ALLOW_ID:
        bot.reply_to(message, "Увы! Идентификация пользователей была закрыта.")
        return
    bot.send_message(message.chat.id, "Напиши своё имя и фамилию через пробел:")
    bot.register_next_step_handler(message, identify_user, user=user)


@db_required
def identify_user(message, user, db):
    name, surname = message.text.split()
    user.name = name
    user.surname = surname
    user.role = max(user.role, DEFAULT_ROLE)
    db.add(user)
    db.commit()
    bot.send_message(message.chat.id, (f"Вы успешно представиилсь, как {user.name} {user.surname}.\n"
                                       f"Ваша роль {user.role_name}."))


@bot.message_handler(commands=["subjects"])
@role_required(Role.User, permission_deny_cb)
def command_subjects(message, user):
    bot.reply_to(message, f"Hello, {user}!")


@bot.message_handler(commands=["deadlines"])
@role_required(Role.User, permission_deny_cb)
def command_deadlines(message, user):
    bot.reply_to(message, f"Hello, {user}!")
