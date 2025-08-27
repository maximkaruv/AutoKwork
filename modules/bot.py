from loguru import logger
from config import TOKEN, USERID
import telebot

bot = telebot.TeleBot(TOKEN)

def send_message(text: str):
    try:
        bot.send_message(
            USERID,
            text,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        logger.success(f"Отправлено уведомление: \"{text[:17]}..\"")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления\nОшибка: {e}\nСообщение: \"{text}\"")

