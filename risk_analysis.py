from models import Indexes, Card, User, Suspect, SuspectCard
from users_analysis import userAnalysis
from card_analysis import cardAnalysis


def riskAnalysis(rows: list, indexes: Indexes, cards: list[Card], users: list[User]) -> tuple[list[Suspect], list[SuspectCard], dict[int], dict[int]]:
    averageTicket = float(rows[0][indexes.average_ticket])
    scores = {'veryLow': 10, 'low': 20,
              'medium': 35, 'high': 50, 'veryHigh': 75}

    suspectUsers, suspectUsersDic = userAnalysis(users, scores, averageTicket)

    suspectCards, suspectCardsDic = cardAnalysis(cards, scores)

    # Order the suspects by score, from highest to lowest
    suspectUsers.sort(key=lambda x: x.score, reverse=True)
    suspectCards.sort(key=lambda x: x.score, reverse=True)

    return suspectUsers, suspectCards, suspectUsersDic, suspectCardsDic
