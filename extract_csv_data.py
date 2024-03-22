from datetime import datetime


class Indexes:
    transaction_id = None
    merchant_id = None
    user_id = None
    card_number = None
    transaction_date = None
    Hour = None
    transaction_amount = None
    device_id = None
    has_cbk = None


def extractCsvData(file: str) -> tuple[list, Indexes]:
    rows = []

    with open(file) as f:
        for line in f:
            line = line.strip()
            if line:
                columns = line.split(',')

                if Indexes.user_id == None:
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
                    hour = f"{datetime.fromisoformat(columns[Indexes.transaction_date]).hour}H"
                    columns.insert(Indexes.Hour, hour)
                    rows.append(columns)

    return rows, Indexes
