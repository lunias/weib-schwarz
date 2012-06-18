import wx, sys, os
from gamecontrols import *

class GameFrame(wx.Frame):

    def __init__(self, engine):
        self._engine = engine
        wx.Frame.__init__(self, parent=None, title="Weib Schwarz Simulator", size=(1280, 720), style=wx.MINIMIZE_BOX |
                          wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU)
        self.CenterOnScreen()
        self.Game = GamePanel(self, self._engine)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event=None):
        self.Game.OnClose()
        self.Destroy()
