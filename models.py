class Indexes:
    transaction_id: str = None
    merchant_id: str = None
    user_id: str = None
    card_number: str = None
    transaction_date: str = None
    hour: str = None
    transaction_amount: str = None
    device_id: str = None
    recommendation: str = None


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
    def __init__(self, cards_number: list[str], amount: float, devices_id: list[str], cbk: int, orders: int, hour: str):
        self.cards_number: list[str] = cards_number
        self.amount: float = amount
        self.devices_id: list[str] = devices_id
        self.cbk: int = cbk
        self.orders: int = orders
        self.hour: int = hour

    def insert(self, card_number: str, amount: float, device_id: str, cbk: bool):
        self.cards_number = [card_number]
        self.amount = float(amount)
        self.devices_id = [device_id]

        if cbk == 'TRUE':
            self.cbk = 1

    def update(self, card_number: str, amount: float, device_id: str, cbk: bool, hour: str):
        self.amount = self.amount + float(amount)
        self.orders = self.orders + 1

        if card_number not in self.cards_number:
            self.cards_number.append(card_number)

        if device_id not in self.devices_id:
            self.devices_id.append(device_id)

        if cbk == 'TRUE':
            self.cbk += 1

        if int(hour) < self.hour:
            self.hour = int(hour)


class Suspect:
    def __init__(self, user_id: str, score: int, reasons: list[str]):
        self.user_id: str = user_id
        self.score: int = score
        self.reasons: list[str] = reasons

    def updateScore(self, score: int):
        if (self.score != 100):
            if (self.score + score > 100):
                self.score = 100
            else:
                self.score = self.score + score


class SuspectCard(Suspect):
    def __init__(self, card_id: str, score: int, reasons: list[str]):
        self.card_id: str = card_id
        self.score: int = score
        self.reasons: list[str] = reasons

    def updateScore(self, score: int):
        super().updateScore(score)
