import string
import telebot

from library import *
from func_pass import strong_pass
from faq_bot import faq_about
from end_of_words import period_result, end_of_word
from func_pass import social_password, pass_corrector


bot = telebot.TeleBot('7763321668:AAELL2LjdEvhL_CqN1hcGb7ulM4S1sGWgaw')
bot.set_webhook()


@bot.message_handler(commands=["start"])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Пароль для соц сетей', 'Сложный пароль')
    bot.send_message(m.chat.id,
                     '\n\n*🔐 Напиши боту свой пароль и'
                     ' он проверит его на надежность*\\!\n'
                     '*Либо можешь сгенерировать уже готовый\\!*\n\n'
                     '1️⃣ Пароль для соц сетей\n'
                     '\n2️⃣ Сложный пароль\n',
                     reply_markup=markup, parse_mode='MarkdownV2')


@bot.message_handler(commands=["help"])
def help(m):
    bot.send_message(m.chat.id, 'По всем вопросам работы бота писать *@SpectreGather*\n'
                                '\n*Бот создан в рамках индивидульного проекта*', parse_mode='MarkdownV2')


@bot.message_handler(commands=["about"])
def help(m):
    result = faq_about()
    bot.send_message(m.chat.id, result, parse_mode='MarkdownV2')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    flag = True
    check_string = string.ascii_lowercase + string.ascii_uppercase + string.punctuation + string.digits

    if message.text.strip() == 'Пароль для соц сетей':
        markup = telebot.types.ReplyKeyboardMarkup(True)
        markup.row('🗺 Google', '📮 Yandex', '📘 Vk', '📬 Mail')
        markup.row('💬 Facebook', '📺 Avito', '📱 Instagram')
        markup.row('📄 Gosuslugi', '🔥 Свой вариант')
        markup.row('🏠 Назад в меню')
        bot.send_message(message.chat.id,'*Выбери* к чему тебе нужно придумать пароль', reply_markup=markup, parse_mode='MarkdownV2')

    elif message.text.strip() in ('🗺 Google', '📮 Yandex', '📘 Vk', '📬 Mail', '💬 Facebook', '📺 Avito', '📱 Instagram', '📄 Gosuslugi'):
        text_to_function = message.text.lower()
        bot.send_message(message.chat.id,
                         social_password(text_to_function[2:]))

    elif message.text.strip() == '🔥 Свой вариант':
        bot.send_message(message.chat.id, 'Напиши название *сайта* или *приложения*', parse_mode='MarkdownV2')
        bot.register_next_step_handler(message, get_individual)

    elif message.text.strip() == '🏠 Назад в меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('Пароль для соц сетей', 'Сложный пароль')
        bot.send_message(message.chat.id, '🏝 Ты в меню', reply_markup=markup)

    elif message.text.strip() == 'Сложный пароль':
        answer = strong_pass(False)
        bot.send_message(message.chat.id, '*'f'{answer}*',
                         parse_mode='MarkdownV2')
    else:
        for char in message.text.strip():
            if char not in check_string:
                flag = False
        if flag:
            get_pass(message)
        else:
            bot.send_message(message.chat.id,
                             '❌ *Недопустимые символы*\n'
                             'Проверьте вводимый текст\n\n'
                             '\\- Есть пробелы\n'
                             '\\- Перепутана русская *A* и латинская\n'
                             '\\- Есть нестандартные символы\n\n'
                             '*P\\.S\\. Бот различает русский и '
                             'латинский алфавит*',
                             parse_mode='MarkdownV2')


def get_individual(message: types.Message):
    check_string = string.ascii_lowercase + string.ascii_uppercase + \
                   string.punctuation + string.digits
    text = message.text
    flag = True
    for char in message.text.strip():
        if char not in check_string:
            flag = False

    if message.text.strip() in ('🗺 Google', '📮 Yandex', '📘 Vk', '📬 Mail', '💬 Facebook', '📺 Avito', '📱 Instagram', '📄 Gosuslugi'):
        text = message.text[2:].lower()
        bot.send_message(message.chat.id, '💎 Вот *пять вариантов* для тебя\\!', parse_mode='MarkdownV2')
        for _ in range(0, 5):
            bot.send_message(message.chat.id, social_password(text))
    elif flag is False:
        bot.send_message(message.chat.id,
                         '❌ *Недопустимые символы*\n'
                         'Проверьте вводимый текст\n\n'
                         '\\- Есть пробелы\n'
                         '\\- Перепутана русская *A* и латинская\n'
                         '\\- Есть нестандартные символы\n\n'
                         '*P\\.S\\. Бот различает русский и '
                         'латинский алфавит*',
                         parse_mode='MarkdownV2')
        return 0
    else:
        bot.send_message(message.chat.id, '💎 Вот *пять вариантов* для тебя\\!', parse_mode='MarkdownV2')
        for _ in range(0, 5):
            bot.send_message(message.chat.id, social_password(text))


@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    corrected_password = pass_corrector(call.data)
    bot.send_message(call.message.chat.id, corrected_password)


bot.polling(none_stop=True, interval=0)