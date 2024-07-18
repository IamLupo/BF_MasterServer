from Config import readFromConfig
from Utilities.Packet import Packet
from Utilities.RandomStringGenerator import GenerateRandomString

def HandleListClubs(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "ListClubs")

    Packet(toSend).send(self, "club", 0x80000000, self.CONNOBJ.plasmaPacketID)

def HandleAddClub(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "AddClub")

    Packet(toSend).send(self, "club", 0x80000000, self.CONNOBJ.plasmaPacketID) 

def HandleUpdateMember(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "UpdateMember")

    Packet(toSend).send(self, "club", 0x80000000, self.CONNOBJ.plasmaPacketID) 


def ReceivePacket(self, data, txn):
    if txn == 'ListClubs':
        HandleListClubs(self, data)
    elif txn == 'AddClub':
        HandleAddClub(self, data)
    elif txn == 'UpdateMember':
        HandleUpdateMember(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown club message (' + txn + ")", 2)