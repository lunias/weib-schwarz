import wx, sys, os
from wx import richtext
from wx.lib.plot import PlotGraphics, PlotCanvas, PolyLine
import engine, network, gameframe, dialogs

ID_NEW = 10001
ID_OPEN = 10002
ID_SAVE = 10003
ID_SAVEAS = 10004
ID_CLOSE = 10005
ID_CONNECT = 10006
ID_LISTEN = 10007
ID_PLAY = 10008
ID_POPUP_ADD = 10009
ID_POPUP_REMOVE = 10010

class MainFrame(wx.Frame):

    def __init__(self, engine, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.Centre()
        self.Engine = engine
        self.SelectedFromDeck = ''
        self.SelectedFromSide = False
        self.SortDeckBy = 'Name'
        self.Plotting = 'Level'

        #Variables
        self.panel    = wx.Panel(self)
        self.vbox1    = wx.BoxSizer(wx.VERTICAL)
        self.vbox2    = wx.BoxSizer(wx.VERTICAL)
        self.vbox5    = wx.BoxSizer(wx.VERTICAL)
        self.hbox     = wx.BoxSizer(wx.HORIZONTAL)
        self.graphbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hmbox1   = wx.BoxSizer(wx.HORIZONTAL)
        self.hmbox2   = wx.BoxSizer(wx.HORIZONTAL)
        self.hvbox1   = wx.BoxSizer(wx.HORIZONTAL)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        #Status Bar
        self.StatusBar = wx.StatusBar(self,-1)
        self.SetStatusBar(self.StatusBar)
        self.StatusBar.SetStatusText(self.Engine.GetNameVersion(), 0)

        #Card Search
        self.CardSearchCtrl = wx.TextCtrl(self.panel, -1, "")
        self.CardSearchCtrl.Bind(wx.EVT_TEXT, self.OnSearchInput, self.CardSearchCtrl)

        #Card List
        self.CardListCtrl = wx.ListCtrl(self.panel, -1, size=(300, -1), style = wx.LC_REPORT | wx.LC_SINGLE_SEL |
                                        wx.LC_NO_HEADER | wx.LC_HRULES )
        self.CardListCtrl.InsertColumn(0, 'Name')
        self.CardListCtrl.InsertColumn(1, 'CardID')
        n = 0
        for c in self.Engine.CardDict.GetSortedValues():
            idx = self.CardListCtrl.InsertStringItem(n, c.Name)
            self.CardListCtrl.SetStringItem(idx, 1, c.CardID)
            n += 1
        self.CardListCtrl.SetColumnWidth(0, 310)
        self.CardListCtrl.SetColumnWidth(1, 0)
        self.CardListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnCardSelected)
        self.CardListCtrl.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnCardListItemRClick)
        self.CardListCtrl.Bind(wx.EVT_LEFT_DCLICK, self.OnAddCard)

        #Deck List
        self.DeckHeaderText = wx.StaticText(self.panel, -1, 'Cards in Deck: 0')
        self.DeckListCtrl = wx.ListCtrl(self.panel, -1, size=(-1, 520), style = wx.LC_REPORT | wx.LC_SINGLE_SEL |
                                        wx.LC_HRULES)
        self.DeckListCtrl.InsertColumn(0, 'Card Name')
        self.DeckListCtrl.SetColumnWidth(0, 350)
        self.DeckListCtrl.InsertColumn(1, 'Color')
        self.DeckListCtrl.SetColumnWidth(1, 50)
        self.DeckListCtrl.InsertColumn(2, 'Level')
        self.DeckListCtrl.SetColumnWidth(2, 50)
        self.DeckListCtrl.InsertColumn(3, 'Cost')
        self.DeckListCtrl.SetColumnWidth(3, 50)
        self.DeckListCtrl.InsertColumn(4, 'Power')
        self.DeckListCtrl.SetColumnWidth(4, 50)
        self.DeckListCtrl.InsertColumn(5, 'Soul')
        self.DeckListCtrl.SetColumnWidth(5, 50)
        self.DeckListCtrl.InsertColumn(6, 'Count')
        self.DeckListCtrl.SetColumnWidth(6, 50)
        self.DeckListCtrl.InsertColumn(7, 'CardID')
        self.DeckListCtrl.SetColumnWidth(7, 0)
        self.DeckListCtrl.Bind(wx.EVT_LIST_COL_CLICK, self.OnDeckColumnClick)
        self.DeckListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnDeckCardSelected)
        self.DeckListCtrl.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnDeckListItemRClick)
        self.DeckListCtrl.Bind(wx.EVT_LEFT_DCLICK, self.OnRemoveCard)

        #Deck Graph
        self.DeckGraphCanvas = PlotCanvas(self.panel)
        self.DeckGraphCanvas.Draw(self.DrawGraph(), xAxis=(0,4))

        #Card Info
        self.CardNameCtrl = wx.StaticText(self.panel, -1, style=wx.ALIGN_CENTRE)
        self.CardImageCtrl = wx.StaticBitmap(self.panel, -1, size=(300,420))
        self.CardDescriptionCtrl = wx.TextCtrl(self.panel, -1, size=(300,150), style=wx.TE_MULTILINE | wx.TE_READONLY |
                                               wx.TE_LEFT)

        #Build UI
        self.BuildUI()

        #Layout
        self.hvbox1.Add(self.CardSearchCtrl, 1, wx.ALL | wx.EXPAND, 2)
        self.hvbox1.Add(self.CardReloadCtrl, 0, wx.ALL | wx.EXPAND, 2)
        self.vbox1.Add(self.hvbox1, 0, wx.ALL | wx.EXPAND, 2)
        self.vbox1.Add(self.CardListCtrl, 1, wx.ALL | wx.EXPAND, 2)

        self.hmbox1.Add(self.DeckHeaderText, 1, wx.ALL | wx.EXPAND, 2)
        self.hmbox2.Add(self.DeckListCtrl, 1, wx.ALL | wx.EXPAND, 2)
        self.graphbox.Add(self.DeckGraphCanvas, 1, wx.ALL | wx.EXPAND, 2)
        self.vbox2.Add(self.hmbox1, 0, wx.ALL | wx.EXPAND, 2)
        self.vbox2.Add(self.hmbox2, 1, wx.ALL | wx.EXPAND, 2)
        self.vbox2.Add(self.graphbox, 1, wx.ALL | wx.EXPAND, 2)

        self.vbox5.Add(self.CardNameCtrl, 0, wx.ALL | wx.ALIGN_CENTER , 2)
        self.vbox5.Add(self.CardImageCtrl, 0, wx.ALL | wx.ALIGN_CENTER, 2)
        self.vbox5.Add(self.CardDescriptionCtrl, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 2)

        self.hbox.Add(self.vbox1, 0, wx.EXPAND | wx.ALL, 2)
        self.hbox.Add(self.vbox2, 1, wx.EXPAND | wx.ALL, 2)
        self.hbox.Add(self.vbox5, 0, wx.EXPAND | wx.ALL, 2)
        self.panel.SetSizer(self.hbox)
        self.panel.Layout()

    def BuildUI(self, changes=0):
        if changes:
            self.CardReloadCtrl.Destroy()
            self.GetToolBar().Destroy()
            self.CardListPopupMenu.Destroy()
            self.DeckListPopupMenu.Destroy()

        #Menu
        self.Menu = wx.MenuBar()
        self.mFile = wx.Menu()
        self.mGame = wx.Menu()
        self.mTools = wx.Menu()
        self.mHelp = wx.Menu()

        #File Menu
        item = wx.MenuItem(self.mFile,ID_NEW,'New')
        item.SetBitmap(self.Engine.GetImageSkin('New'))
        self.Bind(wx.EVT_MENU, self.OnNew, item)
        self.mFile.AppendItem(item)

        item = wx.MenuItem(self.mFile,ID_OPEN,'Open')
        item.SetBitmap(self.Engine.GetImageSkin('Open'))
        self.Bind(wx.EVT_MENU, self.OnOpen, item)
        self.mFile.AppendItem(item)

        item = wx.MenuItem(self.mFile,ID_SAVE,'Save')
        item.SetBitmap(self.Engine.GetImageSkin('Save'))
        self.Bind(wx.EVT_MENU, self.OnSave, item)
        self.mFile.AppendItem(item)

        item = wx.MenuItem(self.mFile,ID_SAVEAS,'SaveAs')
        item.SetBitmap(self.Engine.GetImageSkin('SaveAs'))
        self.Bind(wx.EVT_MENU, self.OnSaveAs, item)
        self.mFile.AppendItem(item)

        item = wx.MenuItem(self.mFile,ID_CLOSE,'Close')
        item.SetBitmap(self.Engine.GetImageSkin('Close'))
        self.Bind(wx.EVT_MENU, self.OnMenuClose, item)
        self.mFile.AppendItem(item)

        #Game Menu
        item = self.mGame.Append(ID_CONNECT, text='Connect')
        self.Bind(wx.EVT_MENU, self.OnConnectMenu, item)

        item = self.mGame.Append(ID_LISTEN, text='Listen')
        self.Bind(wx.EVT_MENU, self.OnListenMenu, item)

        item = self.mGame.Append(ID_PLAY, text='Test')
        self.Bind(wx.EVT_MENU, self.OnPlayMenu, item)

        #Create Menu
        self.Menu.Append(self.mFile, 'File')
        self.Menu.Append(self.mGame, 'Game')
        self.SetMenuBar(self.Menu)

        #Card Reload
        self.CardReloadCtrl = wx.BitmapButton(self.panel, -1, self.Engine.GetImageSkin('Reload'))
        self.CardReloadCtrl.SetToolTipString("Reload")
        self.CardReloadCtrl.Bind(wx.EVT_BUTTON, self.OnCardReload)

        #CardList Popup
        self.CardListPopupMenu = wx.Menu()
        item = wx.MenuItem(self.CardListPopupMenu,ID_POPUP_ADD,'Add')
        item.SetBitmap(self.Engine.GetImageSkin('Todeck'))
        self.Bind(wx.EVT_MENU, self.OnAddCard, item)
        self.CardListPopupMenu.AppendItem(item)

        #DeckList Popup
        self.DeckListPopupMenu = wx.Menu()
        item = wx.MenuItem(self.DeckListPopupMenu,ID_POPUP_REMOVE,'Remove')
        item.SetBitmap(self.Engine.GetImageSkin('Totrunk'))
        self.Bind(wx.EVT_MENU, self.OnRemoveCard, item)
        self.DeckListPopupMenu.AppendItem(item)

    def OnClose(self, event):
        if self.ShowDialog("Are you sure?", "Exit", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) == wx.ID_YES:
            sys.exit()

    def ShowDialog(self, message, title, style, parent=None):
        if parent == None:
            parent = self
        dialog = wx.MessageDialog(parent, message, title, style)
        return dialog.ShowModal()

    def OnSearchInput(self, event):
        input = self.CardSearchCtrl.GetValue()
        if len(input) < 3:
            return
        li = self.Engine.FindCardByNameLike(input)
        self.CardListCtrl.DeleteAllItems()
        n=0
        for c in li:
            idx = self.CardListCtrl.InsertStringItem(n, c.Name)
            self.CardListCtrl.SetStringItem(idx, 1, c.CardID)
            n += 1

    def OnCardReload(self, event):
        self.CardListCtrl.DeleteAllItems()
        n = 0
        for c in self.Engine.CardDict.GetSortedValues():
            idx = self.CardListCtrl.InsertStringItem(n, c.Name)
            self.CardListCtrl.SetStringItem(idx, 1, c.CardID)
            n += 1
        self.CardSearchCtrl.SetValue('')

    def OnCardSelected(self, event):
        cardID = self.CardListCtrl.GetItem(event.m_itemIndex, 1).GetText()
        card = self.Engine.CardDict.GetCardByID(cardID)
        self.SelectedFromDeck = cardID
        self.ShowCardInfo(card)

    def OnDeckCardSelected(self, event):
        cardID = self.DeckListCtrl.GetItem(event.m_itemIndex, 7).GetText()
        card = self.Engine.CardDict.GetCardByID(cardID)
        self.SelectedFromDeck = cardID
        self.ShowCardInfo(card)

    def OnCardListItemRClick(self, event):
        self.panel.PopupMenu(self.CardListPopupMenu)

    def OnDeckListItemRClick(self, event):
        self.panel.PopupMenu(self.DeckListPopupMenu)

    def OnDeckColumnClick(self, event):
        col = event.m_col
        if col == 0:
            self.SortDeckBy = 'Name'
        elif col == 1:
            self.SortDeckBy = 'Color'
        elif col == 2:
            self.SortDeckBy = 'Level'
            self.Plotting = 'Level'
        elif col == 3:
            self.SortDeckBy = 'Cost'
            self.Plotting = 'Cost'
        elif col == 4:
            self.SortDeckBy = 'Power'
            self.Plotting = 'Power'
        elif col == 5:
            self.SortDeckBy = 'Soul'
            self.Plotting = 'Soul'
        elif col == 6:
            self.SortDeckBy = 'Count'
        self.RefreshCardList()

    def ShowCardInfo(self, card):
        self.CardNameCtrl.SetLabel(card.Name.replace('&', '&&'))
        self.CardImageCtrl.SetBitmap(self.Engine.GetImageBigCard(card))

        desc = 'Card No: ' + card.CardID + ' Rarity: ' + card.Rarity + '\n'
        desc += 'Color: ' + card.Color + ' (' + card.Side + ')\n'
        desc += 'Level: ' + str(card.Level) + ' Cost: ' + str(card.Cost)
        desc += ' Power: ' + str(card.Power) + ' Soul: ' + str(card.Soul) + '\n'
        desc += 'Traits: '
        for trait in card.Traits:
            desc += '[' + trait + '] '
        desc += '\nTriggers: '
        for trigger in card.Triggers:
            desc += '[' + trigger + '] '
        desc += '\n\nFlavor:\n' + card.Flavor + '\n'
        desc += '\nTEXT:\n' + card.Text + '\n'

        self.CardDescriptionCtrl.SetValue(desc)
        self.panel.SendSizeEvent()

    def OnAddCard(self, event):
        if self.SelectedFromDeck == '':
            return
        c = self.Engine.CardDict.GetCardByID(self.SelectedFromDeck)
        self.Engine.Deck.Add(c)
        self.RefreshCardList()

    def OnRemoveCard(self, event):
        if self.SelectedFromDeck == '':
            return
        self.Engine.Deck.RemoveCardByID(self.SelectedFromDeck)
        self.SelectedFromDeck = ''
        self.RefreshCardList()

    def RefreshCardList(self):
        self.DeckListCtrl.DeleteAllItems()
        for card, count in self.Engine.Deck.GetCardsAndCounts(self.SortDeckBy):
            idx = self.DeckListCtrl.InsertStringItem(self.DeckListCtrl.GetItemCount(), card.Name)
            self.DeckListCtrl.SetStringItem(idx, 1, card.Color)
            self.DeckListCtrl.SetStringItem(idx, 2, str(card.Level))
            self.DeckListCtrl.SetStringItem(idx, 3, str(card.Cost))
            self.DeckListCtrl.SetStringItem(idx, 4, str(card.Power))
            self.DeckListCtrl.SetStringItem(idx, 5, str(card.Soul))
            self.DeckListCtrl.SetStringItem(idx, 6, str(count))
            self.DeckListCtrl.SetStringItem(idx, 7, card.CardID)
        self.DeckHeaderText.SetLabel('Cards in Deck: ' + str(self.Engine.Deck.GetCardCount()))
        self.DeckGraphCanvas.Draw(self.DrawGraph())

    def OnNew(self, event):
        self.Engine.NewDeck()
        self.SelectedFromDeck = ''
        self.RefreshCardList()

    def OnOpen(self, event=None, path=''):
        if path == '':
            dialog = wx.FileDialog(self, 'Open...', "", "", "XML Deck files (*.xml)|*.xml", wx.FD_OPEN)
            dialog.SetPath(os.path.join(self.Engine.DecksDirectory,'deck.xml'))
            if dialog.ShowModal() != wx.ID_OK:
                dialog.Destroy()
                return
            else:
                name = dialog.GetFilename()
                dir = dialog.GetDirectory()
                path = os.path.join(dir,name)
                dialog.Destroy()
        self.Engine.OpenDeck(path)
        self.Engine.DeckPath = path
        self.RefreshCardList()

    def OnSave(self, event):
        if self.Engine.DeckPath != '':
            self.Engine.SaveDeck(self.Engine.Deck, self.Engine.DeckPath)
        else:
            self.OnSaveAs(event)

    def OnSaveAs(self, event):
        dialog = wx.FileDialog(self, "Save As...", "", "", "XML Deck files (*.xml)|*.xml", wx.FD_SAVE)
        dialog.SetPath(os.path.join(self.Engine.DecksDirectory, 'deck.xml'))
        if dialog.ShowModal() == wx.ID_OK:
            name = dialog.GetFilename()
            dir = dialog.GetDirectory()
            path = os.path.join(dir,name)
            if not path.endswith('.xml'):
                path += '.xml'
            self.Engine.SaveDeck(self.Engine.Deck, path)
            self.Engine.DeckPath = path
        dialog.Destroy()

    def OnMenuClose(self, event):
        self.Close()

    def OnPlayMenu(self, event):
        self.Engine.GameFrame = gameframe.GameFrame(self.Engine)
        self.Engine.Game = self.Engine.GameFrame.Game
        self.Engine.Network = network.Network(self.Engine.Game)
        #self.Engine.Game._nick = self.Engine.GetSetting('Nick')
        self.Engine.Game.Shuffle()
        self.Engine.GameFrame.Show()

    def OnListenMenu(self, event):
        self.Engine.GameFrame = gameframe.GameFrame(self.Engine)
        self.Engine.Game = self.Engine.GameFrame.Game
        self.Engine.Network = network.Network(self.Engine.Game)
        dialog = dialogs.ListenDialog(self)
        dialog.ShowModal()

    def OnConnectMenu(self, event):
        self.Engine.GameFrame = gameframe.GameFrame(self.Engine)
        self.Engine.Game = self.Engine.GameFrame.Game
        self.Engine.Network = network.Network(self.Engine.Game)
        dialog = dialogs.ConnectionDialog(self)
        dialog.ShowModal()

    def DrawGraph(self):
        lines = []
        last_point = (-1, 0)
        for x, y in self.Engine.Deck.GetAttrsAndCounts(self.Plotting):
            lines.append(PolyLine([last_point, (x, y)], width=5))
            last_point = (x, y)
        if not lines:
            lines.append(PolyLine([(0, 0), (0, 0)]))
        return PlotGraphics(lines, self.Plotting, self.Plotting, 'Count')
