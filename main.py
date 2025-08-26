import json
import os
from time import sleep
from modules.kwork import KworkAPI
from modules.bot import send_message

# Инициализация API
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

# Файл для хранения заказов
ORDERS_FILE = 'orders.json'

def load_orders():
    """Загружает старые заказы из файла, возвращает список"""
    if os.path.exists(ORDERS_FILE) and os.path.getsize(ORDERS_FILE) > 0:
        try:
            with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f'[error] Ошибка чтения {ORDERS_FILE}: {e}')
    return []


def save_orders(orders):
    """Сохраняет заказы в файл безопасно через временный файл"""
    tmp_file = ORDERS_FILE + '.tmp'
    with open(tmp_file, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    os.replace(tmp_file, ORDERS_FILE)


def fetch_updates():
    """Проверяет новые кворки и отправляет уведомления"""
    orders = kwork.get_orders()
    if not orders:
        print('[warn] Не удалось получить кворки')
        return

    old_orders = load_orders()
    old_ids = {o['id'] for o in old_orders}

    # Находим новые заказы
    new_orders = [o for o in orders if o['id'] not in old_ids]

    if new_orders:
        print(f'[info] Найдено {len(new_orders)} новых кворков')

        for order in new_orders:
            desc = f'-----------------\n{order["description"]}' if order.get("description") else ''
            send_message(NOTIFICATION.format(
                id=order['id'],
                title=order['title'],
                description=desc,
                price=order['price'],
                max_price=order['max_price'],
                offers_count=order['offers_count'],
                last_date=order['last_date']
            ))
            sleep(2)  # небольшая пауза между сообщениями

        # Объединяем старые и новые заказы и сохраняем
        all_orders = old_orders + new_orders
        save_orders(all_orders)
    else:
        print('[warn] Новых кворков нет')

    print('[info] Цикл завершён')


if __name__ == "__main__":
    while True:
        print('[info] Запущен новый цикл')
        fetch_updates()
        sleep(60 * 5)  # каждые 5 минут
