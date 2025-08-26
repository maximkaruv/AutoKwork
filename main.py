from modules.kwork import KworkAPI
from modules.bot import send_message
from time import sleep
import json

kwork = KworkAPI()

NOTIFICATION = """Новый кворк {id}!
*\"{title}\"*
{description}
-----------------
Цена: *{price}*
Максимальная цена: *{max_price}*
Откликов: {offers_count}
Действителен до _{last_date}_
"""

def fetch_updates():
    orders = [order for order in kwork.get_orders()]
    old_orders = json.load(open('orders.json', 'r'))

    if orders != old_orders:
        new_orders = [x for x in orders if x not in old_orders]
        json.dump(open('orders.json', 'w'), indent=2, ensure_ascii=False)

        for order in new_orders:
            desc = order['description']
            desc = f'-----------------\n{desc}' if desc else ''

            send_message(NOTIFICATION.format(
                title=order['title'],
                description=desc,
                price=order['price'],
                max_price=order['max_price'],
                offers_count=order['offers_count'],
                last_date=order['last_date']
            ))
            sleep(2)

while True:
    fetch_updates()
    sleep(60*5)