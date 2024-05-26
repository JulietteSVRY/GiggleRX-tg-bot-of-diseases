import logging
import telebot
from handlers import register_handlers
from settings import TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)
register_handlers(bot)

if __name__ == '__main__':
    bot.polling(none_stop=True)