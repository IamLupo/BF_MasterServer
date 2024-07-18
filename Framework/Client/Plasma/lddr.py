from Database import Database
from Utilities.Packet import Packet

db = Database()

def HandleListLadders(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "ListLadders")

    Packet(toSend).send(self, "lddr", 0x80000000, self.CONNOBJ.plasmaPacketID)

def ReceivePacket(self, data, txn):
    if txn == 'ListLadders':
        HandleListLadders(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown rank message (' + txn + ")", 2)