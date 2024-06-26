from models import User, Suspect


def userAnalysis(users: list[User], scores: dict[str, int], averageTicket: float) -> tuple[list[Suspect], dict[int]]:
    suspects: list[Suspect] = []
    # Create a dictionary to store the score of each suspect and be more easy to access after
    suspectsDict: dict[int] = {}

    for id in users:
        user: User = users[id]
        suspect = Suspect(user_id=id, score=0, reasons=[])
        reasons: list[str] = []

        match len(user.cards_number):
            case 3:
                suspect.updateScore(scores['low'])

            case 4:
                suspect.updateScore(scores['medium'])

            case 5:
                suspect.updateScore(scores['high'])

            case n if n > 5:
                suspect.updateScore(scores['veryHigh'])

        match len(user.devices_id):
            case 3:
                suspect.updateScore(scores['medium'])

            case 4:
                suspect.updateScore(scores['high'])

            case n if n > 4:
                suspect.updateScore(scores['veryHigh'])

        match user.orders:
            case n if n > 3 and n <= 5:
                suspect.updateScore(scores['low'])

            case n if n > 5 and n <= 7:
                suspect.updateScore(scores['medium'])

            case n if n > 7:
                suspect.updateScore(scores['high'])

        match user.amount:
            case n if n >= averageTicket * 2 and n < averageTicket * 2.5:
                suspect.updateScore(scores['medium'])

            case n if n >= averageTicket * 2.5 and n < averageTicket * 3.5:
                suspect.updateScore(scores['high'])

            case n if n >= averageTicket * 3.5:
                suspect.updateScore(scores['veryHigh'])

        if len(user.cards_number) > 2:
            reasons.append('Cards')

        if len(user.devices_id) > 2:
            reasons.append('Devices')

        if user.cbk > 0:
            suspect.updateScore(100)
            reasons.append('CBK')

        if user.orders > 3:
            reasons.append('Orders')

        if user.amount >= averageTicket * 2:
            reasons.append('Amount')

        suspect.reasons = reasons

        if suspect.score > 0:
            if int(user.hour) < 6:
                suspect.updateScore(scores['low'])
                reasons.append('Hour')

        if suspect.score > 30:
            suspects.append(suspect)
            suspectsDict[suspect.user_id] = {'score': suspect.score}

    return suspects, suspectsDict
