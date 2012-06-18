import sys, os, wx, time, re, urllib, math
from xml.dom import minidom
import version, network
import cards, deck, deckbuilder

class Engine():

    def __init__(self):
        self.Application = wx.App(redirect=True,filename="ws.log")
        self.BaseDirectory = os.getcwd()
        self.SkinsDirectory = os.path.join(self.BaseDirectory, 'skins')
        self.ImagesDirectory = os.path.join(self.BaseDirectory, 'images')
        self.DecksDirectory = os.path.join(self.BaseDirectory, 'decks')

        self._ip = ''

        self.CardDict = cards.Cards()
        self.Deck = deck.Deck()
        self.DeckPath = ''

        self.Frame = deckbuilder.MainFrame(engine=self, parent=None, title="Weib Schwarz Deck Builder",
                                           size=(1300, 800))

        self.Frame.Show()
        self.Application.MainLoop()

    def GetVersion(self):
        return version.GetVersion()

    def GetNameVersion(self):
        return "%s %s" % (version.GetName(), version.GetVersion())

    def FindCardByNameLike(self, name):
        li = list()
        for card in self.CardDict.GetSortedValues():
            if name in card.Name:
                li.append(card)
        return li

    def FindCardByCardID(self, cardID):
        return self.CardDict.GetCardByID(cardID)

    def GetImageSkin(self, name):
        path = os.path.join(self.SkinsDirectory, name + '.png')
        if os.path.exists(path):
            return wx.Bitmap(path)
        return -1

    def GetBitmapCard(self, c):
        path = os.path.join(self.ImagesDirectory, c.GetCardImage() + '.jpg')
        if os.path.exists(path):
            return wx.Bitmap(path)
        return -1

    def GetImageCard(self, c):
        if c.IsFaceDown():
            bmp = self.ResizeBitmap(self.GetImageSkin('CardBack'), 60, 88)
            if c.IsHorizontal():
                bmp = self.Rotate90Bitmap(bmp)
            return bmp
        b = self.ResizeBitmap(self.GetImageSkin('CardBack'), 60, 88)
        bmp = self.GetImageSmallCard(c.GetCardImage())
        if not bmp is -1:
            dc = wx.MemoryDC()
            dc.SelectObject(b)
            dc.DrawBitmap(bmp, 0, 0)
        if c.IsHorizontal():
            b = self.Rotate90Bitmap(b)
        if c.IsOpponentCard():
            b = self.Rotate180Bitmap(b)
        return b

    def GetImageCardScaled(self, name):
        path = os.path.join(self.ImagesDirectory, name + '.jpg')
        if os.path.exists(path):
            image = wx.Image(path)
            image.Rescale(289, 420, wx.IMAGE_QUALITY_HIGH)
            return wx.BitmapFromImage(image)
        return -1

    def GetImageSmallCard(self, name):
        path = os.path.join(self.ImagesDirectory, name + '.jpg')
        if os.path.exists(path):
            image = wx.Image(path)
            image.Rescale(60, 88, wx.IMAGE_QUALITY_HIGH)
            return wx.BitmapFromImage(image)
        return -1

    def GetImageBigCard(self, card):
        dc = wx.MemoryDC()
        dc.SelectObject(self.GetImageSkin('CardBack'))
        cbmp = self.GetImageCardScaled(card.Image)
        if not cbmp is -1:
            dc.DrawBitmap(cbmp, 0, 0)
        return dc.GetAsBitmap()

    def ResizeBitmap(self, bmp, w, h, q=wx.IMAGE_QUALITY_HIGH):
        img = wx.ImageFromBitmap(bmp)
        img.Rescale(w, h, q)
        return wx.BitmapFromImage(img)

    def Rotate90Bitmap(self, bmp):
        img = wx.ImageFromBitmap(bmp)
        return wx.BitmapFromImage(img.Rotate90(False))

    def Rotate180Bitmap(self, bmp):
        img = wx.ImageFromBitmap(bmp)
        return wx.BitmapFromImage(img.Rotate(math.pi, wx.Point(30, 44)))

    def NewDeck(self):
        self.Deck = deck.Deck()
        self.DeckPath = ''

    def OpenDeck(self, path):
        if not os.path.exists(path):
            return False
        else:
            xmldoc = minidom.parse(path)
        self.Deck = deck.Deck()
        for node in xmldoc.firstChild.childNodes:
            c = self.CardDict.GetCardByID(node.getAttribute('cardID'))
            self.Deck.Add(c)

    def SaveDeck(self, deck, path):
        handle = open(path, 'w')
        doc = minidom.Document()
        element = doc.createElement("deck")
        doc.appendChild(element)
        for c in deck.Cards:
            node = doc.createElement("card")
            node.setAttribute('cardID', c.CardID)
            element.appendChild(node)
        data = doc.toxml()
        handle.write(data)
        handle.close()

    def GetIp(self):
        if not self._ip:
            try:
                l = re.findall('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', urllib.urlopen("http://checkip.dyndns.org/").read())[0]
                self._ip = '%s.%s.%s.%s' % (l[0],l[1],l[2],l[3])
            except:
                self._ip == ''
        return self._ip

if __name__ == "__main__":
    e = Engine()
