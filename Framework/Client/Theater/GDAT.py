from Globals import Clients
from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    try:
        lobbyID = str(data.get("PacketData", "LID"))
        gameID = str(data.get("PacketData", "GID"))
    except:
        lobbyID = None
        gameID = None

    if lobbyID is not None and gameID is not None:
        server = None

        for srv in Clients:
            if str(srv.serverData.get("ServerData", "LID")) == lobbyID and str(srv.serverData.get("ServerData", "GID")) == gameID:
                server = srv

        toSend = Packet().create()
        toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
        toSend.set("PacketData", "LID", lobbyID)
        toSend.set("PacketData", "GID", gameID)

        toSend.set("PacketData", "HU", str(server.personaID))
        toSend.set("PacketData", "HN", str(server.personaName))

        toSend.set("PacketData", "I", "86.87.139.235")
        toSend.set("PacketData", "P", "3658")
        toSend.set("PacketData", "N", "[XBOX360] IamLupo-Server")  # name of server in list
        toSend.set("PacketData", "AP", "0")
        toSend.set("PacketData", "MP", "24")
        toSend.set("PacketData", "JP", "0")
        toSend.set("PacketData", "PW", "0")
        toSend.set("PacketData", "TYPE", "G")
        toSend.set("PacketData", "J", "0")

        toSend.set("PacketData", "V", "1.0")
        toSend.set("PacketData", "QP", "0")

        #toSend.set("PacketData", "I", server.ipAddr)
        #toSend.set("PacketData", "P", str(server.serverData.get("ServerData", "PORT")))  # Port
        #toSend.set("PacketData", "N", str(server.serverData.get("ServerData", "NAME")))  # name of server in list
        #toSend.set("PacketData", "AP", str(server.serverData.get("ServerData", "ACTIVE-PLAYERS")))  # current number of players on server
        #toSend.set("PacketData", "MP", str(server.serverData.get("ServerData", "MAX-PLAYERS")))  # Maximum players on server
        toSend.set("PacketData", "QP", str(server.serverData.get("ServerData", "B-U-length")))  # Something with the queue...lets just set this equal to B-U-length
        #toSend.set("PacketData", "JP", str(server.serverData.get("ServerData", "JOINING-PLAYERS")))   # Players that are joining the server right now?
        #toSend.set("PacketData", "PL", "PC")  # Platform - PC / XENON / PS3

        # Constants
        #toSend.set("PacketData", "PW", "0")  # ??? - its certainly not something like "hasPassword"
        #toSend.set("PacketData", "TYPE", str(server.serverData.get("ServerData", "TYPE")))  # what type?? constant value - "G"
        #toSend.set("PacketData", "J", str(server.serverData.get("ServerData", "JOIN")))  # ??? constant value - "O"

        # Userdata
        """
        toSend.set("PacketData", "B-U-matchmaking_state", str(server.serverData.get("ServerData", "B-U-matchmaking_state")))
        toSend.set("PacketData", "B-U-team_play", str(server.serverData.get("ServerData", "B-U-team_play")))
        toSend.set("PacketData", "B-U-car_tier", str(server.serverData.get("ServerData", "B-U-car_tier")))
        toSend.set("PacketData", "B-U-game_mode", str(server.serverData.get("ServerData", "B-U-game_mode")))
        toSend.set("PacketData", "B-U-help_type", str(server.serverData.get("ServerData", "B-U-help_type")))
        toSend.set("PacketData", "B-U-player_dnf", str(server.serverData.get("ServerData", "B-U-player_dnf")))

        toSend.set("PacketData", "B-version", str(server.serverData.get("ServerData", "B-version")))  # Version of the server (exact version) - TRY TO CONNECT TO ACTUAL VERSION OF SERVER
        toSend.set("PacketData", "V", "1.0")  # "clientVersion" of server (shows up in server log on startup)
        toSend.set("PacketData", "B-U-max_online_player", str(server.serverData.get("ServerData", "B-U-max_online_player"))) 
        toSend.set("PacketData", "B-U-n2o", str(server.serverData.get("ServerData", "B-U-n2o")))
        toSend.set("PacketData", "B-U-track", str(server.serverData.get("ServerData", "B-U-track")))
        toSend.set("PacketData", "B-U-collision_detection", str(server.serverData.get("ServerData", "B-U-collision_detection")))
        toSend.set("PacketData", "B-U-version", str(server.serverData.get("ServerData", "B-U-version")))
        toSend.set("PacketData", "B-U-race_type_sprint", str(server.serverData.get("ServerData", "B-U-race_type_sprint")))
        toSend.set("PacketData", "B-U-race_type_pursuit_tag", str(server.serverData.get("ServerData", "B-U-race_type_pursuit_tag")))
        toSend.set("PacketData", "B-U-race_type_speedtrap", str(server.serverData.get("ServerData", "B-U-race_type_speedtrap")))

        toSend.set("PacketData", "B-U-game_type", str(server.serverData.get("ServerData", "B-U-game_type")))
        toSend.set("PacketData", "B-U-race_type_canyon_due", str(server.serverData.get("ServerData", "B-U-race_type_canyon_due")))
        toSend.set("PacketData", "B-U-race_type_circuit", str(server.serverData.get("ServerData", "B-U-race_type_circuit")))
        toSend.set("PacketData", "B-U-race_type_knockout", str(server.serverData.get("ServerData", "B-U-race_type_knockout")))
        toSend.set("PacketData", "B-U-length", str(server.serverData.get("ServerData", "B-U-length")))  # players in queue or maximum queue length? (sometimes smaller than QP (-1?))
        """
        Packet(toSend).send(self, "GDAT", 0x00000000, 0)

        toSend = Packet().create()
        toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
        toSend.set("PacketData", "LID", lobbyID)
        toSend.set("PacketData", "GID", gameID)
        toSend.set("PacketData", "UGID", server.serverData.get("ServerData", "UGID"))

   #     playersData = []
   #     for i in range(32):
   #         if len(str(i)) == 1:
   #             curr = "0" + str(i)
   #         else:
   #             curr = str(i)

#            pdat = server.serverData.get("ServerData", "D-pdat" + curr)

#            if pdat != "|0|0|0|0":
 #               playersData.append(pdat)

        Packet(toSend).send(self, "GDET", 0x00000000, 0)

        #for player in playersData:
         #   for playerOnServer in server.connectedPlayers:
          #      if playerOnServer.personaName == player.split('|')[0]:
           #         toSend = Packet().create()
            #        toSend.set("PacketData", "NAME", playerOnServer.personaName)
             #       toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
              #      toSend.set("PacketData", "PID", str(playerOnServer.playerID))
               #     toSend.set("PacketData", "UID", str(playerOnServer.personaID))
                #    toSend.set("PacketData", "LID", lobbyID)
                 #   toSend.set("PacketData", "GID", gameID)
                  #  Packet(toSend).send(self, "PDAT", 0x00000000, 0)
    else:
        toSend = Packet().create()
        toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
        Packet(toSend).send(self, "GDAT", 0x00000000, 0)
