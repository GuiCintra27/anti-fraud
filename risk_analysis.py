class Titles:
    def __init__(self, transaction_id, merchant_id, user_id, card_number, transaction_date, Hour, transaction_amount, device_id, has_cbk):
        self.transaction_id = transaction_id
        self.merchant_id = merchant_id
        self.user_id = user_id
        self.card_number = card_number
        self.transaction_date = transaction_date
        self.Hour = Hour
        self.transaction_amount = transaction_amount
        self.device_id = device_id
        self.has_cbk = has_cbk


def riskAnalysis(data: list, Titles: Titles):
    print("Risk Analysis")
