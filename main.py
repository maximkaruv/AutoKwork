from modules.logging import setlogger, logger
from modules.kwork import KworkAPI
from modules.bot import send_message
import json, os
from time import sleep


setlogger('main.log')
kwork = KworkAPI()

# Шаблон уведомления
NOTIFICATION = """Новый кворк {id}
<b>"{title}"</b>
{description}
-----------------
Цена: <b>{price}</b>₽
Максимальная цена: <b>{max_price}</b>₽
Откликов: {offers_count}
Действителен <i>до {last_date}</i>
"""

# Файл для хранения полученных id кворков
ORDERS_FILE = "orders.json"


# Загружаем старые кворки
def load_orders():
    if os.path.exists(ORDERS_FILE) and os.path.getsize(ORDERS_FILE) > 0:
        try:
            with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Ошибка чтения {ORDERS_FILE}: {e}")
    return []


# Сохраняем новые квкорки
def save_orders(orders):
    try:
        with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка записи {ORDERS_FILE}: {e}")


# Проверяем биржу на наличие новых кворков и отправляем уведомления
async def fetch_updates():
    orders = kwork.get_orders()
    if not orders:
        logger.error("Не удалось получить кворки")
        return

    old_orders = load_orders()
    old_ids = {o['id'] for o in old_orders}

    new_orders = [o for o in orders if o['id'] not in old_ids]

    if not new_orders:
        logger.warning("Новых кворков не найдено")
        logger.info("=== Цикл завершён ===")

    logger.info(f"Найдено {len(new_orders)} новых кворков")

    for order in new_orders:
        desc = f"-----------------\n{order["description"]}" if order.get('description') else ""
        send_message(NOTIFICATION.format(
            id=order['id'],
            title=order['title'],
            description=desc,
            price=order['price'],
            max_price=order['max_price'],
            offers_count=order['offers_count'],
            last_date=order['last_date']
        ))
        sleep(2)

    all_orders = old_orders + new_orders
    save_orders(all_orders)

    logger.info("=== Цикл завершён ===")


# Запуск
if __name__ == "__main__":
    while True:
        logger.info('=== Запущен новый цикл ===')
        fetch_updates()
        sleep(60 * 5)
