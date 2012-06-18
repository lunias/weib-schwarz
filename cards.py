import card

class Cards():

    def __init__(self):
        self.CardDict = {}
        self.CardCount = 0

        self.PopulateDict()

    def AddCard(self, card):
        self.CardDict[card.CardID] = card
        self.CardCount += 1

    def GetCardByID(self, card_id):
        return self.CardDict[card_id]

    def GetSortedValues(self):
        values = self.CardDict.values()
        values.sort(lambda x, y: cmp(x.Name, y.Name))
        return [value for value in values]

    def PopulateDict(self):
        #disgaea trial deck
        name   = 'Overlord Laharl and his Vassal Etna'
        image  = 'DG103'
        flavor = 'Prince, you\'re just a big softy! If that was me, I would\'ve wasted them all!'
        text   = ('[A] When the Battle Opponent of this becomes Reversed, if there are no '
                  'Climax Cards in your opponent\'s Waiting Room, you may choose a card in your '
                  'Waiting Room and put it in your Stock.')
        traits = ['Demon', 'Weapon']
        to_add = card.Card('DG/S02-103', name, image, 'TD', 'Green', 'Schwarz Character', 0, 0, 2500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Raspberyl & Sapphire All Ready for Gym'
        image  = 'DG104'
        flavor = 'Are there really demons that are this cute? That\'s too much for me !'
        text   = ('[C] If there are 4 or more Climax cards in your Waiting Room, this gains '
                '"[A] ENCORE [Discard a Character card from your hand to the Waiting Room]"')
        traits = ['Demon', 'Sports']
        to_add = card.Card('DG/S02-104', name, image, 'TD', 'Green', 'Schwarz Character', 2, 2, 8500, 2,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Laharl & Flonne'
        image  = 'DGT01'
        flavor = 'Laharl: That\'s right! I\'m the Overlord!'
        text   = ''
        traits = ['Demon', 'Angel']
        to_add = card.Card('DG/S02-T01', name, image, 'TD', 'Green', 'Schwarz Character', 0, 0, 3000, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Prinny Squad'
        image  = 'DGT02'
        flavor = 'I\'ve got a bad feeling about this, dood!'
        text   = ('[C] You may have as many copies of the card with the same name as this in '
                'your deck as you wish.\n[S] [Put a ::Prinny:: Character to the Waiting Room ]'
                'Choose 1 of your opponent\'s Front Row Characters. That Character gets -1000 Power for the turn.')
        traits = ['Prinny', 'None']
        to_add = card.Card('DG/S02-T02', name, image, 'TD', 'Green', 'Schwarz Character', 0, 0, 1500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Average Cleric'
        image  = 'DGT03'
        flavor = 'I am always beside you...'
        text   = ('[S] Brainstorm [(1)] Reveal the top 4 cards of your Library and put them '
                  'in your Waiting Room. For each Climax card revealed this way, choose 1 of your '
                  'Characters. That Character gains +2000 Power for the turn.')
        traits = ['God', 'Magic']
        to_add = card.Card('DG/S02-T03', name, image, 'TD', 'Green', 'Schwarz Character', 0, 0, 2000, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Genius Rune Knight'
        image  = 'DGT04'
        flavor = 'I can sense a demonic power from this evil room...'
        text   = ('[A] When this is placed from hand to the Stage, you may choose a Climax '
                  'card in your opponent\'s Waiting Room and return it to the Library. If you do '
                  'so, shuffle that Library, and choose 1 of your Characters. That Character gains '
                  '+3000 Power for the turn.')
        traits = ['Weapon', 'Magic']
        to_add = card.Card('DG/S02-T04', name, image, 'TD', 'Green', 'Schwarz Character', 0, 0, 2500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Universe Police Justice Flonne'
        image  = 'DGT05'
        flavor = '"Love & Peace!!" to your heart!'
        text   = ('[A] When this attacks, if "Assassin from Celestia" is in your Climax '
                  'Zone, then all your Characters gain +1000 Power for the turn. '
                  '\n[S] [Rest 1 of your Characters] This card gains +1000 Power for the turn.')
        traits = ['Angel', 'Police']
        to_add = card.Card('DG/S02-T05', name, image, 'TD', 'Green', 'Schwarz Character', 1, 0, 4000, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Good-for-Nothing Archer'
        image  = 'DGT06'
        flavor = 'Umm, my strong point is my vertical role. Shooting weak points is my hobby.'
        text   = ('[A] When this is placed from hand to the Stage, choose 1 of your '
                  'opponent\'s Characters. That Character gets -500 Power for the turn.')
        traits = ['Weapon', 'None']
        to_add = card.Card('DG/S02-T06', name, image, 'TD', 'Green', 'Schwarz Character', 1, 1, 4500, 1,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Etna & Flonne'
        image  = 'DGT07'
        flavor = 'Flonne, you aren\'t supposed to be tainted by the demonic side, are you?'
        text   = ('[S] [Counter] BACKUP 1500, Level 1 [Discard this card from hand to the '
                  'Waiting Room]')
        traits = ['Demon', 'Angel']
        to_add = card.Card('DG/S02-T07', name, image, 'TD', 'Green', 'Schwarz Character', 1, 0, 1500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Revival of the Bow'
        image  = 'DGT08'
        flavor = 'Finally... Finally returned!'
        text   = ('[Counter] Choose up to 5 non-Climax Cards in your Waiting Room and return '
                  'them to your Library. Shuffle your Library. If you returned 5 cards, choose 1 '
                  'Character in your opponent\'s Front Row. That Character gets -1500 Power for the '
                  'turn.')
        traits = ['None', 'None']
        to_add = card.Card('DG/S02-T08', name, image, 'TD', 'Green', 'Schwarz Event', 1, 0, 0, 0,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Assassin from Celestia'
        image  = 'DGT09'
        flavor = 'Nice to meet you, I\'m an assassin~'
        text   = ('[C] All your Characters gain +2 Soul.')
        traits = ['None', 'None']
        to_add = card.Card('DG/S02-T09', name, image, 'TD', 'Green', 'Schwarz Climax', 0, 0, 0, 0,
                           traits, ['Soul', 'Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Etna, the Overlord Assassin'
        image  = 'DGT10'
        flavor = ('I don\'t think it\'s love. If it\'s no good, I\'ll just '
                  'kill him.')
        text   = ('None')
        traits = ['Demon', 'Weapon']
        to_add = card.Card('DG/S02-T10', name, image, 'TD', 'Red', 'Schwarz Character', 0, 0, 3000, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Vyers, the Dark Adonis / Mid-Boss'
        image  = 'DGT11'
        flavor = ('Mi- Mi- Midboss!!?')
        text   = ('[C] ASSIST All your Characters in front of this card gain +500 Power. '
                  '\n[A] When this becomes Reversed while battling, you may return this to your '
                  'Library. If so, shuffle your Library.')
        traits = ['Demon', 'Will']
        to_add = card.Card('DG/S02-T11', name, image, 'TD', 'Red', 'Schwarz Character', 0, 0, 500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Invincible Robot Thursday'
        image  = 'DGT12'
        flavor = ('GORDON KEEPS STARING AT JENNIFER\'S THIGHS,  PERVERT!')
        text   = ('[C] All your other ::Hero:: Characters and Characters with "Protagonist" '
                  'in the name gain +500 Power. \n[S] [(2) Rest this] Choose 1 Character in your '
                  'Waiting Room and return it to your hand.')
        traits = ['Mecha', 'Hero']
        to_add = card.Card('DG/S02-T12', name, image, 'TD', 'Red', 'Schwarz Character', 0, 0, 500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Prince Laharl of the Netherworld'
        image  = 'DGT13'
        flavor = ('Prince Laharl, Successor of the Netherworld, that\'s me!')
        text   = ('[A] When this attacks, if "King of the Earth" is in your Climax Zone, you '
                  'may choose a card in your opponent\'s Waiting Room and put it on top of the '
                  'Library. \n[A] BOND/"Etna & Flonne" [(1)]')
        traits = ['Demon', 'Weapon']
        to_add = card.Card('DG/S02-T13', name, image, 'TD', 'Red', 'Schwarz Character', 1, 0, 3000, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Captain Gordon, Defender of Earth'
        image  = 'DGT14'
        flavor = ('Captain Gordon, Defender of Earth! I have arrived!!')
        text   = 'None'
        traits = ['Hero', 'Weapon']
        to_add = card.Card('DG/S02-T14', name, image, 'TD', 'Red', 'Schwarz Character', 1, 1, 6000, 1,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Demon Girl Etna, the Ultimate Beauty'
        image  = 'DGT15'
        flavor = ('A beautiful girl dances in the darkness of the devil realm, next time'
                  'on "Birth of Queen Etna"!')
        text   = 'None'
        traits = ['Demon', 'Weapon']
        to_add = card.Card('DG/S02-T15', name, image, 'TD', 'Red', 'Schwarz Character', 2, 2, 9000, 2,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = '"Beauty Baron" Mid-Boss'
        image  = 'DGT16'
        flavor = ('You\'ll regret treating me like a mid-boss!!')
        text   = ('[A] When this is placed from hand to Stage, if there are 5 or fewer cards '
                  'in your Library, return all cards in your Waiting Room to Library. If so, '
                  'shuffle that Library, and you may deal 1 damage to opponent. (Damage Cancel can '
                  'occur. \n[A] When this becomes Reversed while battling, you may return this to your '
                  'Library. If so, shuffle your Library.')
        traits = ['Demon', 'Will']
        to_add = card.Card('DG/S02-T16', name, image, 'TD', 'Red', 'Schwarz Character', 2, 1, 7500, 1,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Supreme Overlord Laharl'
        image  = 'DGT17'
        flavor = ('... Who are you, the reckless person who disturbs the sleep of Laharl?')
        text   = ('[A] When this is placed from hand to the Stage, you may put the top card '
                  'of your Clock in your Waiting Room. \n[S] [Send this to Memory] Choose a combination '
                  'of up to 2 ::Angel:: and/or ::Demon:: Characters in your Waiting Room and return them '
                  'to your hand.')
        traits = ['Demon', 'Weapon']
        to_add = card.Card('DG/S02-T17', name, image, 'TD', 'Red', 'Schwarz Character', 3, 2, 10000, 2,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'King of the Earth'
        image  = 'DGT18'
        flavor = ('I\'ll become the King of the Earth from now on.')
        text   = ('[C] All your Characters gain +2 Soul.')
        traits = ['None', 'None']
        to_add = card.Card('DG/S02-T18', name, image, 'TD', 'Red', 'Schwarz Climax', 0, 0, 0, 0,
                           traits, ['Soul', 'Soul'], flavor, text, None)
        self.AddCard(to_add)

        #evangelion booster
        name   = '"First Battle" Shinji'
        image  = 'EV001'
        flavor = ('I\'ll do it. I\'ll pilot it.')
        text   = ('[A] When this attacks, if "EVA-01\'s First Battle" is in the Climax Zone, '
                  'this gains +2 Soul for the turn. \n[A] ENCORE [Discard a Character card from '
                  'hand to the Waiting Room]')
        traits = ['Pilot', 'None']
        to_add = card.Card('EV/S12-001', name, image, 'RR', 'Yellow', 'Schwarz Character', 1, 1, 6000, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'EVA-01 (Awaken State 1)'
        image  = 'EV002'
        flavor = ('None')
        text   = ('[C] EXPERIENCE If sum of the Levels of the cards in your Level Zone is 4 '
                  'or more, this gains +1500 Power and the following ability: "[C] This cannot be '
                  'chosen as a target by an opponent\'s effect." \n[A] When this is placed from hand '
                  'to the Stage or placed via CHANGE to the Stage, draw up to 2 cards and discard a card '
                  'from hand to the Waiting Room.')
        traits = ['Mecha', 'Awaken']
        to_add = card.Card('EV/S12-002', name, image, 'RR', 'Yellow', 'Schwarz Character', 3, 2, 9500, 2,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Shinji, Bento Duty'
        image  = 'EV003'
        flavor = ('Sorry, Ayanami. It didn\'t fit your taste?')
        text   = ('[C] All your other Characters who have either "Asuka" and/or "Ayanami" in '
                  'the name gain +500 Power. \n[S] [Rest this] Choose 1 of your Characters whose name '
                  'contains "Asuka" or "Ayanami". That Character gains +500 Power and "Bento Box" for the turn.')
        traits = ['Pilot', 'Bento Box']
        to_add = card.Card('EV/S12-003', name, image, 'R', 'Yellow', 'Schwarz Character', 0, 0, 1000, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Pre-Mission Shinji'
        image  = 'EV004'
        flavor = ('We might die from this.')
        text   = ('[A] When this is placed from hand to the Stage, this gains +1500 Power for the turn.')
        traits = ['Pilot', 'None']
        to_add = card.Card('EV/S12-004', name, image, 'R', 'Yellow', 'Schwarz Character', 0, 0, 2500, 1,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Misato Katsuragi'
        image  = 'EV005'
        flavor = ('I want to become the cupid that brings Commander Ikari and Shinji-chan together.')
        text   = ('[C] EXPERIENCE During your turn, if the sum of Levels of cards in your Level Zone is 1 '
                  'or higher, this gains +1500 Power. \n[S] [Rest 1 of your ::Pilot:: Characters] This '
                  'gains +1000 Power for the turn.')
        traits = ['Animal', 'None']
        to_add = card.Card('EV/S12-005', name, image, 'R', 'Yellow', 'Schwarz Character', 1, 0, 4500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Kaworu on the Lunar Surface'
        image  = 'EV006'
        flavor = ('I will enjoy it when we meet, Shinji Ikari.')
        text   = ('[C] All your other ::Pilot:: Characters gain +500 Power. \n'
                  '[C] [Rest this] Choose 1 of your Characters who has "Shinji" in the name. That '
                  'Character gains +1000 Power for the turn.')
        traits = ['Puzzle', 'None']
        to_add = card.Card('EV/S12-006', name, image, 'R', 'Yellow', 'Schwarz Character', 1, 1, 4500, 1,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Misato, Entrusting the Future'
        image  = 'EV007'
        flavor = ('If Third Impact occurs now, humanity will become extinct.')
        text   = ('[C] EXPERIENCE If the sum of Levels of cards in your Level Zone is 3 or '
                  'higher, this gains +1 Soul. \n[A] [(1)] When "Future Entrusted" is placed to '
                  'your Climax Zone, if this is in the Front Row, reveal the top card of your Library. '
                  'If it is a Level 2 or lower Character, move to a Slot on the Stage. (If not, put it back)')
        traits = ['Animal', 'None']
        to_add = card.Card('EV/S12-007', name, image, 'R', 'Yellow', 'Schwarz Character', 2, 1, 7500, 1,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'PenPen'
        image  = 'EV008'
        flavor = ('Misato: "The name is PenPen."')
        text   = ('[A] BOND/"Misato Katsuragi" [(1)] \n'
                  '[S] [Rest this] Choose 1 of your Characters who has "Misato" in the name. That '
                  'Character gains +500 Power for the turn.')
        traits = ['Animal', 'None']
        to_add = card.Card('EV/S12-008', name, image, 'U', 'Yellow', 'Schwarz Character', 0, 0, 500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Kaworu Nagisa'
        image  = 'EV009'
        flavor = ('Nice to meet you, father.')
        text   = ('[C] All your other ::Puzzle:: Characters gain +500 Power. \n'
                  '[S] [(1) Rest this] Choose 1 of your ::Puzzle:: Characters. That Character '
                  'gains +1 Soul for the turn.')
        traits = ['Puzzle', 'None']
        to_add = card.Card('EV/S12-009', name, image, 'U', 'Yellow', 'Schwarz Character', 0, 0, 1500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Misato in the Living Room'
        image  = 'EV010'
        flavor = ('Bath, the laundry for life.')
        text   = ('[A] When this attacks, reveal the top card of your Library. If it\'s a '
                  'Character with either ::Animal:: or ::Pilot::, this gains +1500 Power for the '
                  'turn. (Put the revealed card back where it was)')
        traits = ['Animal', 'None']
        to_add = card.Card('EV/S12-010', name, image, 'U', 'Yellow', 'Schwarz Character', 0, 0, 2500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Shinji, Fired!?'
        image  = 'EV011'
        flavor = ('Shinji: "?" Asuka: "You\'re fired"')
        text   = ('[C] ASSIST All your Characters in front of this gain +1000 Power during your turn.')
        traits = ['Pilot', 'None']
        to_add = card.Card('EV/S12-011', name, image, 'U', 'Yellow', 'Schwarz Character', 1, 0, 3500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = '"EVA-01 Pilot" Shinji'
        image  = 'EV012'
        flavor = ('Misato-san!')
        text   = ('[A] CHANGE [(2) Discard a card from the hand to the Waiting Room, put '
                  'this in the Waiting Room] At the beginning of your Climax Phase, you may pay '
                  'cost. If so, choose a "EVA-01 (Awaken State 1)" in your Waiting Room and put it '
                  'in the Slot this was in.')
        traits = ['None', 'None']
        to_add = card.Card('EV/S12-012', name, image, 'U', 'Yellow', 'Schwarz Character', 2, 1, 8000, 1,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Misato in the Picture'
        image  = 'EV013'
        flavor = ('None')
        text   = ('[C] This gains +1000 Power during your turn.')
        traits = ['Animal', 'None']
        to_add = card.Card('EV/S12-013', name, image, 'U', 'Yellow', 'Schwarz Character', 0, 0, 2500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Shinji on the Rooftop'
        image  = 'EV014'
        flavor = ('None')
        text   = ('[S] [Rest 1 of your ::Pilot:: Characters] This gains +1000 Power for the turn.')
        traits = ['Pilot', 'Music']
        to_add = card.Card('EV/S12-014', name, image, 'C', 'Yellow', 'Schwarz Character', 0, 0, 2500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Shinji, Meeting'
        image  = 'EV015'
        flavor = ('Meeting is impossible, it seems.')
        text   = ('None')
        traits = ['Pilot', 'None']
        to_add = card.Card('EV/S12-015', name, image, 'C', 'Yellow', 'Schwarz Character', 0, 0, 3000, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Evangelion Test EVA-01'
        image  = 'EV016'
        flavor = ('Misato: "All according to the operation. Good job, Shinji"')
        text   = ('[C] This cannot Side Attack. \n'
                  '[A] ENCORE [Discard a Character card from hand to the Waiting Room]')
        traits = ['Mecha', 'Weapon']
        to_add = card.Card('EV/S12-016', name, image, 'C', 'Yellow', 'Schwarz Character', 1, 0, 5500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Misato, Emergency Situation'
        image  = 'EV017'
        flavor = ('Medic, hurry!')
        text   = ('None')
        traits = ['Animal', 'None']
        to_add = card.Card('EV/S12-017', name, image, 'C', 'Yellow', 'Schwarz Character', 1, 1, 7000, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Misato, Driver'
        image  = 'EV018'
        flavor = ('Sorry to keep you waiting.')
        text   = ('[S] [Counter] BACKUP 3000, Level 2 [(1) Discard this card from hand to '
                  'the Waiting Room]')
        traits = ['Animal', 'Glasses']
        to_add = card.Card('EV/S12-018', name, image, 'C', 'Yellow', 'Schwarz Character', 2, 1, 2500, 1,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'EVA-01, G-Type Equipment'
        image  = 'EV019'
        flavor = ('Misato "Operation Yashima, commence!"')
        text   = ('[A] [(2)] When this attacks, if "Operation Yashima" is in the Climax '
                  'Zone, you may pay cost. If you do, choose 1 Character whose Level is 2 or lower '
                  'in your Opponent\'s Front Row and choose 1 Character whose Level is 2 or lower '
                  'in your Opponent\'s Back Row. Return those Characters to the hand.')
        traits = ['Mecha', 'Weapon']
        to_add = card.Card('EV/S12-019', name, image, 'C', 'Yellow', 'Schwarz Character', 2, 2, 8500, 2,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Shinji Ikari'
        image  = 'EV020'
        flavor = ('I need to do something here. Misato-san!')
        text   = ('None')
        traits = ['Pilot', 'None']
        to_add = card.Card('EV/S12-020', name, image, 'C', 'Yellow', 'Schwarz Character', 2, 2, 9000, 2,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Angel\'s Assault'
        image  = 'EV021'
        flavor = ('Aoba: "High energy level detected inside the target!" Misato: "What!?"')
        text   = ('Choose 1 of your Opponent\'s Character whose Level is 1 or lower. Return '
                  'that Character to the hand. ')
        traits = ['None', 'None']
        to_add = card.Card('EV/S12-021', name, image, 'U', 'Yellow', 'Schwarz Event', 1, 1, 0, 0,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Second Impact'
        image  = 'EV022'
        flavor = ('Kaji: "...Second Impact"')
        text   = ('Put all Characters whose Level is 3 or lower in the Stock in any order '
                  'you choose. (This effect affects both your and your Opponent\'s Characters. This '
                  'effect does not target.)')
        traits = ['None', 'None']
        to_add = card.Card('EV/S12-022', name, image, 'U', 'Yellow', 'Schwarz Event', 3, 7, 0, 0,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'EVA-01\'s First Battle'
        image  = 'EV023'
        flavor = ('Woah!!')
        text   = ('[A] When this is placed from hand to the Climax Zone, draw a card, and '
                  'choose 1 of your Characters. That Character gains +2000 Power and +1 Soul for '
                  'the turn.')
        traits = ['None', 'None']
        to_add = card.Card('EV/S12-023', name, image, 'CR', 'Yellow', 'Schwarz Climax', 0, 0, 0, 0,
                           traits, ['Soul', 'Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Operation Yashima'
        image  = 'EV024'
        flavor = ('Misato: "Positron sniping ready!"')
        text   = ('[A] When this is placed from hand to the Climax Zone, put the top card in '
                  'your Library in the Stock Zone, and all your Characters gain +1 Soul for the '
                  'turn.')
        traits = ['None', 'None']
        to_add = card.Card('EV/S12-024', name, image, 'CC', 'Yellow', 'Schwarz Climax', 0, 0, 0, 0,
                           traits, ['Soul', 'Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Future Entrusted'
        image  = 'EV025'
        flavor = ('No reason. It\'s just because it\'s your destiny.')
        text   = ('[C] All your Characters gain +1000 Power and +1 Soul.')
        traits = ['None', 'None']
        to_add = card.Card('EV/S12-025', name, image, 'CC', 'Yellow', 'Schwarz Climax', 0, 0, 0, 0,
                           traits, ['Soul', 'Bounce'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Mari Illustrious Makinami'
        image  = 'EV026'
        flavor = ('Just keep it to yourself, puppy of NERV.')
        text   = ('[C] EXPERIENCE If the sum of Levels of cards in your Level Zone is 2 or '
                  'higher, this gains +1000 Power. \n[A] When this attacks, if "Encounter on '
                  'the Rooftop" is in the Climax Zone, you may put the top card of your Library to your Stock.')
        traits = ['Pilot', 'Glasses']
        to_add = card.Card('EV/S12-026', name, image, 'RR', 'Green', 'Schwarz Character', 1, 1, 6000, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Beast Mari'
        image  = 'EV027'
        flavor = ('Gaahhhhhh...')
        text   = ('[C] If you have 2 or more other ::Pilot:: Characters, this gains +1000 Power. '
                  '\n[C] EXPERIENCE If the sum of Levels of cards in your Level Zone is 3 or higher, '
                  'this gains "[A] ENCORE [Discard a Character card from hand to the Waiting '
                  'Room]".')
        traits = ['Pilot', 'Glasses']
        to_add = card.Card('EV/S12-027', name, image, 'RR', 'Green', 'Schwarz Character', 2, 1, 7500, 1,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Mari, Looking at the Sky'
        image  = 'EV028'
        flavor = ('When your own goal gets adults involved, you become diffident.')
        text   = ('[A] When this attacks, choose 1 of your Characters with either ::Pilot:: '
                  'or ::Mecha::. That Character gains +500 Power for the turn.\n'
                  '[A] BOND/"Evangelion Locally Specified EVA-05" [(1)] ')
        traits = ['Pilot', 'Glasses']
        to_add = card.Card('EV/S12-028', name, image, 'R', 'Green', 'Schwarz Character', 0, 0, 500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Mari, Secret Entry'
        image  = 'EV029'
        flavor = ('You are interesting')
        text   = ('[A] When this is placed from hand to the Stage, choose 1 of your '
                  '::Pilot:: Characters. That Character gains +1500 Power for the turn.')
        traits = ['Pilot', 'Glasses']
        to_add = card.Card('EV/S12-029', name, image, 'R', 'Green', 'Schwarz Character', 0, 0, 2000, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Maya Ibuki'
        image  = 'EV030'
        flavor = ('It\'s no use!! It\'s completely uncontrollable!!')
        text   = ('[C] EXPERIENCE If the sum of Levels of cards in your Level Zone is 2 or '
                  'higher, this gains +1000 Power.\n[A] ENCORE [Discard a Character card from '
                  'hand to the Waiting Room]')
        traits = ['None', 'None']
        to_add = card.Card('EV/S12-030', name, image, 'R', 'Green', 'Schwarz Character', 1, 0, 4500, 1,
                           traits, [], flavor, text, None)
        self.AddCard(to_add)

        name   = 'EVA-02, Beast State 2'
        image  = 'EV031'
        flavor = ('Mari: "The Beast!"')
        text   = ('[A] When this attacks, if "The Last Card" is in the Climax Zone, all your '
                  'Characters gain +2000 Power for the turn.\n[A] ENCORE [Discard a Character '
                  'card from hand to the Waiting Room]')
        traits = ['Mecha', 'Animal']
        to_add = card.Card('EV/S12-031', name, image, 'R', 'Green', 'Schwarz Character', 2, 2, 7500, 2,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)

        name   = 'Mari, Hard Fighting'
        image  = 'EV032'
        flavor = ('Gahhhhh!!')
        text   = ('[A] When this is placed from hand to the Stage, you may put the top card '
                  'in your Clock in your Waiting Room.\n'
                  '[A] [(3) Put a Level 1 or higher ::Mecha:: Character from your Stage to the '
                  'Waiting Room] When this attacks, if "Adults\' Convenience And Own Goal" is in '
                  'the Climax Zone, you may pay cost. If so, choose 1 of your Opponent\'s Level 2 '
                  'or lower Character. Put it in the Clock.')
        traits = ['Pilot', 'Glasses']
        to_add = card.Card('EV/S12-032', name, image, 'R', 'Green', 'Schwarz Character', 3, 2, 10000, 2,
                           traits, ['Soul'], flavor, text, None)
        self.AddCard(to_add)


