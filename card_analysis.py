from models import Card, SuspectCard


def cardAnalysis(cards: list[Card], scores: dict[str, int]) -> tuple[list[SuspectCard], dict[int]]:
    suspects: list[SuspectCard] = []
    # Create a dictionary to store the score of each suspect and be more easy to access after
    suspectsDict: dict[int] = {}

    for id in cards:
        card: Card = cards[id]
        suspect = SuspectCard(card_id=id, score=0, reasons=[])
        reasons: list[str] = []

        match len(card.users_id):
            case 3:
                suspect.updateScore(scores['medium'] + 20)

            case 4:
                suspect.updateScore(scores['high'] + 20)

            case n if n > 4:
                suspect.updateScore(scores['veryHigh'] + 25)

        if len(card.users_id) > 2:
            reasons.append('Users')

        suspect.reasons = reasons
        if suspect.score > 30:
            suspects.append(suspect)
            suspectsDict[suspect.card_id] = {'score': suspect.score}

    return suspects, suspectsDict
