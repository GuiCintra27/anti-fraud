from models import Card, SuspectCard


def cardAnalysis(cards: list[Card], scores: dict[str, int]) -> list[SuspectCard]:
    suspects: list[SuspectCard] = []

    for id in cards:
        card: Card = cards[id]
        suspect = SuspectCard(card_id=id, score=0, reasons=[])
        reasons: list[str] = []

        match len(card.users_id):
            case 3:
                suspect.updateScore(scores['medium'])

            case 4:
                suspect.updateScore(scores['high'])

            case n if n > 4:
                suspect.updateScore(scores['veryHigh'])

        match len(card.devices_id):
            case 3:
                suspect.updateScore(scores['medium'])

            case 4:
                suspect.updateScore(scores['high'])

            case n if n > 4:
                suspect.updateScore(scores['veryHigh'])

        if len(card.users_id) > 2:
            reasons.append('Cards')

        if len(card.devices_id) > 2:
            reasons.append('Devices')

        suspect.reasons = reasons
        if suspect.score > 0:
            suspects.append(suspect)

    return suspects
