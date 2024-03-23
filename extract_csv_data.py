from datetime import datetime
from models import Indexes, Card, User


def extractCsvData(file: str) -> tuple[list, Indexes]:
    # Dados das linhas da tabela
    rows = []
    # Abaixo estou criando como dicionário para facilitar a busca e diminuir a complexidade de tempo
    # Lista de cartões e os dados aos quais estão vinculados
    cards = {}
    # Lista de usuários e os dados aos quais estão vinculados
    users = {}
    # Total de vendas
    totalAmount = 0

    with open(file) as f:
        for line in f:
            line = line.strip()  # Remove espaços em branco
            if line:
                columns = line.split(',')  # Divide a linha em colunas

                # Adiciona as posições das colunas à variável Indexes
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
                    # Não trabalhar com valores da tabela antes desta linha, pois as posições só se acertam após adicionar o horário nas colunas
                    # Converter data para hora e acrescentar na lista
                    hour = f"{datetime.fromisoformat(columns[Indexes.transaction_date]).hour}H"
                    columns.insert(Indexes.hour, hour)
                    rows.append(columns)

                    # Soma a venda ao valor total de vendas
                    totalAmount += float(columns[Indexes.transaction_amount])

                    user_id = columns[Indexes.user_id]
                    amount = columns[Indexes.transaction_amount]
                    device_id = columns[Indexes.device_id]
                    card_number = columns[Indexes.card_number]
                    cbk = columns[Indexes.has_cbk]

                    # Verifica os dados dos cartões, quantos usuários e dispositivos relacionados
                    card = Card([], [])

                    if card_number in cards:
                        currCard = cards[card_number]
                        currCard.update(user_id, device_id)

                    else:
                        card.insert(user_id, device_id)
                        cards[card_number] = card

                    # Verifica os dados de compra de cada cliente, quantos cartões, dispositivos, pedidos, chargebacks e total gasto no dia
                    user: User = User([], 0, [], 0, 1)

                    if user_id in users:
                        currUser = users[user_id]
                        currUser.update(card_number, amount, device_id, cbk)

                    else:
                        user.insert(card_number, amount, device_id, cbk)
                        users[user_id] = user

    # Ticket médio
    averageTicket = "%.2f" % round((totalAmount / len(rows)), 2)
    rows[0] = rows[0] + [averageTicket]

    return rows, Indexes
