import wx, sys, os
import engine

class ConnectionDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title='Connection', size=(-1,-1),style=wx.CAPTION):
        wx.Dialog.__init__(self, parent=parent, id=id, title=title, size=size, style=style)
        self.CenterOnParent()
        self.Frame = parent
        self._hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self._vsizer1 = wx.BoxSizer(wx.VERTICAL)
        self._vsizer2 = wx.BoxSizer(wx.VERTICAL)
        self.AddressStaticText = wx.StaticText(self, -1, "Address")
        self.AddressTextCtrl = wx.TextCtrl(self, -1, "127.0.0.1")
        self.PortStaticText = wx.StaticText(self, -1, "Port")
        self.PortTextCtrl = wx.TextCtrl(self, -1, "14120")
        self.NickStaticText = wx.StaticText(self, -1, "Nickname")
        self.NickTextCtrl = wx.TextCtrl(self, -1, "Lunias")
        self.OkButton = wx.Button(self, wx.ID_OK)
        self.CancelButton = wx.Button(self, wx.ID_CANCEL)
        self.OkButton.Bind(wx.EVT_BUTTON, self.OnOk)
        self.CancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.Connect(-1, -1, 500003, self.OnConnection)
        self.Connect(-1, -1, 500004, self.OnConnectionError)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self._vsizer1.Add(self.AddressStaticText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.Add(self.AddressTextCtrl, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer1.Add(self.PortStaticText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.Add(self.PortTextCtrl, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer1.Add(self.NickStaticText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.Add(self.NickTextCtrl, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer1.Add(self.CancelButton, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.Add(self.OkButton, 1, wx.ALL | wx.EXPAND, 2)

        self._hsizer.Add(self._vsizer1, 1, wx.ALL | wx.EXPAND, 2)
        self._hsizer.Add(self._vsizer2, 1, wx.ALL | wx.EXPAND, 2)

        self.SetSizer(self._hsizer)
        self.Layout()
        self.Fit()

    def OnClose(self, event):
        return

    def OnOk(self, event):
        self.OkButton.Disable()
        vars = self.GetValues()
        self.Frame.Engine.Network.Connect(vars[0], int(vars[1]), vars[2], self)

    def OnCancel(self, event):
        self.Frame.Engine.Network.StopConnect()
        self.EndModal(0)

    def OnConnection(self, event):
        self.EndModal(2)

    def OnConnectionError(self, event):
        self.Frame.ShowDialog('Connection Error', '', wx.OK | wx.ICON_ERROR, self)
        self.OkButton.Enable()

    def GetValues(self):
        vars = []
        vars.append(self.AddressTextCtrl.GetValue())
        vars.append(self.PortTextCtrl.GetValue())
        vars.append(self.NickTextCtrl.GetValue())
        return vars

class ListenDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title='Listen', size=(-1,-1),style=wx.CAPTION):
        wx.Dialog.__init__(self, parent=parent, id=id, title=title, size=size, style=style)
        self.CenterOnParent()
        self.Frame = parent
        self._engine = self.Frame.Engine
        self._ipdialog = wx.TextEntryDialog(self, '', '', style=wx.OK, defaultValue='')
        self._hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self._vsizer1 = wx.BoxSizer(wx.VERTICAL)
        self._vsizer2 = wx.BoxSizer(wx.VERTICAL)
        self._vsizer3 = wx.BoxSizer(wx.VERTICAL)
        self.NickStaticText = wx.StaticText(self, -1, "Nickname")
        self.NickTextCtrl = wx.TextCtrl(self, -1, 'Lunias')
        self.PortStaticText = wx.StaticText(self, -1, "Port")
        self.PortTextCtrl = wx.TextCtrl(self, -1, "14120")
        self.IpButton = wx.Button(self, -1, label='Get IP')
        self.OkButton = wx.Button(self, wx.ID_OK)
        self.CancelButton = wx.Button(self, wx.ID_CANCEL)
        self.OkButton.Bind(wx.EVT_BUTTON, self.OnOk)
        self.CancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.IpButton.Bind(wx.EVT_BUTTON, self.OnGetIp)
        self.Connect(-1, -1, 500001, self.OnListen)
        self.Connect(-1, -1, 500002, self.OnListenError)

        self._vsizer1.Add(self.PortStaticText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer1.Add(self.NickStaticText, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer1.Add(self.IpButton, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer2.AddStretchSpacer(2)
        self._vsizer2.Add(self.CancelButton, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer3.Add(self.PortTextCtrl, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer3.Add(self.NickTextCtrl, 1, wx.ALL | wx.EXPAND, 2)
        self._vsizer3.Add(self.OkButton, 1, wx.ALL | wx.EXPAND, 2)

        self._hsizer.Add(self._vsizer1, 1, wx.ALL | wx.EXPAND, 2)
        self._hsizer.Add(self._vsizer2, 1, wx.ALL | wx.EXPAND, 2)
        self._hsizer.Add(self._vsizer3, 1, wx.ALL | wx.EXPAND, 2)

        self.SetSizer(self._hsizer)
        self.Layout()
        self.Fit()

    def OnGetIp(self, event=None):
        try:
            ip = self._engine.GetIp()
            self._ipdialog.SetValue(ip)
            self._ipdialog.SetTitle(ip)
            self._ipdialog.ShowModal()
        except: pass

    def OnOk(self, event):
        self.OkButton.Disable()
        vars = self.GetValues()
        self.Frame.Engine.Network.Listen(int(vars[0]), vars[1], self)

    def OnCancel(self, event):
        self.Frame.Engine.Network.StopListen()
        self.EndModal(0)

    def OnListen(self, event):
        self.EndModal(2)

    def OnListenError(self, event):
        self.Frame.ShowDialog('Listen Error', '', wx.OK | wx.ICON_ERROR, self)
        self.OkButton.Enable()

    def GetValues(self):
        vars = []
        vars.append(self.PortTextCtrl.GetValue())
        vars.append(self.NickTextCtrl.GetValue())
        return vars


