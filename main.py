import random
import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6563459949:AAFWAEPmBP97Y9qpQWty_l8akdIx3jzciIM",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()
    favorite_color = State()
    favorite_number = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Опрос"  # Можно менять текст
text_button_1 = "Случайное число от 1 до 100"  # Можно менять текст
text_button_2 = "Нажми на меня 😇"  # Можно менять текст
text_button_3 = "Или на меня 😏"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        '*Привет!* Чем займёмся? ☺️',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, '*Супер!* Ваше _имя_? 🧐')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, '*Превосходно!* Ваш _возраст_? 😏')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, '*Великолепно!* Ваш _любимый цвет_? 🌈')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.favorite_color, message.chat.id)


@bot.message_handler(state=PollState.favorite_color)
def favorite_color(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['favorite_color'] = message.text
    bot.send_message(message.chat.id, '*Замечательно!* Ваше _любимое число_? 🔢')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.favorite_number, message.chat.id)


@bot.message_handler(state=PollState.favorite_number)
def favorite_number(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['favorite_number'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за прохождение опроса! 😌', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    number = random.randint(1, 100)
    bot.send_message(message.chat.id, str(number), reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Попался 😈](https://youtu.be/dQw4w9WgXcQ?si=QNTvZglZLXh7hTCV)",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "[Нажми 🥰](https://youtu.be/APk4mLodk88?si=UwgBv2NouJ-RPrFr)",
                     reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()
