from datetime import datetime


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


class User:
    def __init__(self, cards_number: list[str], devices_id: list[str], cbk: int, orders: int):
        self.cards_number: list[str] = cards_number
        self.devices_id: list[str] = devices_id
        self.cbk: int = cbk
        self.orders: int = orders


def extractCsvData(file: str) -> tuple[list, Indexes]:
    # Dados das linhas da tabela
    rows = []
    # Abaixo estou criando como dicionário para facilitar a busca e não ter que relizar mais um loop
    # Lista de cartões e os dados aos quais estão vinculados
    cards = {}
    # Lista de usuários e os dados aos quais estão vinculados
    users = {}

    with open(file) as f:
        for line in f:
            line = line.strip()  # Remove espaços em branco
            if line:
                columns = line.split(',')  # Divide a linha em colunas

                if Indexes.user_id is None:
                    counter = 0
                    for column in columns:
                        match column:
                            case "transaction_id":
                                Indexes.transaction_id = counter
                            case "merchant_id":
                                Indexes.merchant_id = counter
                            case "user_id":
                                Indexes.user_id = counter
                            case "card_number":
                                Indexes.card_number = counter
                            case "transaction_date":
                                Indexes.transaction_date = counter
                                Indexes.hour = counter + 1
                                counter += 1
                            case "transaction_amount":
                                Indexes.transaction_amount = counter
                            case "device_id":
                                Indexes.device_id = counter
                            case "has_cbk":
                                Indexes.has_cbk = counter

                        counter += 1

                else:
                    # Converter data para hora e acrescentar na lista
                    hour = f"{datetime.fromisoformat(columns[Indexes.transaction_date]).hour}H"
                    columns.insert(Indexes.hour, hour)
                    rows.append(columns)

                    user_id = columns[Indexes.user_id]
                    device_id = columns[Indexes.device_id]
                    card_number = columns[Indexes.card_number]
                    cbk = columns[Indexes.has_cbk]

                    card = Card([], [])

                    # Verificar se o cartão ja existe e adicionar os dados, quantos usuários vinculados e quantos dispositivos
                    if card_number in cards:
                        currCard = currCard
                        if user_id not in currCard.users_id:
                            currCard.users_id.append(user_id)

                        if device_id not in currCard.devices_id:
                            currCard.devices_id.append(device_id)

                    else:
                        card.users_id = [user_id]
                        card.devices_id = [device_id]
                        currCard = card

                    # Verifica à quantos cartões e dispositivos um usuário está vinculado
                    # E saber o total de chargeback em relação aos pedidos feitos
                    user: User = User([], [], 0, 0)

                    if user_id in users:
                        currUser = users[user_id]
                        currUser.orders = currUser.orders + 1

                        if card_number not in currUser.cards_number:
                            currUser.cards_number.append(card_number)

                        if device_id not in currUser.devices_id:
                            currUser.devices_id.append(device_id)

                        if cbk:
                            if not currUser.cbk:
                                currUser.cbk = 1
                            else:
                                currUser.cbk = currUser.cbk + 1

                    else:
                        user.cards_number = [card_number]
                        user.devices_id = [device_id]
                        user.orders = 1
                        if cbk:
                            user.cbk = 1
                        currUser = user

    return rows, Indexes
