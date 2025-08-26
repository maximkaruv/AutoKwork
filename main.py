from kwork import KworkAPI

kwork = KworkAPI()

orders = []

for order in kwork.get_orders():
    print(order['id'])