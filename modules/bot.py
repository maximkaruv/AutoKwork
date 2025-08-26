from config import TOKEN, USERID
import telebot

bot = telebot.TeleBot(TOKEN)

def send_message(text: str):
    try:
        bot.send_message(USERID, text, parse_mode="HTML")
        print(f"[bot] Сообщение отправлено")
    except Exception as e:
        print(f"[bot] Ошибка при отправке: {e}\nСообщение: {text}")

