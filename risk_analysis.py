from models import Indexes, Card, User, Suspect, SuspectCard
from users_analysis import userAnalysis
from card_analysis import cardAnalysis


def riskAnalysis(data: list, indexes: Indexes, cards: list[Card], users: list[User]) -> tuple[list[Suspect], list[SuspectCard]]:
    averageTicket = float(data[0][len(data[0]) - 1])
    scores = {'veryLow': 10, 'low': 20,
              'medium': 35, 'high': 50, 'veryHigh': 75}

    suspectUsers = userAnalysis(users, scores, averageTicket)

    suspectCards = cardAnalysis(cards, scores)

    suspectUsers.sort(key=lambda x: x.score)
    suspectCards.sort(key=lambda x: x.score)

    return suspectUsers, suspectCards
