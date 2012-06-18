import network
import struct

PACKET_CONNECT = 0
PACKET_CHAT = 1
PACKET_DECK = 2
PACKET_DRAW = 3
PACKET_SHUFFLE = 4
PACKET_CARDMOVE = 5
PACKET_CARDFLIP = 6
PACKET_LIFECHANGE = 7
PACKET_PHASE = 8
PACKET_ROLL = 9
PACKET_DISCONNECT = 10
PACKET_TARGET = 11
PACKET_FLIPCOIN = 12
PACKET_RESETGAME = 13
PACKET_LOOK = 14
PACKET_CARDACTION = 15
PACKET_CARDCOUNTER = 16
PACKET_SHUFFLEHAND = 17
PACKET_CHANGECONTROL = 18
PACKET_DONEMULLIGAN = 19

class Packet():
    def __init__(self,id):
        self._id = id
        self._buffer = []
        self._fmt = ''

    def GetId(self):
        return self._id

    def Write(self, fmt, data):
        self._fmt += fmt
        self._buffer.append(data)

    def WriteInt(self, data):
        self.Write('i', data)

    def WriteString(self, data):
        if type(data) is unicode:
            data = data.encode('utf-8')
        elif not type(data) is str:
            data = str(data)
        topack = []
        for c in data:
            topack.append(ord(c))
        self.WriteInt(len(topack))
        for b in topack:
            self.WriteInt(b)

    def WriteBool(self, data):
        if data: self.WriteInt(1)
        else: self.WriteInt(0)

    def Build(self):
        self._buffer.insert(0,self._id)
        self._buffer.insert(1,struct.calcsize(self._fmt))
        return struct.pack('>ii'+self._fmt, *self._buffer)

class ConnectPacket(Packet):
    def __init__(self, nickname, version, pid):
        Packet.__init__(self, PACKET_CONNECT)
        self.WriteString(nickname)
        self.WriteString(version)
        self.WriteInt(pid)

class ChatPacket(Packet):
    def __init__(self, message):
        Packet.__init__(self, PACKET_CHAT)
        self.WriteString(message)

class DeckPacket(Packet):
    def __init__(self, deck):
        Packet.__init__(self, PACKET_DECK)
        for c in deck:
            self.WriteString(c.CardID)

class DrawPacket(Packet):
    def __init__(self, reveal):
        Packet.__init__(self, PACKET_DRAW)
        self.WriteBool(reveal)

class ShufflePacket(Packet):
    def __init__(self, deck):
        Packet.__init__(self, PACKET_SHUFFLE)
        for c in deck:
            self.WriteString(c.GetSerial())

class ShuffleHandPacket(Packet):
    def __init__(self, hand):
        Packet.__init__(self, PACKET_SHUFFLEHAND)
        for c in hand:
            self.WriteString(c.GetSerial())

class CardMovePacket(Packet):
    def __init__(self, serial, dest, dest2=0, x=0, y=0):
        Packet.__init__(self, PACKET_CARDMOVE)
        self.WriteString(serial)
        self.WriteInt(dest)
        self.WriteInt(dest2)
        self.WriteInt(x)
        self.WriteInt(y)

class CardFlipPacket(Packet):
    def __init__(self, serial, state):
        Packet.__init__(self, PACKET_CARDFLIP)
        self.WriteString(serial)
        self.WriteInt(state)

class LifeChangePacket(Packet):
    def __init__(self, offset):
        Packet.__init__(self, PACKET_LIFECHANGE)
        self.WriteInt(offset)

class PhasePacket(Packet):
    def __init__(self, phase):
        Packet.__init__(self, PACKET_PHASE)
        self.WriteInt(phase)

class RollPacket(Packet):
    def __init__(self, faces, n):
        Packet.__init__(self, PACKET_ROLL)
        self.WriteInt(faces)
        self.WriteInt(n)

class DisconnectPacket(Packet):
    def __init__(self):
        Packet.__init__(self, PACKET_DISCONNECT)

class TargetPacket(Packet):
    def __init__(self, p, serial):
        Packet.__init__(self, PACKET_TARGET)
        self.WriteInt(p)
        self.WriteString(serial)

class FlipCoinPacket(Packet):
    def __init__(self, h):
        Packet.__init__(self, PACKET_FLIPCOIN)
        self.WriteBool(h)

class DoneMulliganingPacket(Packet):
    def __init__(self, h):
        Packet.__init__(self, PACKET_DONEMULLIGAN)
        self.WriteBool(h)

class ResetGamePacket(Packet):
    def __init__(self):
        Packet.__init__(self, PACKET_RESETGAME)

class LookPacket(Packet):
    def __init__(self, n):
        Packet.__init__(self, PACKET_LOOK)
        self.WriteInt(n)

class CardActionPacket(Packet):
    def __init__(self, action):
        Packet.__init__(self, PACKET_CARDACTION)
        self.WriteInt(action)

class CardCounterPacket(Packet):
    def __init__(self, serial, action, count):
        Packet.__init__(self, PACKET_CARDCOUNTER)
        self.WriteString(serial)
        self.WriteInt(action)
        self.WriteInt(count)

class ChangeControlPacket(Packet):
    def __init__(self, serial, action, count):
        Packet.__init__(self, PACKET_CHANGECONTROL)
        self.WriteString(serial)
        self.WriteInt(action)
        self.WriteInt(count)
