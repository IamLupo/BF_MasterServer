import time
from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    toSend = Packet().create()
	

    tid = data.get("PacketData", "TID")
    prot = data.get("PacketData", "PROT")

    toSend.set("PacketData", "PROT", prot)
    toSend.set("PacketData", "TIME", str(int(time.time())))
    toSend.set("PacketData", "TID", str(tid))
    
    Packet(toSend).send(self, "CONN", 0x00000000, 0)
