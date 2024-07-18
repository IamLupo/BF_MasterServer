from Globals import Clients

from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    toSend = Packet().create()

    tid = data.get("PacketData", "TID")
    
    toSend.set("PacketData", "NAME", "6004597505439282620")
    toSend.set("PacketData", "TID", str(tid))
    #toSend.set("PacketData", "NAME", self.CONNOBJ.personaName)

    Packet(toSend).send(self, "USER", 0x00000000, 0)