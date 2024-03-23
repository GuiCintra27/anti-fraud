from datetime import datetime


class Indexes:
    transaction_id: str = None
    merchant_id: str = None
    user_id: str = None
    card_number: str = None
    transaction_date: str = None
    Hour: str = None
    transaction_amount: str = None
    device_id: str = None


class Card:
    def __init__(self, users_id: list[str], devices_id: list[str]):
        self.users_id: list[str] = users_id
        self.devices_id: list[str] = devices_id


def extractCsvData(file: str) -> tuple[list, Indexes]:
    # Dados das linhas da tabela
    rows = []
    # Lista de cartões e os dados aos quais estão vinculados (estou criando como dicionário para facilitar a busca e não ter que relizar mais um loop)
    cards = {}

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
                                Indexes.Hour = counter + 1
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
                    columns.insert(Indexes.Hour, hour)
                    rows.append(columns)

                    # Adicionar os dados do cartão na lista
                    userId = columns[Indexes.user_id]
                    deviceId = columns[Indexes.device_id]
                    cardNumber = columns[Indexes.card_number]

                    card = Card([], [])

                    # Verificar se o cartão ja existe e adicionar os dados, quantos usuários vinculados e quantos dispositivos
                    if cardNumber in cards:
                        currCard = cards[cardNumber]
                        if userId not in currCard.users_id:
                            cards[cardNumber].users_id.append(userId)

                        if deviceId not in currCard.devices_id:
                            cards[cardNumber].devices_id.append(deviceId)

                    else:
                        card.users_id = [userId]
                        card.devices_id = [deviceId]
                        cards[cardNumber] = card

    return rows, Indexes
