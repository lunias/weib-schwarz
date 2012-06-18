import socket, wx, thread, sys, struct, traceback
from packets import *
from packetevents import *

ID_DISCONNECTED = 0
ID_CONNECTED = 1
ID_LISTENING = 2
ID_CONNECTING = 3
ID_STOPLISTEN = 4

def Loop(nw, *args):
    try:
        while nw.GetState() == ID_CONNECTED:
            packet = RecvPacket(nw.GetSocket())
            reader = PacketReader(packet[0], packet[1], packet[2])
            nw.OnPacket(reader)
    except:
        nw.OnClose()

def RecvPacket(sock):
    header_size = 0
    header = ''
    while header_size < 8:
        header += sock.recv(1)
        header_size += 1
    id,size = struct.unpack('>ii', header)

    recv_size = 0
    data = ''
    while recv_size < size:
        data += sock.recv(1)
        recv_size += 1

    return [id,size,data]

def ConnectThread(nw, *args):
    try:
        nw._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        nw._connection.connect(nw.GetHost())
        nw._frame._nick = nw._nick
        nw.SetState(ID_CONNECTED)
        nw.OnConnect()
    except:
        traceback.print_exc()
        nw.OnConnectionError()

def ListenThread(nw, *args):
    try:
        nw._listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        nw._listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        nw._listener.bind(nw.GetHost())
        nw._listener.listen(1)
        conn, address = nw._listener.accept()
        nw._listener.close()
        if nw.GetState() == ID_STOPLISTEN:
            conn.close()
            nw.SetState(ID_DISCONNECTED)
            return
        nw._connection = conn
        nw._frame._nick = nw._nick
        nw.SetState(ID_CONNECTED)
        nw.OnListen()
    except:
        traceback.print_exc()
        nw.OnListenError()

class OnListenEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(500001)
        self.data = data

class OnListenErrorEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(500002)
        self.data = data

class OnConnectionEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(500003)
        self.data = data

class OnConnectionErrorEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(500004)
        self.data = data

class Network():
    def __init__(self, frame):
        self._frame = frame
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listener = ''
        self._state = ID_DISCONNECTED
        self._buffer = ''
        self._host = ('', 0)
        self._handlers = dict()
        self._nick = ''
        self._thread = ''
        self.PacketHandlers()

    def SetState(self, state):
        self._state = state

    def GetState(self):
        return self._state

    def GetHost(self):
        return self._host

    def GetFrame(self):
        return self._frame

    def GetSocket(self):
        return self._connection

    def Connect(self, address, port, nick, dialog):
        self._nick = nick
        self._dialog = dialog
        self._host = (address,port)
        self.SetState(ID_CONNECTING)
        self._thread = thread.start_new_thread(ConnectThread, (self,))

    def Listen(self, port, nick, dialog):
        self._nick = nick
        self._dialog = dialog
        self._host = ('', port)
        self.SetState(ID_LISTENING)
        self._thread = thread.start_new_thread(ListenThread, (self,))

    def OnConnect(self):
        wx.PostEvent(self._dialog, OnConnectionEvent(''))
        self._thread = thread.start_new_thread(Loop, (self,))
        self.Write(ConnectPacket(self._nick, self._frame._engine.GetVersion(), 2).Build())

    def OnListen(self):
        wx.PostEvent(self._dialog, OnListenEvent(''))
        self._thread = thread.start_new_thread(Loop, (self,))
        self.Write(ConnectPacket(self._nick, self._frame._engine.GetVersion(), 1).Build())

    def OnConnectionError(self):
        wx.PostEvent(self._dialog, OnConnectionErrorEvent(''))

    def OnListenError(self):
        wx.PostEvent(self._dialog, OnListenErrorEvent(''))

    def DummyConnection(self):
        try:
            dummy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dummy.connect(('127.0.0.1',self._host[1]))
            dummy.close()
        except:
            pass

    def StopListen(self):
        try:
            self.SetState(ID_STOPLISTEN)
            self.DummyConnection()
        except:
            pass

    def StopConnect(self):
        try:
            self.SetState(ID_DISCONNECTED)
            self._connection.close()
        except:
            pass

    def Close(self):
        try:
            self.Write(packets.DisconnectPacket().Build())
            self.SetState(ID_DISCONNECTED)
            self._connection.close()
        except:
            pass

    def OnClose(self):
        try:
            self.SetState(ID_DISCONNECTED)
            self._connection.close()
        except:
            pass

    def Write(self, data, flush=True):
        self._buffer += data
        if flush:
            self.Flush()

    def Recv(self, l=4096):
        return self._connection.recv(l)

    def Flush(self):
        self._connection.sendall(self._buffer)
        self.ClearBuffer()

    def ClearBuffer(self):
        self._buffer = ''

    def GetBuffer(self):
        return self._buffer

    def Close(self):
        try:
            self._connection.close()
        except:
            pass
        self.SetState(ID_DISCONNECTED)

    def PacketHandlers(self):
        self._handlers[PACKET_CONNECT] = PacketConnectEvent
        self._frame.Connect(-1, -1, EVT_CONNECT, self._frame.OnConnectPacket)
        self._handlers[PACKET_CHAT] = PacketChatEvent
        self._frame.Connect(-1, -1, EVT_CHAT, self._frame.OnChatPacket)
        self._handlers[PACKET_DECK] = PacketDeckEvent
        self._frame.Connect(-1, -1, EVT_DECK, self._frame.OnDeckPacket)
        self._handlers[PACKET_DRAW] = PacketDrawEvent
        self._frame.Connect(-1, -1, EVT_DRAW, self._frame.OnDrawPacket)
        self._handlers[PACKET_SHUFFLE] = PacketShuffleEvent
        self._frame.Connect(-1, -1, EVT_SHUFFLE, self._frame.OnShufflePacket)
        self._handlers[PACKET_CARDMOVE] = PacketCardMoveEvent
        self._frame.Connect(-1, -1, EVT_CARDMOVE, self._frame.OnCardMovePacket)
        self._handlers[PACKET_CARDFLIP] = PacketCardFlipEvent
        self._frame.Connect(-1, -1, EVT_CARDFLIP, self._frame.OnCardFlipPacket)
        #self._handlers[PACKET_LIFECHANGE] = PacketLifeChangeEvent
        #self._frame.Connect(-1, -1, EVT_LIFECHANGE, self._frame.OnLifeChangePacket)
        self._handlers[PACKET_PHASE] = PacketPhaseEvent
        self._frame.Connect(-1, -1, EVT_PHASE, self._frame.OnPhasePacket)
        #self._handlers[PACKET_ROLL] = PacketRollEvent
        #self._frame.Connect(-1, -1, EVT_ROLL, self._frame.OnRollPacket)
        self._handlers[PACKET_DISCONNECT] = PacketDisconnectEvent
        self._frame.Connect(-1, -1, EVT_DISCONNECT, self._frame.OnDisconnectPacket)
        #self._handlers[PACKET_TARGET] = PacketTargetEvent
        #self._frame.Connect(-1, -1, EVT_TARGET, self._frame.OnTargetPacket)
        self._handlers[PACKET_FLIPCOIN] = PacketFlipCoinEvent
        self._frame.Connect(-1, -1, EVT_FLIPCOIN, self._frame.OnFlipCoinPacket)
        self._handlers[PACKET_DONEMULLIGAN] = PacketDoneMulliganingEvent
        self._frame.Connect(-1, -1, EVT_DONEMULLIGAN, self._frame.OnDoneMulliganingPacket)
        #self._handlers[PACKET_RESETGAME] = PacketResetGameEvent
        #self._frame.Connect(-1, -1, EVT_RESETGAME, self._frame.OnResetGamePacket)
        #self._handlers[PACKET_LOOK] = PacketLookEvent
        #self._frame.Connect(-1, -1, EVT_LOOK, self._frame.OnLookPacket)
        #self._handlers[PACKET_CARDACTION] = PacketCardActionEvent
        #self._frame.Connect(-1, -1, EVT_CARDACTION, self._frame.OnCardActionPacket)
        #self._handlers[PACKET_CARDCOUNTER] = PacketCardCounterEvent
        #self._frame.Connect(-1, -1, EVT_CARDCOUNTER, self._frame.OnCardCounterPacket)
        #self._handlers[PACKET_SHUFFLEHAND] = PacketShuffleHandEvent
        #self._frame.Connect(-1, -1, EVT_SHUFFLEHAND, self._frame.OnShuffleHandPacket)
        #self._handlers[PACKET_CHANGECONTROL] = PacketChangeControlEvent
        #self._frame.Connect(-1, -1, EVT_CHANGECONTROL, self._frame.OnChangeControlPacket)

    def GetHandler(self, id):
        return self._handlers[id]

    def OnPacket(self, reader):
        handler = self.GetHandler(reader.GetId())
        wx.PostEvent(self._frame, handler(reader))

    def IsConnected(self):
        if self._state == ID_CONNECTED:
            return 1
        return 0

class PacketReader():
    def __init__(self, id, length, data):
        self._index = 0
        self._id = id
        self._length = length
        self._data = data

    def GetId(self):
        return self._id

    def GetLength(self):
        return self._length

    def EOP(self):
        if self._index + 1 > self._length: return True
        else: return False

    def Read(self, fmt):
        l = struct.calcsize(fmt)
        d = struct.unpack('>'+fmt, self._data[self._index:self._index+l])[0]
        self._index += l
        return d

    def ReadInt(self):
        return int(self.Read('i'))

    def ReadFloat(self):
        return long(self.Read('f'))

    def ReadLong(self):
        return long(self.Read('l'))

    def ReadString(self):
        size = self.ReadInt()
        data = ''
        for i in range(size):
            data += chr(self.ReadInt())
        return data.decode('utf-8')

    def ReadBool(self):
        if self.ReadInt(): return True
        else: return False
