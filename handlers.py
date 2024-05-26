from telebot import TeleBot, types
from services import get_response_from_gigachat, get_image_url
import random

# Словарь для хранения состояний и истории сообщений пользователей
user_states = {}
user_histories = {}


def start_command(message: types.Message, bot: TeleBot):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text="Здравствуй! Расскажи о своих симптомах")
    # Устанавливаем начальное состояние и историю для пользователя
    user_states[chat_id] = 'awaiting_symptoms'
    user_histories[chat_id] = []


def handle_message(message: types.Message, bot: TeleBot):
    chat_id = message.chat.id
    # Получаем текущее состояние и историю пользователя
    user_state = user_states.get(chat_id, 'awaiting_symptoms')
    user_history = user_histories.get(chat_id, [])

    if user_state == 'awaiting_symptoms':
        user_symptoms = message.text
        user_history.append({'role': 'user', 'content': user_symptoms})

        response = get_response_from_gigachat(user_history)
        user_history.append({'role': 'assistant', 'content': response})

        bot.send_message(chat_id=chat_id, text=response)

        # Определяем сообщение перед отправкой фотографии
        cat_messages = [
            "Вот вам котик для поднятия настроения❤️!",
            "Не забудьте обнять котика сегодня!😻",
            "Котики делают мир лучше!😻",
            "Пусть этот котик принесет вам радость!❤️",
            "Кототерапия для вашего хорошего настроения!😻",
            "Получите заряд позитивных эмоций с этим котиком!❤️",
            "Котики всегда рядом, чтобы поднять настроение!😻",
            "Этот котик улыбается специально для вас!❤️",
            "Не забудьте, что котики всегда рядом!😻",
            "Немного кото-любви для вас!❤️"
        ]
        cat_message = random.choice(cat_messages)
        bot.send_message(chat_id=chat_id, text=cat_message)

        # Отправляем фотографию котика
        image_url = get_image_url()
        bot.send_photo(chat_id=chat_id, photo=image_url)

        # Сбрасываем состояние пользователя, если нужно
        user_states[chat_id] = 'awaiting_symptoms'
        user_histories[chat_id] = user_history


def register_handlers(bot: TeleBot):
    bot.register_message_handler(lambda message: start_command(message, bot), commands=['start'])
    bot.register_message_handler(lambda message: handle_message(message, bot), func=lambda message: True)
