class Card():

    def __init__(self, cardID, name, image, rarity, color, side, level, cost, power, soul,
                 traits, triggers, flavor, text, effects):
        self.CardID = cardID
        self.Name = name
        self.Image = image
        self.Rarity = rarity
        self.Color = color
        self.Side = side
        self.Level = level
        self.Cost = cost
        self.Power = power
        self.Soul = soul
        self.Traits = traits
        self.Triggers = triggers
        self.Flavor = flavor
        self.Text = text
        self.Effects = effects

    def Duplicate(self):
        return Card(self.CardID, self.Name, self.Image, self.Rarity, self.Color, self.Side, self.Level, self.Cost,
                    self.Power, self.Soul, self.Traits, self.Triggers, self.Flavor, self.Text, self.Effects)

    def IsClimax(self):
        if 'Climax' in self.Side:
            return True
        else:
            return False

    def IsCharacter(self):
        if 'Character' in self.Side:
            return True
        else:
            return False

    def IsEvent(self):
        if 'Event' in self.Side:
            return True
        else:
            return False

