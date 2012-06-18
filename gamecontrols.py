import wx, random, sys, os
import engine, network, packets
from deck import Deck

CHAT_GAME = 0
CHAT_PLAYER = 1
CHAT_OPPONENT = 2
CHAT_CONSOLE = 3

POS_FIELD = 0
POS_HAND = 1
POS_DECK = 2
POS_CENTERSTAGE1 = 3
POS_CENTERSTAGE2 = 4
POS_CENTERSTAGE3 = 5
POS_BACKSTAGE1 = 6
POS_BACKSTAGE2 = 7
POS_CLIMAX = 8
POS_STOCK = 9
POS_LEVEL = 10
POS_CLOCK = 11
POS_MEMORY = 12
POS_WAITINGROOM = 13

POS_OPP_FIELD = 14
POS_OPP_HAND = 15
POS_OPP_DECK = 16
POS_OPP_CENTERSTAGE1 = 17
POS_OPP_CENTERSTAGE2 = 18
POS_OPP_CENTERSTAGE3 = 19
POS_OPP_BACKSTAGE1 = 20
POS_OPP_BACKSTAGE2 = 21
POS_OPP_CLIMAX = 22
POS_OPP_STOCK = 23
POS_OPP_LEVEL = 24
POS_OPP_CLOCK = 25
POS_OPP_MEMORY = 26
POS_OPP_WAITINGROOM = 27

FACE_DOWN = 0
FACE_UP = 1

CARD_VERTICAL = 0
CARD_HORIZONTAL = 1

class GameObject(wx.Window):
    def __init__(self, parent, pos, texture, size=-1):
        self._texture = texture
        if size == -1:
            size = (self._texture.GetWidth(), self._texture.GetHeight())
        wx.Window.__init__(self, parent=parent, id=-1, pos=pos, size=size)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self._texture, 0, 0, True)

    def SetTexture(self, texture):
        self._texture = texture
        self.Refresh()

class GamePanel(wx.Panel):

    def __init__(self, parent, engine):
        wx.Panel.__init__(self, parent)

        self.SetBackgroundColour(wx.Colour(205, 201, 201))

        self._parent = parent
        self._engine = engine
        self._nick = 'Lunias'
        self._opponentnick = ''
        self._levelingup = False
        self._opplevelingup = False

        #Play Areas
        self._centerstage = []
        self._backstage = []
        self._climax = []
        self._stock = []
        self._level = []
        self._clock = []
        self._memory = []
        self._waitingroom = []
        self._deck = []
        self._hand = []

        #Other Vars
        self._cardsize = wx.Size(60, 88)
        self._origdeck = None
        self._opponentorigdeck = None
        self._serial = 0
        self._opponentserial = 0
        self._activeplayer = 0
        self._playerid = -1
        self._currentphase = 6
        self._mulliganing = True
        self._oppmulliganing = True
        self._clocked = False

        #Opponent Vars
        self._oppcenterstage = []
        self._oppbackstage = []
        self._oppclimax = []
        self._oppstock = []
        self._opplevel = []
        self._oppclock = []
        self._oppmemory = []
        self._oppwaitingroom = []
        self._oppdeck = []
        self._opphand = []

        #Field Control
        self._fieldctrl = FieldControl(self)
        self._opponentfieldctrl = OpponentFieldControl(self)

        #Deck Control
        self._deckctrl = DeckControl(self._fieldctrl, (622,107), self._engine.GetImageSkin('Deck'))
        self._deckctrl.Bind(wx.EVT_LEFT_DCLICK, self.OnDeckDClick)
        self._deckctrl.Bind(wx.EVT_RIGHT_UP, self.OnDeckRClick)
        self._opponentdeckctrl = OpponentDeckControl(self._opponentfieldctrl, (15, 105),
                                                     self._engine.GetImageSkin('OppDeck'))

        #Waiting Room Control
        self._waitingroomctrl = WaitingRoomControl(self._fieldctrl, (622,207),
                                                   self._engine.GetImageSkin('CardBlank'), self)
        self._waitingroomctrl.Bind(wx.EVT_LEFT_UP, self.OnWaitingRoomLClick)
        self._opponentwaitingroomctrl = OpponentWaitingRoomControl(self._opponentfieldctrl, (15, 5),
                                                                   self._engine.GetImageSkin('CardBlank'), self)
        self._opponentwaitingroomctrl.Bind(wx.EVT_LEFT_UP, self.OnOpponentWaitingRoomLClick)

        #Hand Control
        self._handctrl = HandControl(self)
        self.RefreshHand()

        #Opponent Hand Control
        self._opponenthandctrl = OpponentHandControl(self)
        self.RefreshOpponentHand()

        #Card Visualization Controls
        self._cardimagectrl = wx.StaticBitmap(self, -1, size=(290,420), pos=(720,2))
        self._carddescriptionctrl = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT,
                                                size=(254,420), pos=(1020,2))

        #Console Controls
        self._consolectrl = ConsoleCtrl(self)
        self._consolectrl.SetFont(wx.Font(pointSize=8, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_NORMAL,
                                          weight=wx.FONTWEIGHT_NORMAL, faceName="Tahoma"))
        self._consolectrl.SetFocus()
        self._messagectrl = wx.richtext.RichTextCtrl(self, pos=(710,430), size=(560,110),
                                                     style=wx.richtext.RE_MULTILINE|wx.richtext.RE_READONLY)
        self._messagectrl.BeginFont(wx.Font(pointSize=12, family=wx.FONTFAMILY_DEFAULT,
                                            style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_NORMAL, faceName="Tahoma"))

        #Phase Controls
        self._standphasectrl = StandPhaseControl(self)
        self._drawphasectrl = DrawPhaseControl(self)
        self._clockphasectrl = ClockPhaseControl(self)
        self._mainphasectrl = MainPhaseControl(self)
        self._climaxphasectrl = ClimaxPhaseControl(self)
        self._attackphasectrl = AttackPhaseControl(self)
        self._endphasectrl = EndPhaseControl(self)

        #List Controls
        self._decklistctrl = DeckListControl(self)
        self._opponentdecklistctrl = OpponentDeckListControl(self)
        self._waitingroomlistctrl = WaitingRoomListControl(self)
        self._opponentwaitingroomlistctrl = OpponentWaitingRoomListControl(self)

        #Trigger Controls
        self._triggerctrl = TriggerControl(self._parent)
        self._triggerctrl.Bind(wx.EVT_LEFT_UP, self.OnTrigger)

        #Create Card Controls From Deck
        self.UseDeck(self._engine.Deck)
        self._consolectrl.SetFocus()

    def ClearGame(self):
        self._centerstage = []
        self._backstage = []
        self._climax = []
        self._stock = []
        self._level = []
        self._clock = []
        self._memory = []
        self._waitingroom = []
        self._deck = []
        self._hand = []

    def ClearPhases(self):
        self._standphasectrl._sel = False
        self._standphasectrl.Hide()
        self._standphasectrl.Show()
        self._drawphasectrl._sel = False
        self._drawphasectrl.Hide()
        self._drawphasectrl.Show()
        self._clockphasectrl._sel = False
        self._clockphasectrl.Hide()
        self._clockphasectrl.Show()
        self._mainphasectrl._sel = False
        self._mainphasectrl.Hide()
        self._mainphasectrl.Show()
        self._climaxphasectrl._sel = False
        self._climaxphasectrl.Hide()
        self._climaxphasectrl.Show()
        self._attackphasectrl._sel = False
        self._attackphasectrl.Hide()
        self._attackphasectrl.Show()
        self._endphasectrl._sel = False
        self._endphasectrl.Hide()
        self._endphasectrl.Show()

    def UseDeck(self, deck):
        self._origdeck = deck
        self.ClearGame()
        for card in self._origdeck.GetGameCards():
            cc = CardControl(self._decklistctrl, card.Duplicate(), self._engine, self,
                             self.NewCardSerial(), cpos=POS_DECK)
            self.AddCardToBottom(self._deck, cc)
        self.RefreshDeck()
        self.RefreshHand()

    def Shuffle(self):
        random.shuffle(self._deck)
        self.RefreshDeck()
        self.WriteShufflePacket()

    def OnDeckDClick(self, event):
        self.OnDeckDraw()

    def OnDeckRClick(self, event):
        return

    def OnDeckDraw(self, reveal=0):
        if len(self._deck) < 1 :
            return
        c = self.RemoveCardFromTop(self._deck)
        c.SetCardState(POS_HAND)
        self.AddCardToBottom(self._hand, c)
        c.Reparent(self._handctrl)
        self.RefreshHand()
        self.RefreshDeck()
        self.WritePacket(packets.DrawPacket(reveal))

    def OnOpponentDeckDraw(self, reveal=0):
        c = self.RemoveCardFromTop(self._oppdeck)
        c.SetCardState(POS_OPP_HAND, face=FACE_DOWN)
        self.AddCardToBottom(self._opphand, c)
        c.Reparent(self._opponenthandctrl)
        self.RefreshOpponentHand()
        self.RefreshOpponentDeck()

    def OnTrigger(self, event=None):
        if self._triggerctrl.IsShown():
            self._triggerctrl.EndModal(0)
        else:
            if len(self._deck) > 0:
                self._triggerctrl.CardButton.SetBitmapLabel(self._engine.GetImageBigCard(self._deck[0]._card))
            self._triggerctrl.ShowModal()

    def OnWaitingRoomLClick(self, event=None):
        if self._waitingroomlistctrl.IsShown():
            self._waitingroomlistctrl.Hide()
        else:
            self._waitingroomlistctrl.Scroll.Scroll(0, 0)
            self._waitingroomlistctrl.Show()

    def OnOpponentWaitingRoomLClick(self, event=None):
        if self._opponentwaitingroomlistctrl.IsShown():
            self._opponentwaitingroomlistctrl.Hide()
        else:
            self._opponentwaitingroomlistctrl.Scroll.Scroll(0, 0)
            self._opponentwaitingroomlistctrl.Show()

    def RefreshDeck(self):
        self._deckctrl.UpdateCardTooltip(self._deck)

    def RefreshOpponentDeck(self):
        self._opponentdeckctrl.UpdateCardTooltip(self._oppdeck)

    def RefreshWaitingRoom(self):
        self._waitingroomctrl.UpdateCardTooltip(self._waitingroom)
        if len(self._waitingroom) == 0:
            return
        y_pos = 0
        x_pos = 0
        y_move = 90
        x_move = 60
        count = 0
        self._waitingroomlistctrl.Scroll.Scroll(0, 0)
        for c in self._waitingroom:
            count += 1
            #c.RefreshTexture()
            c.SetPosition((x_pos, y_pos))
            c.Reparent(self._waitingroomlistctrl.Scroll)
            #c.Hide()
            #c.Show()
            x_pos += x_move
            if count % 10 == 0:
                count = 0
                x_pos = 0
                y_pos += y_move
        self._waitingroomlistctrl.Scroll.SetScrollbars(0, 90, 0, 5)

    def RefreshOpponentWaitingRoom(self):
        self._opponentwaitingroomctrl.UpdateCardTooltip(self._oppwaitingroom)
        if len(self._oppwaitingroom) == 0:
            return
        y_pos = 0
        x_pos = 0
        y_move = 90
        x_move = 60
        count = 0
        self._opponentwaitingroomlistctrl.Scroll.Scroll(0, 0)
        for c in self._oppwaitingroom:
            count += 1
            c.SetPosition((x_pos, y_pos))
            c.Reparent(self._opponentwaitingroomlistctrl.Scroll)
            x_pos += x_move
            if count % 10 == 0:
                count = 0
                x_pos = 0
                y_pos += y_move
        self._opponentwaitingroomlistctrl.Scroll.SetScrollbars(0, 90, 0, 5)

    def RefreshHand(self):
        l = self._hand
        n = len(l)
        if n < 1:
            return
        card_width = self.GetCardSize().GetWidth() + 2
        self_width = self._handctrl.GetSize().GetWidth()
        self_mid = self_width/2
        x_pos = 0
        if n > 8:
            card_width = self_width/n
        elif n%2 == 0:
            x_pos = self_mid - (card_width*(n/2))
        else:
            x_pos = self_mid - ((card_width*(n/2)) + card_width/2)
        for c in l:
            c.SetPosition((x_pos,0))
            x_pos += card_width
            c.Hide()
            c.Show()
            if sys.platform == "win32":
                c.Lower()

    def RefreshOpponentHand(self):
        l = self._opphand
        n = len(l)
        if n < 1:
            return
        card_width = self.GetCardSize().GetWidth() + 2
        self_width = self._opponenthandctrl.GetSize().GetWidth()
        self_mid = self_width/2
        x_pos = 0
        if n > 8:
            card_width = self_width/n
        elif n%2 == 0:
            x_pos = self_mid - (card_width*(n/2))
        else:
            x_pos = self_mid - ((card_width*(n/2)) + card_width/2)
        for c in l:
            c.SetPosition((x_pos,0))
            x_pos += card_width
            c.Hide()
            c.Show()
            if sys.platform == "win32":
                c.Lower()

    def RefreshCardInfo(self, name, bmp, desc):
        self._cardimagectrl.SetBitmap(bmp)
        self._carddescriptionctrl.SetValue(desc)

    def GetCardSize(self):
        return self._cardsize

    def AddCardToTop(self, l, c):
        l.insert(0, c)

    def AddCardToBottom(self, l, c):
        l.append(c)

    def RemoveCardFromTop(self, l):
        return l.pop(0)

    def RemoveCardFromBottom(self, l):
        return l.pop(len(l)-1)

    def MoveCard(self, source, dest, card):
        self.MoveCardToTop(source, dest, card)

    def MoveCardToTop(self, src, dest, card):
        src.remove(card)
        dest.insert(0, card)

    def MoveCardToBottom(self, src, dest, card):
        src.remove(card)
        dest.append(card)

    def NewCardSerial(self):
        s = str(self._serial)
        self._serial += 1
        return s

    def NewOpponentCardSerial(self):
        s = str(self._opponentserial)
        self._opponentserial += 1
        return s

    def GetCardFromSerial(self, serial):
        for c in self._centerstage:
            if c.GetSerial() == serial:
                return c
        for c in self._backstage:
            if c.GetSerial() == serial:
                return c
        for c in self._climax:
            if c.GetSerial() == serial:
                return c
        for c in self._stock:
            if c.GetSerial() == serial:
                return c
        for c in self._level:
            if c.GetSerial() == serial:
                return c
        for c in self._clock:
            if c.GetSerial() == serial:
                return c
        for c in self._memory:
            if c.GetSerial() == serial:
                return c
        for c in self._waitingroom:
            if c.GetSerial() == serial:
                return c
        for c in self._hand:
            if c.GetSerial() == serial:
                return c
        for c in self._deck:
            if c.GetSerial() == serial:
                return c
        return -1

    def GetOpponentCardFromSerial(self, serial):
        for c in self._oppcenterstage:
            if c.GetSerial() == serial:
                return c
        for c in self._oppbackstage:
            if c.GetSerial() == serial:
                return c
        for c in self._oppclimax:
            if c.GetSerial() == serial:
                return c
        for c in self._oppstock:
            if c.GetSerial() == serial:
                return c
        for c in self._opplevel:
            if c.GetSerial() == serial:
                return c
        for c in self._oppclock:
            if c.GetSerial() == serial:
                return c
        for c in self._oppmemory:
            if c.GetSerial() == serial:
                return c
        for c in self._oppwaitingroom:
            if c.GetSerial() == serial:
                return c
        for c in self._opphand:
            if c.GetSerial() == serial:
                return c
        for c in self._oppdeck:
            if c.GetSerial() == serial:
                return c
        return -1

    def OnCardDropOnField(self, x, y, data):
        c = self.GetCardFromSerial(data)
        self._currentcard = c
        if self.Hit(x, y, wx.Rect(0,0,self._fieldctrl.GetSize().GetWidth(),self._fieldctrl.GetSize().GetHeight())):
            self._currentcard = (c, x, y)
            if c.GetCardPosition() == POS_HAND:
                if not self._levelingup and self._activeplayer == self._playerid: self.OnHandPlay()
            elif (c.GetCardPosition() == POS_CENTERSTAGE1 or c.GetCardPosition() == POS_CENTERSTAGE2 or
                  c.GetCardPosition() == POS_CENTERSTAGE3 or c.GetCardPosition() == POS_BACKSTAGE1 or
                  c.GetCardPosition() == POS_BACKSTAGE2):
                if not self._levelingup and self._activeplayer == self._playerid: self.OnSwapCharacters()
            elif c.GetCardPosition() == POS_CLOCK and self._levelingup:
                self.OnClockToLevel()

        self._consolectrl.SetFocus()

    def OnHandPlay(self, arg=None):
        card = self._currentcard[0]
        x = self._currentcard[1]
        y = self._currentcard[2]

        xy_loc, field_loc = self.PositionCard(card, x, y)

        if card.IsEvent() and not field_loc == POS_CLOCK:
            if not self._currentphase == 3:
                return
            card.SetCardState(POS_WAITINGROOM)
            self.MoveCard(self._hand, self._waitingroom, card)
            card.Reparent(self._waitingroomctrl)
            self.RefreshHand()
            self.RefreshWaitingRoom()
            self.WriteMoveCardPacket(card, POS_OPP_WAITINGROOM, 0, 0, 0)
            self.WriteGameMessage('played ' + card.GetCardName() + '.', CHAT_PLAYER)
            return

        if xy_loc == -1 or field_loc == POS_LEVEL:
            return

        if field_loc == POS_CENTERSTAGE1 or field_loc == POS_CENTERSTAGE2 or field_loc == POS_CENTERSTAGE3:
            if not self._currentphase == 3:
                return
            for c in self._centerstage:
                if c.GetCardPosition() == field_loc:
                    self.MoveCard(self._centerstage, self._waitingroom, c)
                    c.SetCardState(POS_WAITINGROOM)
                    c.Reparent(self._waitingroomlistctrl)
                    self.RefreshWaitingRoom()
                    self.WriteMoveCardPacket(c, POS_OPP_WAITINGROOM, 0, 0, 0)
                    break
            card.SetCardState(field_loc)
            self.MoveCard(self._hand, self._centerstage, card)
        elif field_loc == POS_BACKSTAGE1 or field_loc == POS_BACKSTAGE2:
            if not self._currentphase == 3:
                return
            for c in self._backstage:
                if c.GetCardPosition() == field_loc:
                    self.MoveCard(self._backstage, self._waitingroom, c)
                    c.SetCardState(POS_WAITINGROOM)
                    c.Reparent(self._waitingroomlistctrl)
                    self.RefreshWaitingRoom()
                    self.WriteMoveCardPacket(c, POS_OPP_WAITINGROOM, 0, 0, 0)
                    break
            card.SetCardState(field_loc)
            self.MoveCard(self._hand, self._backstage, card)
        elif field_loc == POS_CLIMAX:
            if not self._currentphase == 4:
                return
            card.SetCardState(field_loc, CARD_HORIZONTAL)
            self.MoveCard(self._hand, self._climax, card)
        elif field_loc == POS_CLOCK:
            if not self._currentphase == 2 or self._clocked:
                return
            card.SetCardState(field_loc)
            self.MoveCard(self._hand, self._clock, card)
            self.OnDeckDraw()
            self.OnDeckDraw()
            self._clocked = True

        card.Reparent(self._fieldctrl)
        self.RefreshHand()
        card.SetPosition(xy_loc)
        if sys.platform == "win32":
            card.Lower()
        card.Hide()
        card.Show()
        self.WriteMoveCardPacket(card, field_loc+14, 0, xy_loc.x, xy_loc.y)
        if not field_loc == POS_CLOCK:
            self.WriteGameMessage('placed ' + card.GetCardName() +
                                  ' on the field.', CHAT_PLAYER)
        else:
            self.WriteGameMessage('clocked ' + card.GetCardName() +
                                  ' (total damage ' + str(len(self._clock)) + ')', CHAT_PLAYER)
            self.DoLevelCheck()

    def DoLevelCheck(self):
        if len(self._clock) < 7:
            self._levelingup = False
        else:
            self._levelingup = True

    def OnOpponentHandPlay(self, arg=None):
        card = self._opponentcurrentcard[0]
        dest = self._opponentcurrentcard[1]
        x = self._opponentcurrentcard[2]
        y = self._opponentcurrentcard[3]

        if dest == POS_OPP_CENTERSTAGE1 or dest == POS_OPP_CENTERSTAGE2 or dest == POS_OPP_CENTERSTAGE3:
            card.SetCardState(dest)
            self.MoveCard(self._opphand, self._oppcenterstage, card)
        elif dest == POS_OPP_BACKSTAGE1 or dest == POS_OPP_BACKSTAGE2:
            card.SetCardState(dest)
            self.MoveCard(self._opphand, self._oppbackstage, card)
        elif dest == POS_OPP_CLIMAX:
            card.SetCardState(dest, CARD_HORIZONTAL)
            self.MoveCard(self._opphand, self._oppclimax, card)
        elif dest == POS_OPP_CLOCK:
            card.SetCardState(dest)
            self.MoveCard(self._opphand, self._oppclock, card)

        card.Reparent(self._opponentfieldctrl)
        self.RefreshOpponentHand()
        self.RefreshOpponentWaitingRoom()
        card.SetPosition(self.PositionOpponentCard(card, dest))
        if sys.platform == "win32":
            card.Lower()
        card.Hide()
        card.Show()
        if not dest == POS_OPP_CLOCK:
            self.WriteGameMessage('placed ' + card.GetCardName() +
                                  ' on the field.', CHAT_OPPONENT)
        else:
            self.WriteGameMessage('clocked ' + card.GetCardName() +
                                  ' (total damage ' + str(len(self._oppclock)) + ')', CHAT_OPPONENT)

    def OnSwapCharacters(self, arg=None):
        card = self._currentcard[0]
        x = self._currentcard[1]
        y = self._currentcard[2]

        if not self._currentphase == 3:
            return

        xy_loc, field_loc = self.PositionCard(card, x, y)
        if xy_loc == -1 or field_loc == POS_CLOCK or field_loc == POS_CLIMAX or field_loc == POS_LEVEL:
            return

        if field_loc == POS_CENTERSTAGE1 or field_loc == POS_CENTERSTAGE2 or field_loc == POS_CENTERSTAGE3:
            for c in self._centerstage:
                if c.GetCardPosition() == field_loc:
                    if card.GetCardPosition() == POS_BACKSTAGE1 or card.GetCardPosition() == POS_BACKSTAGE2:
                        self.MoveCard(self._centerstage, self._backstage, c)
                    c.SetCardState(card.GetCardPosition(), c.GetCardMode())
                    my_pos = self.PositionCard(c, card.GetPositionTuple()[0]+22, card.GetPositionTuple()[1]+25)[0]
                    c.SetPosition(my_pos)
                    if sys.platform == "win32":
                        c.Lower()
                    c.Hide()
                    c.Show()
                    break
            if card.GetCardPosition() == POS_BACKSTAGE1 or card.GetCardPosition() == POS_BACKSTAGE2:
                self.MoveCard(self._backstage, self._centerstage, card)
            card.SetCardState(field_loc, card.GetCardMode())

        elif field_loc == POS_BACKSTAGE1 or field_loc == POS_BACKSTAGE2:
            for c in self._backstage:
                if c.GetCardPosition() == field_loc:
                    if (card.GetCardPosition() == POS_CENTERSTAGE1 or card.GetCardPosition() == POS_CENTERSTAGE2 or
                        card.GetCardPosition() == POS_CENTERSTAGE3):
                        self.MoveCard(self._backstage, self._centerstage, c)
                    c.SetCardState(card.GetCardPosition(), c.GetCardMode())
                    my_pos = self.PositionCard(c, card.GetPositionTuple()[0]+22, card.GetPositionTuple()[1]+25)[0]
                    c.SetPosition(my_pos)
                    if sys.platform == "win32":
                        c.Lower()
                    c.Hide()
                    c.Show()
                    break
            if (card.GetCardPosition() == POS_CENTERSTAGE1 or card.GetCardPosition() == POS_CENTERSTAGE2 or
                card.GetCardPosition() == POS_CENTERSTAGE3):
                self.MoveCard(self._centerstage, self._backstage, card)
            card.SetCardState(field_loc, card.GetCardMode())

        card.SetPosition(xy_loc)
        if sys.platform == "win32":
            card.Lower()
        card.Hide()
        card.Show()
        self.WriteMoveCardPacket(card, field_loc+14, 0, xy_loc.x, xy_loc.y)

    def OnOpponentSwapCharacters(self, arg=None):
        card = self._opponentcurrentcard[0]
        dest = self._opponentcurrentcard[1]
        x = self._opponentcurrentcard[2]
        y = self._opponentcurrentcard[3]

        if dest == POS_OPP_CENTERSTAGE1 or dest == POS_OPP_CENTERSTAGE2 or dest == POS_OPP_CENTERSTAGE3:
            for c in self._oppcenterstage:
                if c.GetCardPosition() == dest:
                    if card.GetCardPosition() == POS_OPP_BACKSTAGE1 or card.GetCardPosition() == POS_OPP_BACKSTAGE2:
                        self.MoveCard(self._oppcenterstage, self._oppbackstage, c)
                    c.SetCardState(card.GetCardPosition(), c.GetCardMode())
                    my_pos = self.PositionOpponentCard(c, card.GetCardPosition())
                    c.SetPosition(my_pos)
                    if sys.platform == "win32":
                        card.Lower()
                    card.Hide()
                    card.Show()
                    break
            if card.GetCardPosition() == POS_OPP_BACKSTAGE1 or card.GetCardPosition() == POS_OPP_BACKSTAGE2:
                self.MoveCard(self._oppbackstage, self._oppcenterstage, card)
            card.SetCardState(dest, card.GetCardMode())

        elif dest == POS_OPP_BACKSTAGE1 or dest == POS_OPP_BACKSTAGE2:
            for c in self._oppbackstage:
                if c.GetCardPosition() == dest:
                    if (card.GetCardPosition() == POS_OPP_CENTERSTAGE1 or
                        card.GetCardPosition() == POS_OPP_CENTERSTAGE2 or
                        card.GetCardPosition() == POS_OPP_CENTERSTAGE3):
                        self.MoveCard(self._oppbackstage, self._oppcenterstage, c)
                    c.SetCardState(card.GetCardPosition(), c.GetCardMode())
                    my_pos = self.PositionOpponentCard(c, card.GetCardPosition())
                    c.SetPosition(my_pos)
                    if sys.platform == "win32":
                        card.Lower()
                    card.Hide()
                    card.Show()
                    break
            if (card.GetCardPosition() == POS_OPP_CENTERSTAGE1 or card.GetCardPosition() == POS_OPP_CENTERSTAGE2 or
                card.GetCardPosition() == POS_OPP_CENTERSTAGE3):
                self.MoveCard(self._oppcenterstage, self._oppbackstage, card)
            card.SetCardState(dest, card.GetCardMode())

        card.SetPosition(self.PositionOpponentCard(card, dest))
        if sys.platform == "win32":
            card.Lower()
        card.Hide()
        card.Show()

    def OnOpponentHandToWaitingRoom(self, arg=None):
        card = self._opponentcurrentcard
        self.MoveCard(self._opphand, self._oppwaitingroom, card)
        card.SetCardState(POS_OPP_WAITINGROOM)
        card.Reparent(self._opponentwaitingroomlistctrl)
        self.RefreshOpponentWaitingRoom()
        self.RefreshOpponentHand()
        if not self._oppmulliganing:
            self.WriteGameMessage('played ' + card.GetCardName() + '.', CHAT_OPPONENT)

    def OnOpponentStageToWaitingRoom(self, arg=None):
        card = self._opponentcurrentcard
        if arg == POS_OPP_CENTERSTAGE1 or arg == POS_OPP_CENTERSTAGE2 or arg == POS_OPP_CENTERSTAGE3:
            self.MoveCard(self._oppcenterstage, self._oppwaitingroom, card)
        elif arg == POS_OPP_BACKSTAGE1 or arg == POS_OPP_BACKSTAGE2:
            self.MoveCard(self._oppbackstage, self._oppwaitingroom, card)
        card.SetCardState(POS_OPP_WAITINGROOM)
        card.Reparent(self._opponentwaitingroomlistctrl)
        self.RefreshOpponentWaitingRoom()
        self.RefreshOpponentHand()

    def OnClimaxToWaitingRoom(self, arg=None):
        card = self._currentcard
        self.MoveCard(self._climax, self._waitingroom, card)
        card.SetCardState(POS_WAITINGROOM)
        card.Reparent(self._waitingroomlistctrl)
        self.RefreshWaitingRoom()
        self.WriteMoveCardPacket(card, POS_OPP_WAITINGROOM, 0, 0, 0)

    def OnOpponentClimaxToWaitingRoom(self, arg=None):
        card = self._opponentcurrentcard
        self.MoveCard(self._oppclimax, self._oppwaitingroom, card)
        card.SetCardState(POS_OPP_WAITINGROOM)
        card.Reparent(self._opponentwaitingroomlistctrl)
        self.RefreshOpponentWaitingRoom()

    def OnClockToLevel(self, arg=None):
        card = self._currentcard[0]
        x = self._currentcard[1]
        y = self._currentcard[2]

        xy_loc, field_loc = self.PositionCard(card, x, y)

        if xy_loc == -1:
            return

        if field_loc == POS_LEVEL:
            card.SetCardState(field_loc)
            self.MoveCard(self._clock, self._level, card)
        else:
            return

        card.SetPosition(xy_loc)
        if sys.platform == "win32":
            card.Lower()
        card.Hide()
        card.Show()
        self.WriteMoveCardPacket(card, field_loc+14, 0, xy_loc.x, xy_loc.y)

        for i in range(6):
            self._clock[0].SetCardState(POS_WAITINGROOM)
            self._clock[0].Reparent(self._waitingroomlistctrl)
            self._waitingroom.insert(0, self._clock.pop(0))

        self.RefreshWaitingRoom()

        self.DoLevelCheck()

    def OnOpponentClockToLevel(self, arg=None):
        card = self._opponentcurrentcard[0]
        dest = self._opponentcurrentcard[1]
        x = self._opponentcurrentcard[2]
        y = self._opponentcurrentcard[3]

        card.SetCardState(dest)
        self.MoveCard(self._oppclock, self._opplevel, card)

        card.SetPosition(self.PositionOpponentCard(card, dest))
        if sys.platform == "win32":
            card.Lower()
        card.Hide()
        card.Show()

        for i in range(6):
            self._oppclock[0].SetCardState(POS_OPP_WAITINGROOM)
            self._oppclock[0].Reparent(self._opponentwaitingroomlistctrl)
            self._oppwaitingroom.insert(0, self._oppclock.pop(0))

        self.RefreshOpponentWaitingRoom()

    def OnClose(self):
        self.WriteDisconnectPacket()
        self._engine.Network.Close()
        return True

    def OnCardPopup(self, c):
        pos = c.GetCardPosition()
        if pos == POS_CENTERSTAGE1 or pos == POS_CENTERSTAGE2 or pos == POS_CENTERSTAGE3:
            if not c.GetCardMode() == CARD_HORIZONTAL and self._currentphase == 5:
                if self._activeplayer == self._playerid: self.OnCardCenterStagePopup(c)
            elif self._currentphase == 3:
                if self._activeplayer == self._playerid: self.OnCardMainPhasePopup(c)
        elif pos == POS_BACKSTAGE1 or pos == POS_BACKSTAGE2:
            if self._currentphase == 3 and self._activeplayer == self._playerid:
                self.OnCardMainPhasePopup(c)
        elif pos == POS_HAND:
            self.OnCardHandPopup(c)

    def OnCardCenterStagePopup(self, c):
        menu = wx.Menu()
        item = wx.MenuItem(menu, -1, 'Front Attack')
        item.SetBitmap(self._engine.GetImageSkin('Attack'))
        menu.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.OnCardFieldAttack, item)
        item = wx.MenuItem(menu, -1, '  Side Attack')
        item.SetBitmap(self._engine.GetImageSkin('SideAttack'))
        self.Bind(wx.EVT_MENU, self.OnCardFieldSideAttack, item)
        menu.AppendItem(item)
        self._currentcard = c
        self.PopupMenu(menu)

    def OnCardMainPhasePopup(self, c):
        menu = wx.Menu()
        item = wx.MenuItem(menu, -1, 'Startup Ability')
        item.SetBitmap(self._engine.GetImageSkin('Activate'))
        #self.Bind(wx.EVT_MENU, self.OnCardFieldStartup, item)
        menu.AppendItem(item)
        self._currentcard = c
        self.PopupMenu(menu)

    def OnCardHandPopup(self, c):
        if self._mulliganing:
            menu = wx.Menu()
            item = wx.MenuItem(menu, -1, 'To Waiting Room')
            item.SetBitmap(self._engine.GetImageSkin('Towaiting'))
            self.Bind(wx.EVT_MENU, self.OnCardHandToWaitingRoom, item)
            menu.AppendItem(item)
            item = wx.MenuItem(menu, -1, 'Done Mulliganing')
            item.SetBitmap(self._engine.GetImageSkin('Luck'))
            self.Bind(wx.EVT_MENU, self.OnDoneMulliganing, item)
            menu.AppendItem(item)
            self._currentcard = c
            c.PopupMenu(menu)

    def OnCardHandToWaitingRoom(self, arg=None):
        card = self._currentcard
        self.WriteMoveCardPacket(card, POS_OPP_WAITINGROOM)
        self.MoveCard(self._hand, self._waitingroom, card)
        card.SetCardState(POS_WAITINGROOM)
        card.Reparent(self._waitingroomlistctrl)
        self.RefreshWaitingRoom()
        self.RefreshHand()

    def OnDoneMulliganing(self, arg=None):
        for i in range(len(self._hand), 5):
            self.OnDeckDraw()
        self.WriteDoneMulliganingPacket()
        self.WriteGameMessage('is done mulliganing.', CHAT_PLAYER)
        self._mulliganing = False

    def OnCardFieldAttack(self, event=None):
        card = self._currentcard
        self.WriteFlipCardPacket(card, 0)
        card.Horizontal()
        card.RefreshTexture()
        card.SetPosition(self.PositionCard(card, card.GetPositionTuple()[0]+22, card.GetPositionTuple()[1]+25)[0])
        card.Hide()
        card.Show()
        self.OnTrigger()
        self.WriteChatPacket('attacks with ' + card.GetCardName() + '.')
        self.WriteChatMessage('attacks with ' + card.GetCardName() + '.', CHAT_PLAYER)

    def OnCardFieldSideAttack(self, event=None):
        card = self._currentcard
        self.WriteFlipCardPacket(card, 0)
        card.Horizontal()
        card.RefreshTexture()
        card.SetPosition(self.PositionCard(card, card.GetPositionTuple()[0]+22, card.GetPositionTuple()[1]+25)[0])
        card.Hide()
        card.Show()
        self.WriteChatPacket('side attacks with ' + card.GetCardName())
        self.WriteChatMessage('side attacks with ' + card.GetCardName(), CHAT_PLAYER)

    def OnCardFieldVertical(self, event=None):
        card = self._currentcard
        self.WriteFlipCardPacket(card, 1)
        card.Vertical()
        card.RefreshTexture()
        card.SetPosition(self.PositionCard(card, card.GetPositionTuple()[0]+22, card.GetPositionTuple()[1]+25)[0])
        card.Hide()
        card.Show()

    def OnOpponentCardFieldHorizontal(self, event=None):
        card = self._opponentcurrentcard
        card.Horizontal()
        card.RefreshTexture()
        card.SetPosition(self.PositionOpponentCard(card, card.GetCardPosition()))
        card.Hide()
        card.Show()

    def OnOpponentCardFieldVertical(self, event=None):
        card = self._opponentcurrentcard
        card.Vertical()
        card.RefreshTexture()
        card.SetPosition(self.PositionOpponentCard(card, card.GetCardPosition()))
        card.Hide()
        card.Show()

    def Hit(self, x1, y1, r):
        x2 = r.GetX()
        y2 = r.GetY()
        x3 = r.GetX() + r.GetWidth()
        y3 = r.GetY() + r.GetHeight()
        if x1 >= x2 and x1 <= x3 and y1 >= y2 and y1 <= y3:
            return True
        else:
            return False

    def PositionCard(self, card, x, y):
        #CENTER STAGE 1, 2, 3
        if self.Hit(x, y, wx.Rect(267, 7, 60, 88)) and card.IsCharacter():
            x, y = 266, 7
            if card.IsHorizontal():
                x -= 12
                y += 15
            field_pos = POS_CENTERSTAGE1
        elif self.Hit(x, y, wx.Rect(371, 7, 60, 88)) and card.IsCharacter():
            x, y = 370, 7
            if card.IsHorizontal():
                x -= 12
                y += 15
            field_pos = POS_CENTERSTAGE2
        elif self.Hit(x, y, wx.Rect(471, 7, 60, 88)) and card.IsCharacter():
            x, y = 470, 7
            if card.IsHorizontal():
                x -= 12
                y += 15
            field_pos = POS_CENTERSTAGE3
        #BACK STAGE 1, 2
        elif self.Hit(x, y, wx.Rect(304, 104, 60, 88)) and card.IsCharacter():
            x, y = 304, 104
            field_pos = POS_BACKSTAGE1
            if card.IsHorizontal():
                x -= 12
                y += 15
        elif self.Hit(x, y, wx.Rect(436, 104, 60, 88)) and card.IsCharacter():
            x, y = 436, 104
            field_pos = POS_BACKSTAGE2
            if card.IsHorizontal():
                x -= 12
                y += 15
        #CLIMAX
        elif self.Hit(x, y, wx.Rect(107, 7, 88, 60)) and card.IsClimax():
            x, y = 107, 7
            field_pos = POS_CLIMAX
        #CLOCK
        elif self.Hit(x, y, wx.Rect(200, 200, 395, 100)):
            offset = len(self._clock) * 30
            x, y = 226+offset, 209
            field_pos = POS_CLOCK
        #LEVEL
        elif self.Hit(x, y, wx.Rect(102, 102, 88, 188)):
            offset = len(self._level) * 30
            x, y = 120, 115+offset
            field_pos = POS_LEVEL
        else:
            return -1, -1
        return wx.Point(x, y), field_pos

    def PositionOpponentCard(self, card, dest):
        if dest == POS_OPP_CENTERSTAGE3:
            x, y = 168, 203
            if card.IsHorizontal():
                x -= 12
                y += 15
        elif dest == POS_OPP_CENTERSTAGE2:
            x, y = 268, 203
            if card.IsHorizontal():
                x -= 12
                y += 15
        elif dest == POS_OPP_CENTERSTAGE1:
            x, y = 372, 203
            if card.IsHorizontal():
                x -= 12
                y += 15
        elif dest == POS_OPP_BACKSTAGE2:
            x, y = 203, 107
            if card.IsHorizontal():
                x -= 12
                y += 15
        elif dest == POS_OPP_BACKSTAGE1:
            x, y = 335, 107
            if card.IsHorizontal():
                x -= 12
                y += 15
        elif dest == POS_OPP_CLIMAX:
            x, y = 505, 230
        elif dest == POS_OPP_CLOCK:
            offset = len(self._oppclock) * 30 + 20
            x, y = 465-offset, 3
        elif dest == POS_OPP_LEVEL:
            offset = len(self._opplevel) * 30
            x, y = 520, 120-offset
        else:
            return wx.Point(1, 1)
        return wx.Point(x, y)


    #CONSOLE FUNCTIONS
    def ProcessMessage(self, m):
        self.WriteChatPacket(m)
        self.WriteChatMessage(m, CHAT_PLAYER)

    def WriteChatMessage(self, msg, w):
        self._messagectrl.SetInsertionPointEnd()
        self._messagectrl.Newline()
        if w == CHAT_PLAYER:
            self._messagectrl.BeginTextColour(wx.BLUE)
            self._messagectrl.WriteText(self._nick+': ')
            self._messagectrl.EndTextColour()
        elif w == CHAT_OPPONENT:
            self._messagectrl.BeginTextColour(wx.RED)
            self._messagectrl.WriteText(self._opponentnick+': ')
            self._messagectrl.EndTextColour()

        self._messagectrl.BeginTextColour(wx.BLACK)
        self._messagectrl.WriteText(msg)
        self._messagectrl.EndTextColour()

        while self._messagectrl.ScrollLines(10):
            pass
        self._messagectrl.SetInsertionPoint(0)

    def WriteGameMessage(self, msg, s):
        self._messagectrl.SetInsertionPointEnd()
        self._messagectrl.Newline()
        self._messagectrl.BeginTextColour(wx.GREEN)
        self._messagectrl.WriteText('Game: ')
        self._messagectrl.EndTextColour()
        if s == CHAT_GAME:
            self._messagectrl.BeginTextColour(wx.BLACK)
            self._messagectrl.WriteText(msg)
            self._messagectrl.EndTextColour()
        elif s == CHAT_PLAYER:
            self._messagectrl.BeginTextColour(wx.BLUE)
            self._messagectrl.WriteText(self._nick)
            self._messagectrl.EndTextColour()
            self._messagectrl.BeginTextColour(wx.BLACK)
            self._messagectrl.WriteText(' ' + msg)
            self._messagectrl.EndTextColour()
        elif s == CHAT_OPPONENT:
            self._messagectrl.BeginTextColour(wx.RED)
            self._messagectrl.WriteText(self._opponentnick)
            self._messagectrl.EndTextColour()
            self._messagectrl.BeginTextColour(wx.BLACK)
            self._messagectrl.WriteText(' ' + msg)
            self._messagectrl.EndTextColour()
        elif s == CHAT_CONSOLE:
            self._messagectrl.BeginTextColour(wx.BLACK)
            self._messagectrl.WriteText(msg)
            self._messagectrl.EndTextColour()
        while self._messagectrl.ScrollLines(10):
            pass
        self._messagectrl.SetInsertionPoint(0)

    #Packets
    def WritePacket(self, packet):
        if self._engine.Network.GetState() == network.ID_CONNECTED:
            try:
                self._engine.Network.Write(packet.Build())
            except:
                self.OnDisconnectPacket()

    def WriteChatPacket(self, m):
        self.WritePacket(packets.ChatPacket(m))

    def WriteDeckPacket(self):
        self.WritePacket(packets.DeckPacket(self._origdeck.GetGameCards()))

    def WriteShufflePacket(self):
        self.WritePacket(packets.ShufflePacket(self._deck))

    def WriteMoveCardPacket(self, card, dest, dest2=0, x=0, y=0):
        self.WritePacket(packets.CardMovePacket(card.GetSerial(), dest, dest2, x, y))

    def WriteFlipCardPacket(self, card, sta):
        self.WritePacket(packets.CardFlipPacket(card.GetSerial(), sta))

    def WritePhasePacket(self, phase):
        self.WritePacket(packets.PhasePacket(phase))

    def WriteFlipCoinPacket(self, h):
        self.WritePacket(packets.FlipCoinPacket(h))

    def WriteDoneMulliganingPacket(self):
        self.WritePacket(packets.DoneMulliganingPacket(False))

    def WriteDisconnectPacket(self):
        self.WritePacket(packets.DisconnectPacket())

    #Packet Events
    def OnConnectPacket(self, event):
        self.Parent.Show()
        self._opponentnick = event.data.ReadString()
        self._opponentversion = event.data.ReadString()
        self._playerid = event.data.ReadInt()
        self.WriteGameMessage('Connected with: ' + self._opponentnick + ' (' + self._opponentversion + ')', CHAT_GAME)
        if self._playerid == 1:
            head = random.randint(0, 1)
            self.WriteFlipCoinPacket(head)
            if head:
                self._activeplayer = 1
                self.WriteGameMessage('flipped a coin and won the flip.', CHAT_PLAYER)
            else:
                self._activeplayer = 2
                self.WriteGameMessage('flipped a coin and lost the flip.', CHAT_PLAYER)
        self.WriteDeckPacket()

    def OnChatPacket(self, event):
        self.WriteChatMessage('' + event.data.ReadString(), CHAT_OPPONENT)

    def OnDeckPacket(self, event):
        reader = event.data
        cards = []
        while 1:
            try:
                c = self._engine.FindCardByCardID(reader.ReadString())
            except:
                break
            cards.append(c)
        self._opponentorigdeck = Deck()
        for c in cards:
            self._opponentorigdeck.Add(c)
        deck = self._opponentorigdeck.GetGameCards()
        for c in deck:
            g = OpponentCardControl(self._opponentdecklistctrl, c.Duplicate(), self._engine,
                                    self, self.NewOpponentCardSerial(), cpos=POS_OPP_DECK)
            self.AddCardToBottom(self._oppdeck, g)
        self.RefreshOpponentDeck()
        self.Shuffle()
        for i in range(0, 5):
            self.OnDeckDraw()

    def OnDrawPacket(self, event):
        reader = event.data
        self.OnOpponentDeckDraw(reader.ReadBool())

    def OnShufflePacket(self, event):
        reader = event.data
        l = []
        while 1:
            try:
                l.append(self.GetOpponentCardFromSerial(reader.ReadString()))
            except:
               break
        self._oppdeck = l
        self.RefreshOpponentDeck()
        self.WriteGameMessage('shuffled their deck.', CHAT_OPPONENT)

    def OnCardMovePacket(self, event):
        reader = event.data
        card = self.GetOpponentCardFromSerial(reader.ReadString())
        dest = reader.ReadInt()
        self._opponentcurrentcard = card
        pos = card.GetCardPosition()
        if pos == POS_OPP_HAND:
            if (dest == POS_OPP_CENTERSTAGE1 or dest == POS_OPP_CENTERSTAGE2 or dest == POS_OPP_CENTERSTAGE3 or
                dest == POS_OPP_BACKSTAGE1 or dest == POS_OPP_BACKSTAGE2 or dest == POS_OPP_CLIMAX or
                dest == POS_OPP_CLOCK):
                dest2 = reader.ReadInt()
                x = reader.ReadInt()
                y = reader.ReadInt()
                self._opponentcurrentcard = [card, dest, x, y]
                if dest2 == 0:
                    self.OnOpponentHandPlay()
            elif dest == POS_OPP_WAITINGROOM:
                self.OnOpponentHandToWaitingRoom()
        elif (pos == POS_OPP_CENTERSTAGE1 or pos == POS_OPP_CENTERSTAGE2 or pos == POS_OPP_CENTERSTAGE3 or
              pos == POS_OPP_BACKSTAGE1 or pos == POS_OPP_BACKSTAGE2):
            if (dest == POS_OPP_CENTERSTAGE1 or dest == POS_OPP_CENTERSTAGE2 or dest == POS_OPP_CENTERSTAGE3 or
                dest == POS_OPP_BACKSTAGE1 or dest == POS_OPP_BACKSTAGE2):
                dest2 = reader.ReadInt()
                x = reader.ReadInt()
                y = reader.ReadInt()
                self._opponentcurrentcard = [card, dest, x, y]
                if dest2 == 0:
                    self.OnOpponentSwapCharacters()
            if dest == POS_OPP_WAITINGROOM:
                self.OnOpponentStageToWaitingRoom(pos)
        elif pos == POS_OPP_CLOCK:
            if dest == POS_OPP_LEVEL:
                dest2 = reader.ReadInt()
                x = reader.ReadInt()
                y = reader.ReadInt()
                self._opponentcurrentcard = [card, dest, x, y]
                if dest2 == 0:
                    self.OnOpponentClockToLevel()
        elif pos == POS_OPP_CLIMAX:
            if dest == POS_OPP_WAITINGROOM:
                self.OnOpponentClimaxToWaitingRoom(pos)


    def OnCardFlipPacket(self, event):
        reader = event.data
        card = self.GetOpponentCardFromSerial(reader.ReadString())
        self._opponentcurrentcard = card
        state = reader.ReadInt()
        pos = card.GetCardPosition()
        if state == 0:
            self.OnOpponentCardFieldHorizontal()
        if state == 1:
            self.OnOpponentCardFieldVertical()

    def OnPhasePacket(self, event):
        phase = event.data.ReadInt()
        if phase == 0:
            self._standphasectrl.SelectPhase()
            self.WriteGameMessage('entered Stand Phase.', CHAT_OPPONENT)
        elif phase == 1:
            self._drawphasectrl.SelectPhase()
            self.WriteGameMessage('entered Draw Phase.', CHAT_OPPONENT)
        elif phase == 2:
            self._clockphasectrl.SelectPhase()
            self.WriteGameMessage('entered Clock Phase.', CHAT_OPPONENT)
        elif phase == 3:
            self._mainphasectrl.SelectPhase()
            self.WriteGameMessage('entered Main Phase.', CHAT_OPPONENT)
        elif phase == 4:
            self._climaxphasectrl.SelectPhase()
            self.WriteGameMessage('entered Climax Phase.', CHAT_OPPONENT)
        elif phase == 5:
            self._attackphasectrl.SelectPhase()
            self.WriteGameMessage('entered Attack Phase.', CHAT_OPPONENT)
        elif phase == 6:
            self._endphasectrl.SelectPhase()
            self._activeplayer = (self._activeplayer % 2) + 1
            self.WriteGameMessage('ended turn.', CHAT_OPPONENT)

    def OnFlipCoinPacket(self, event):
        reader = event.data
        head = reader.ReadBool()
        if head:
            self._activeplayer = 1
            self.WriteGameMessage('flipped a coin and won the flip.', CHAT_OPPONENT)
        else:
            self._activeplayer = 2
            self.WriteGameMessage('flipped a coin and lost the flip.', CHAT_OPPONENT)

    def OnDoneMulliganingPacket(self, event):
        self._oppmulliganing = event.data.ReadBool()
        self.WriteGameMessage('is done mulliganing.', CHAT_OPPONENT)

    def OnDisconnectPacket(self, event=None):
        self.WriteGameMessage('disconnected.', CHAT_OPPONENT)
        self._engine.Network.Close()

class FieldControl(wx.Panel, wx.TextDropTarget):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, pos=(0,375), size=(700,300))
        self.SetDropTarget(FieldDropTarget(parent))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self._background = parent._engine.GetImageSkin('Field')

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self._background, 0, 0)

class FieldDropTarget(wx.TextDropTarget):

    def __init__(self, game):
        wx.TextDropTarget.__init__(self)
        self._game = game

    def OnDropText(self, x, y, data):
        self._game.OnCardDropOnField(x, y, data)

class OpponentFieldControl(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, pos=(0,41), size=(700,300))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self._background = parent._engine.GetImageSkin('OpponentField')

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self._background, 0, 0)

class StandPhaseControl(GameObject):

    def __init__(self, parent):
        self._game = parent
        GameObject.__init__(self, parent, (178+80,341), self._game._engine.GetImageSkin('Phase'))
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self._sel = False
        self._opp = False

    def SelectPhase(self):
        self._game._currentphase = 0
        self._game.ClearPhases()
        self._sel = True
        self._opp = True
        self.Hide()
        self.Show()

    def IsSelected(self):
        return self._sel

    def OnLeftUp(self, event=None):
        if self._game._activeplayer == self._game._playerid and self._game._currentphase+1 == 7:
            if self._game._oppmulliganing:
                self._game.WriteGameMessage('Waiting on opponent to finish mulliganing.', CHAT_GAME)
                return
            elif self._game._mulliganing:
                self._game.WriteGameMessage('Please finish mulliganing.', CHAT_GAME)
                return
            self._game._currentphase = 0
            self._game.WritePhasePacket(0)

            for c in self._game._centerstage:
                self._game._currentcard = c
                self._game.OnCardFieldVertical()
            for c in self._game._backstage:
                self._game._currentcard = c
                self._game.OnCardFieldVertical()

            self._game.ClearPhases()
            self._sel = True
            self._opp = False
            self.Hide()
            self.Show()
            self._game.WriteGameMessage('entered Stand Phase.', CHAT_PLAYER)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self._texture, 0, 0, True)
        dc.SetFont(wx.Font(pointSize=10,family=wx.FONTFAMILY_DEFAULT,style=wx.FONTSTYLE_NORMAL,weight=wx.FONTWEIGHT_NORMAL,
                           faceName="Tahoma"))
        if self._sel:
            if self._opp:
                dc.SetTextForeground(wx.RED)
            else:
                dc.SetTextForeground(wx.CYAN)
        else:
            dc.SetTextForeground(wx.WHITE)

        dc.DrawBitmap(self._texture, 0, 0, True)
        dc.DrawText("Stand", 15, 10)

class DrawPhaseControl(GameObject):

    def __init__(self, parent):
        self._game = parent
        GameObject.__init__(self, parent, (241+80,341), self._game._engine.GetImageSkin('Phase'))
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self._sel = False
        self._opp = False

    def SelectPhase(self):
        self._game._currentphase = 1
        self._game.ClearPhases()
        self._sel = True
        self._opp = True
        self.Hide()
        self.Show()

    def IsSelected(self):
        return self._sel

    def OnLeftUp(self, event=None):
        if self._game._activeplayer == self._game._playerid and self._game._currentphase+1 == 1:
            self._game._currentphase = 1
            self._game.WritePhasePacket(1)

            self._game.OnDeckDraw()

            self._game.ClearPhases()
            self._sel = True
            self._opp = False
            self.Hide()
            self.Show()
            self._game.WriteGameMessage('entered Draw Phase.', CHAT_PLAYER)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self._texture, 0, 0, True)
        dc.SetFont(wx.Font(pointSize=10,family=wx.FONTFAMILY_DEFAULT,style=wx.FONTSTYLE_NORMAL,weight=wx.FONTWEIGHT_NORMAL,
                           faceName="Tahoma"))
        if self._sel:
            if self._opp:
                dc.SetTextForeground(wx.RED)
            else:
                dc.SetTextForeground(wx.CYAN)
        else:
            dc.SetTextForeground(wx.WHITE)

        dc.DrawBitmap(self._texture, 0, 0, True)
        dc.DrawText("Draw", 18, 10)

class ClockPhaseControl(GameObject):

    def __init__(self, parent):
        self._game = parent
        GameObject.__init__(self, parent, (304+80,341), self._game._engine.GetImageSkin('Phase'))
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self._sel = False
        self._opp = False

    def SelectPhase(self):
        self._game._currentphase = 2
        self._game.ClearPhases()
        self._sel = True
        self._opp = True
        self.Hide()
        self.Show()

    def IsSelected(self):
        return self._sel

    def OnLeftUp(self, event=None):
        if self._game._activeplayer == self._game._playerid and self._game._currentphase+1 == 2:
            self._game._currentphase = 2
            self._game.WritePhasePacket(2)
            self._game.ClearPhases()
            self._sel = True
            self._opp = False
            self.Hide()
            self.Show()
            self._game.WriteGameMessage('entered Clock Phase.', CHAT_PLAYER)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self._texture, 0, 0, True)
        dc.SetFont(wx.Font(pointSize=10,family=wx.FONTFAMILY_DEFAULT,style=wx.FONTSTYLE_NORMAL,weight=wx.FONTWEIGHT_NORMAL,
                           faceName="Tahoma"))
        if self._sel:
            if self._opp:
                dc.SetTextForeground(wx.RED)
            else:
                dc.SetTextForeground(wx.CYAN)
        else:
            dc.SetTextForeground(wx.WHITE)

        dc.DrawBitmap(self._texture, 0, 0, True)
        dc.DrawText("Clock", 18, 10)

class MainPhaseControl(GameObject):

    def __init__(self, parent):
        self._game = parent
        GameObject.__init__(self, parent, (367+80,341), self._game._engine.GetImageSkin('Phase'))
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self._sel = False
        self._opp = False

    def SelectPhase(self):
        self._game._currentphase = 3
        self._game.ClearPhases()
        self._sel = True
        self._opp = True
        self.Hide()
        self.Show()

    def IsSelected(self):
        return self._sel

    def OnLeftUp(self, event=None):
        if self._game._activeplayer == self._game._playerid and self._game._currentphase+1 == 3:
            self._game._currentphase = 3
            self._game.WritePhasePacket(3)
            self._game.ClearPhases()
            self._sel = True
            self._opp = False
            self.Hide()
            self.Show()
            self._game.WriteGameMessage('entered Main Phase.', CHAT_PLAYER)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self._texture, 0, 0, True)
        dc.SetFont(wx.Font(pointSize=10,family=wx.FONTFAMILY_DEFAULT,style=wx.FONTSTYLE_NORMAL,weight=wx.FONTWEIGHT_NORMAL,
                           faceName="Tahoma"))
        if self._sel:
            if self._opp:
                dc.SetTextForeground(wx.RED)
            else:
                dc.SetTextForeground(wx.CYAN)
        else:
            dc.SetTextForeground(wx.WHITE)

        dc.DrawBitmap(self._texture, 0, 0, True)
        dc.DrawText("Main", 18, 10)

class ClimaxPhaseControl(GameObject):

    def __init__(self, parent):
        self._game = parent
        GameObject.__init__(self, parent, (430+80,341), self._game._engine.GetImageSkin('Phase'))
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self._sel = False
        self._opp = False

    def SelectPhase(self):
        self._game._currentphase = 4
        self._game.ClearPhases()
        self._sel = True
        self._opp = True
        self.Hide()
        self.Show()

    def IsSelected(self):
        return self._sel

    def OnLeftUp(self, event=None):
        if self._game._activeplayer == self._game._playerid and self._game._currentphase+1 == 4:
            self._game._currentphase = 4
            self._game.WritePhasePacket(4)
            self._game.ClearPhases()
            self._sel = True
            self._opp = False
            self.Hide()
            self.Show()
            self._game.WriteGameMessage('entered Climax Phase.', CHAT_PLAYER)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self._texture, 0, 0, True)
        dc.SetFont(wx.Font(pointSize=10,family=wx.FONTFAMILY_DEFAULT,style=wx.FONTSTYLE_NORMAL,weight=wx.FONTWEIGHT_NORMAL,
                           faceName="Tahoma"))
        if self._sel:
            if self._opp:
                dc.SetTextForeground(wx.RED)
            else:
                dc.SetTextForeground(wx.CYAN)
        else:
            dc.SetTextForeground(wx.WHITE)

        dc.DrawBitmap(self._texture, 0, 0, True)
        dc.DrawText("Climax", 12, 10)

class AttackPhaseControl(GameObject):

    def __init__(self, parent):
        self._game = parent
        GameObject.__init__(self, parent, (493+80,341), self._game._engine.GetImageSkin('Phase'))
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self._sel = False
        self._opp = False

    def SelectPhase(self):
        self._game._currentphase = 5
        self._game.ClearPhases()
        self._sel = True
        self._opp = True
        self.Hide()
        self.Show()

    def IsSelected(self):
        return self._sel

    def OnLeftUp(self, event=None):
        if self._game._activeplayer == self._game._playerid and self._game._currentphase+1 == 5:
            self._game._currentphase = 5
            self._game.WritePhasePacket(5)
            self._game.ClearPhases()
            self._sel = True
            self._opp = False
            self.Hide()
            self.Show()
            self._game.WriteGameMessage('entered Attack Phase.', CHAT_PLAYER)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self._texture, 0, 0, True)
        dc.SetFont(wx.Font(pointSize=10,family=wx.FONTFAMILY_DEFAULT,style=wx.FONTSTYLE_NORMAL,weight=wx.FONTWEIGHT_NORMAL,
                           faceName="Tahoma"))
        if self._sel:
            if self._opp:
                dc.SetTextForeground(wx.RED)
            else:
                dc.SetTextForeground(wx.CYAN)
        else:
            dc.SetTextForeground(wx.WHITE)

        dc.DrawBitmap(self._texture, 0, 0, True)
        dc.DrawText("Attack", 14, 10)

class EndPhaseControl(GameObject):

    def __init__(self, parent):
        self._game = parent
        GameObject.__init__(self, parent, (556+80,341), self._game._engine.GetImageSkin('Phase'))
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self._sel = False
        self._opp = False

    def SelectPhase(self):
        self._game._currentphase = 6
        self._game.ClearPhases()
        self._sel = True
        self._opp = True
        self.Hide()
        self.Show()

    def IsSelected(self):
        return self._sel

    def OnLeftUp(self, event=None):
        if self._game._activeplayer == self._game._playerid and self._game._currentphase+1 == 6:
            self._game._currentphase = 6

            self._game._activeplayer = (self._game._activeplayer % 2) + 1
            if len(self._game._climax) > 0:
                self._game._currentcard = self._game._climax[0]
                self._game.OnClimaxToWaitingRoom()
            self._game._clocked = False

            self._game.WritePhasePacket(6)
            self._game.ClearPhases()
            self._sel = True
            self._opp = False
            self.Hide()
            self.Show()
            self._game.WriteGameMessage('ended turn.', CHAT_PLAYER)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.DrawBitmap(self._texture, 0, 0, True)
        dc.SetFont(wx.Font(pointSize=10,family=wx.FONTFAMILY_DEFAULT,style=wx.FONTSTYLE_NORMAL,weight=wx.FONTWEIGHT_NORMAL,
                           faceName="Tahoma"))
        if self._sel:
            if self._opp:
                dc.SetTextForeground(wx.RED)
            else:
                dc.SetTextForeground(wx.CYAN)
        else:
            dc.SetTextForeground(wx.WHITE)

        dc.DrawBitmap(self._texture, 0, 0, True)
        dc.DrawText("End", 21, 10)

class DeckControl(GameObject):

    def __init__(self, parent, pos, t):
        GameObject.__init__(self, parent, pos, t)

    def UpdateCardTooltip(self, li):
        s = 'Deck: ' + str(len(li))
        tip = wx.ToolTip(s)
        tip.SetDelay(250)
        self.SetToolTip(tip)
        self.Hide()
        self.Show()

class OpponentDeckControl(GameObject):

    def __init__(self, parent, pos, t):
        GameObject.__init__(self, parent, pos, t)

    def UpdateCardTooltip(self, li):
        s = 'Deck: ' + str(len(li))
        tip = wx.ToolTip(s)
        tip.SetDelay(250)
        self.SetToolTip(tip)
        self.Hide()
        self.Show()

class WaitingRoomControl(GameObject):

    def __init__(self, parent, pos, t, game):
        self._game = game
        GameObject.__init__(self, parent, pos, t, size=self._game._cardsize)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        if len(self._game._waitingroom) > 0:
            dc.DrawBitmap(self._game._engine.GetImageCard(self._game._waitingroom[0]), 0, 0, True)
        else:
            dc.DrawBitmap(self._texture, 0, 0, True)

    def UpdateCardTooltip(self, li):
        s = 'Waiting Room: ' + str(len(li))
        tip = wx.ToolTip(s)
        tip.SetDelay(250)
        self.SetToolTip(tip)
        self.Hide()
        self.Show()

class OpponentWaitingRoomControl(GameObject):

    def __init__(self, parent, pos, t, game):
        self._game = game
        GameObject.__init__(self, parent, pos, t, size=self._game._cardsize)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        if len(self._game._oppwaitingroom) > 0:
            dc.DrawBitmap(self._game._engine.Rotate180Bitmap(self._game._engine.GetImageCard(self._game._oppwaitingroom[0])),
                          0, 0, True)
        else:
            dc.DrawBitmap(self._texture, 0, 0, True)

    def UpdateCardTooltip(self, li):
        s = 'Waiting Room: ' + str(len(li))
        tip = wx.ToolTip(s)
        tip.SetDelay(250)
        self.SetToolTip(tip)
        self.Hide()
        self.Show()

class TriggerControl(wx.Dialog):

    def __init__(self, parent):
        self._parent = parent

        wx.Dialog.__init__(self, parent=parent, id=-1, title='Trigger Card', size=(290,440), style=wx.CAPTION)
        self.CenterOnParent()
        self.Frame = parent
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.ButtonPanel = wx.Panel(self, -1)

        self.CardButton = wx.BitmapButton(self.ButtonPanel, id=-1, bitmap=wx.NullBitmap, pos=(0, 0), size=(290, 420))
        self.CardButton.Bind(wx.EVT_BUTTON, self.OnCardClick)

    def OnCardClick(self, event):
        self.EndModal(0)

    def OnClose(self, event):
        return

class DeckListControl(wx.Frame):

    def __init__(self, parent):
        self._game = parent
        wx.Frame.__init__(self, parent, -1, 'Deck', pos=(400,300), size=(168,200), style=wx.FRAME_TOOL_WINDOW |
                          wx.FRAME_FLOAT_ON_PARENT | wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Scroll = wx.ScrolledWindow(self,-1)
        self.Scroll.SetScrollbars(0, 1, 0, 200)
        self.Scroll.SetBackgroundColour(wx.Colour(33,35,36))

    def OnClose(self, event=None):
        return
        #self._game.OnPopupDeckSearch()

class OpponentDeckListControl(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'Opponent Deck', pos=(400,300), size=(168,200), style=wx.FRAME_TOOL_WINDOW |
                          wx.FRAME_FLOAT_ON_PARENT | wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Scroll = wx.ScrolledWindow(self,-1)
        self.Scroll.SetScrollbars(0, 1, 0, 200)
        self.Scroll.SetBackgroundColour(wx.Colour(33,35,36))

    def OnClose(self, event=None):
        self.Hide()

class WaitingRoomListControl(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'Waiting Room', pos=(400,300), size=(620,300), style=wx.FRAME_TOOL_WINDOW |
                          wx.FRAME_FLOAT_ON_PARENT | wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Scroll = wx.ScrolledWindow(self, -1)
        self.Scroll.SetScrollbars(0, 1, 0, 200)
        self.Scroll.SetBackgroundColour(wx.Colour(33,35,36))

    def OnClose(self, event=None):
        self.Parent.OnWaitingRoomLClick()

class OpponentWaitingRoomListControl(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'Opponent Waiting Room', pos=(400,300), size=(620,300),
                          style=wx.FRAME_TOOL_WINDOW | wx.FRAME_FLOAT_ON_PARENT | wx.CAPTION |
                          wx.CLOSE_BOX | wx.SYSTEM_MENU)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Scroll = wx.ScrolledWindow(self, -1)
        self.Scroll.SetScrollbars(0, 1, 0, 200)
        self.Scroll.SetBackgroundColour(wx.Colour(33,35,36))

    def OnClose(self, event=None):
        self.Parent.OnOpponentWaitingRoomLClick()

class HandControl(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, pos=(730, 572), size=(500, 100))
        self.SetBackgroundColour(wx.Colour(112, 138, 144))

class OpponentHandControl(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, pos=(1,0), size=(698,40))
        self.SetBackgroundColour(wx.Colour(112, 138, 144))

class CardControl(GameObject, wx.DataObjectSimple, wx.TextDropTarget):

    def __init__(self, parent, card, engine, game, serial, cpos=0, cardmode=0, cardface=1):
        self._card = card
        self._cardposition = cpos
        self._cardface = cardface
        self._cardmode = cardmode
        self._engine = engine
        self._game = game
        self._cardtarget = False
        self._counters = 0
        t = self._engine.GetImageCard(self)
        GameObject.__init__(self, parent, (0,0), t)
        wx.DataObjectSimple.__init__(self)
        self._serial = serial
        self.Bind(wx.EVT_MOTION, self.OnDrag)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseOver)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

        #Drop Target Setup
        wx.TextDropTarget.__init__(self)
        self.SetDropTarget(self)

    def OnDropText(self, x, y, data):
        if self._cardposition == POS_CLOCK:
            self._game.OnCardDropOnField(380, 245, data)
        elif self._cardposition == POS_CENTERSTAGE1:
            self._game.OnCardDropOnField(300, 50, data)
        elif self._cardposition == POS_CENTERSTAGE2:
            self._game.OnCardDropOnField(400, 50, data)
        elif self._cardposition == POS_CENTERSTAGE3:
            self._game.OnCardDropOnField(500, 50, data)
        elif self._cardposition == POS_BACKSTAGE1:
            self._game.OnCardDropOnField(330, 150, data)
        elif self._cardposition == POS_BACKSTAGE2:
            self._game.OnCardDropOnField(470, 150, data)
        elif self._cardposition == POS_LEVEL:
            self._game.OnCardDropOnField(150, 195, data)

    def GetCardMode(self):
        return self._cardmode

    def IsOpponentCard(self):
        return False

    def IsTarget(self):
        return self._cardtarget

    def Target(self):
        if self._cardtarget:
            self._cardtarget = False
        else:
            self._cardtarget = True

    def IsFaceDown(self):
        if self._cardface == FACE_DOWN:
            return 1
        else:
            return 0

    def IsFaceUp(self):
        if self._cardface == FACE_UP:
            return 1
        else:
            return 0

    def IsHorizontal(self):
        if self._cardmode == CARD_HORIZONTAL:
            return 1
        else:
            return 0

    def Horizontal(self):
        self._cardmode = CARD_HORIZONTAL

    def Vertical(self):
        self._cardmode = CARD_VERTICAL

    def IsClimax(self):
        return self._card.IsClimax()

    def IsCharacter(self):
        return self._card.IsCharacter()

    def IsEvent(self):
        return self._card.IsEvent()

    def GetSerial(self):
        return self._serial

    def GetCardName(self):
        return self._card.Name

    def GetCardImage(self):
        return self._card.Image

    def GetCardPosition(self):
        return self._cardposition

    def SetCardState(self, pos=POS_FIELD, mode=CARD_VERTICAL, face=FACE_UP):
        self._cardposition = pos
        self._cardmode = mode
        self._cardface = face
        if self.IsTarget():
            self.Target()
        #if not pos == POS_FIELD:
            #self.RemoveCounters(self._counters)
        self.RefreshTexture()

    def RefreshTexture(self):
        self._texture = self._engine.GetImageCard(self)
        self.SetSize((self._texture.GetWidth(), self._texture.GetHeight()))

    def OnDrag(self, event):
        if not event.Dragging():
            return
        if not event.LeftIsDown():
            return
        tt = self.GetSerial()
        tdo = wx.TextDataObject(tt)
        tds = wx.DropSource(self)
        tds.SetData(tdo)
        tds.DoDragDrop(True)

    def OnMouseOver(self, event):
        desc = self._card.Name + '\n'
        desc += 'Card No: ' + self._card.CardID + ' Rarity: ' + self._card.Rarity + '\n'
        desc += 'Color: ' + self._card.Color + ' (' + self._card.Side + ')\n'
        desc += 'Level: ' + str(self._card.Level) + ' Cost: ' + str(self._card.Cost) + '\n'
        desc += 'Power: ' + str(self._card.Power) + ' Soul: ' + str(self._card.Soul) + '\n'
        desc += 'Traits: '
        for trait in self._card.Traits:
            desc += '[' + trait + '] '
        desc += '\nTriggers: '
        for trigger in self._card.Triggers:
            desc += '[' + trigger + '] '
        desc += '\n\nFlavor:\n' + self._card.Flavor + '\n'
        desc += '\nTEXT:\n' + self._card.Text + '\n'

        self._game.RefreshCardInfo(self._card.Name, self._engine.GetImageBigCard(self._card), desc)

    def OnRightUp(self, event):
        self._game.OnCardPopup(self)

class OpponentCardControl(GameObject):

    def __init__(self, parent, card, engine, game, serial, cpos=0, cardmode=0, cardface=1):
        self._card = card
        self._cardposition = cpos
        self._cardface = cardface
        self._cardmode = cardmode
        self._engine = engine
        self._game = game
        self._cardtarget = False
        self._counters = 0
        t = self._engine.GetImageCard(self)
        GameObject.__init__(self, parent, (0,0), t)
        self._serial = serial
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseOver)
        #self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

    def IsOpponentCard(self):
        if self._cardposition > 14 and self._cardposition < 27:
            return True
        else:
            return False

    def AddCounters(self, n=1):
        self._counters += n
        self.Hide()
        self.Show()

    def RemoveCounters(self, n=1):
        self._counters -= n
        if self._counters < 0:
            self._counters = 0
        self.Hide()
        self.Show()

    def Target(self):
        if self._cardtarget:
            self._cardtarget = False
        else:
            self._cardtarget = True

    def IsTarget(self):
        return self._cardtarget

    def OnMouseOver(self, event):
        if self.IsFaceDown():
            return
        desc = self._card.Name + '\n'
        desc += 'Card No: ' + self._card.CardID + ' Rarity: ' + self._card.Rarity + '\n'
        desc += 'Color: ' + self._card.Color + ' (' + self._card.Side + ')\n'
        desc += 'Level: ' + str(self._card.Level) + ' Cost: ' + str(self._card.Cost) + '\n'
        desc += 'Power: ' + str(self._card.Power) + ' Soul: ' + str(self._card.Soul) + '\n'
        desc += 'Traits: '
        for trait in self._card.Traits:
            desc += '[' + trait + '] '
        desc += '\nTriggers: '
        for trigger in self._card.Triggers:
            desc += '[' + trigger + '] '
        desc += '\n\nFlavor:\n' + self._card.Flavor + '\n'
        desc += '\nTEXT:\n' + self._card.Text + '\n'

        self._game.RefreshCardInfo(self._card.Name, self._engine.GetImageBigCard(self._card), desc)

    def RefreshTexture(self):
        self._texture = self._engine.GetImageCard(self)
        self.SetSize((self._texture.GetWidth(), self._texture.GetHeight()))

    def GetCardName(self):
        return self._card.Name

    def GetCardImage(self):
        return self._card.Image

    def GetCardPosition(self):
        return self._cardposition

    def GetCardFace(self):
        return self._cardface

    def GetCardMode(self):
        return self._cardmode

    def GetSerial(self):
        return self._serial

    def IsFaceDown(self):
        if self._cardface == FACE_DOWN:
            return 1
        else:
            return 0

    def IsFaceUp(self):
        if self._cardface == FACE_UP:
            return 1
        else:
            return 0

    def IsHorizontal(self):
        if self._cardmode == CARD_HORIZONTAL:
            return 1
        else:
            return 0

    def IsVertical(self):
        if self._cardmode == CARD_VERTICAL:
            return 1
        else:
            return 0

    def IsClimax(self):
        return self._card.IsClimax()

    def IsCharacter(self):
        return self._card.IsCharacter()

    def IsEvent(self):
        return self._card.IsEvent()

    def SetCardPosition(self, p):
        if self.IsTarget():
            self.Target()
        self._cardposition = p

    def SetCardState(self, pos=POS_OPP_FIELD, mode=CARD_VERTICAL, face=FACE_UP):
        self._cardposition = pos
        self._cardmode = mode
        self._cardface = face
        if self.IsTarget():
            self.Target()
        #if not pos == POS_FIELD:
            #self.RemoveCounters(self._counters)
        self.RefreshTexture()

    def FaceUp(self):
        if self.IsTarget():
            self.Target()
        self._cardface = FACE_UP

    def FaceDown(self):
        if self.IsTarget():
            self.Target()
        self._cardface = FACE_DOWN

    def Vertical(self):
        if self.IsTarget():
            self.Target()
        self._cardmode = CARD_VERTICAL

    def Horizontal(self):
        if self.IsTarget():
            self.Target()
        self._cardmode = CARD_HORIZONTAL

class ConsoleCtrl(wx.TextCtrl):
    def __init__(self, parent):
        wx.TextCtrl.__init__(self, parent, pos=(710,545), size=(560,-1), style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnPressEnter)

    def OnPressEnter(self, event):
        if len(self.GetValue()) < 1:
            return
        m = self.GetValue()
        self.SetValue('')
        self.Parent.ProcessMessage(m)
