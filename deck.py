from collections import defaultdict

class Deck():

    def __init__(self):
        self.Cards = []

    def Add(self, card):
        self.Cards.append(card)

    def RemoveCardByID(self, cardID):
        for card in self.Cards:
            if card.CardID == cardID:
                self.Cards.remove(card)
                return

    def GetCardCount(self):
        return len(self.Cards)

    def GetCardsAndCounts(self, sort_on):
        d = defaultdict(int)
        for card in self.Cards:
            d[card] += 1
        if sort_on == 'Count':
            return sorted(d.items(), lambda x, y: cmp(x[1], y[1]))
        return sorted(d.items(), lambda x, y: cmp(getattr(x[0], sort_on), getattr(y[0], sort_on)))

    def GetAttrsAndCounts(self, to_plot):
        d = defaultdict(int)
        for card in self.Cards:
            d[getattr(card, to_plot)] += 1
        return sorted(d.items())

    def GetGameCards(self):
        li = []
        for c in self.Cards:
            li.append(c)
        return li

