class Indexes:
    transaction_id: str = None
    merchant_id: str = None
    user_id: str = None
    card_number: str = None
    transaction_date: str = None
    hour: str = None
    transaction_amount: str = None
    device_id: str = None


class Card:
    def __init__(self, users_id: list[str], devices_id: list[str]):
        self.users_id: list[str] = users_id
        self.devices_id: list[str] = devices_id

    def insert(self, user_id: str, device_id: str):
        self.users_id = [user_id]
        self.devices_id = [device_id]

    def update(self, user_id: str, device_id: str):
        if user_id not in self.users_id:
            self.users_id.append(user_id)

        if device_id not in self.devices_id:
            self.devices_id.append(device_id)


class User:
    def __init__(self, cards_number: list[str], amount: float, devices_id: list[str], cbk: int, orders: int):
        self.cards_number: list[str] = cards_number
        self.amount: float = amount
        self.devices_id: list[str] = devices_id
        self.cbk: int = cbk
        self.orders: int = orders

    def insert(self, card_number: str, amount: float, device_id: str, cbk: bool):
        self.cards_number = [card_number]
        self.amount = float(amount)
        self.devices_id = [device_id]

        if cbk:
            self.cbk = 1

    def update(self, card_number: str, amount: float, device_id: str, cbk: bool):
        self.amount = self.amount + float(amount)
        self.orders = self.orders + 1

        if card_number not in self.cards_number:
            self.cards_number.append(card_number)

        if device_id not in self.devices_id:
            self.devices_id.append(device_id)

        if cbk:
            if not self.cbk:
                self.cbk = 1
            else:
                self.cbk = self.cbk + 1
