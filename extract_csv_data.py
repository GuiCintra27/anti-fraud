from datetime import datetime
from models import Indexes, Card, User


def extractCsvData(file: str) -> tuple[list, Indexes, list[Card], list[User]]:
    # Table row data
    rows: list = []
    # Below I am creating it as a dictionary to facilitate the search and reduce time complexity
    # List of cards and the data they are linked to
    cards: list[Card] = {}
    # List of users and the data they are linked to
    users: list[User] = {}
    # Sales amount
    totalAmount: float = 0

    with open(file) as f:
        for line in f:
            line = line.strip()  # Remove whitespace
            if line:
                columns = line.split(',')  # Divide the row into columns

                # Adds column positions to the Indexes variable
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
                                Indexes.recommendation = counter + 1

                        counter += 1

                else:
                    # Do not work with table values before this line, as the positions are only adjusted after adding the time in the columns
                    # Convert date to time and add to list
                    hour = f"{datetime.fromisoformat(columns[Indexes.transaction_date]).hour}H"
                    columns.insert(Indexes.hour, hour)
                    rows.append(columns)

                    user_id = columns[Indexes.user_id]
                    amount = columns[Indexes.transaction_amount]
                    device_id = columns[Indexes.device_id]
                    card_number = columns[Indexes.card_number]
                    cbk = columns[Indexes.has_cbk]

                    # Add the sale to the total sales value
                    totalAmount += float(amount)

                    # Check card data, how many users and related devices
                    card: Card = Card(users_id=[], devices_id=[])

                    if card_number in cards:
                        currCard = cards[card_number]
                        currCard.update(user_id, device_id)

                    else:
                        card.insert(user_id, device_id)
                        cards[card_number] = card

                    # Checks each customer's purchase data, how many cards, devices, orders, chargebacks and total spent on the day
                    user: User = User(cards_number=[], amount=0,
                                      devices_id=[], cbk=0, orders=1, hour=int(hour.split('H')[0]))

                    if user_id in users:
                        currUser = users[user_id]
                        currUser.update(card_number, amount,
                                        device_id, cbk, int(hour.split('H')[0]))

                    else:
                        user.insert(card_number, amount, device_id, cbk)
                        users[user_id] = user

    # Calculate the average ticket
    averageTicket = "%.2f" % round((totalAmount / len(users)), 2)
    rows[0] = rows[0] + [averageTicket]
    # Update the index of the average ticket column
    Indexes.average_ticket = len(rows[0]) - 1

    return rows, Indexes, cards, users
