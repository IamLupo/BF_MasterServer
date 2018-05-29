# -*- coding: utf-8 -*-

from datetime import datetime
from os.path import exists

from ConfigParser import ConfigParser

from Database import Database
from Logger import Log
from Utilities.Packet import Packet

from urllib import quote

db = Database()
logger = Log("PlasmaClient", "\033[33;1m")
logger_err = Log("PlasmaClient", "\033[33;1;41m")


def HandleGetCountryList(self):
    countryList = GetCountryList(self)

    Packet(countryList).sendPacket(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)
    self.CONNOBJ.plasmaPacketID += 1


def GetCountryList(self):
    countryList = ConfigParser()
    countryList.optionxform = str
    countryList.add_section("PacketData")

    if exists("Data/countryLists/countryList_" + self.CONNOBJ.locale):
        with open("Data/countryLists/countryList_" + self.CONNOBJ.locale) as countryListFile:
            countryListData = countryListFile.readlines()
    else:
        with open("Data/countryLists/default") as countryListFile:
            countryListData = countryListFile.readlines()

    countryList.set("PacketData", "TXN", "GetCountryList")
    countryList.set("PacketData", "countryList.[]", str(len(countryListData)))

    countryId = 0
    for line in countryListData:
        countryList.set("PacketData", "countryList." + str(countryId) + ".ISOCode", line.split("=")[0])
        countryList.set("PacketData", "countryList." + str(countryId) + ".description",
                        line.split("=")[1].replace('"', "").replace("\n", ""))
        countryId += 1

    return countryList


def HandleNuGetTos(self, data):
    tos = GetTOS(self)

    Packet(tos).sendPacket(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)
    self.CONNOBJ.plasmaPacketID += 1


def GetTOS(self):
    tos = ConfigParser()
    tos.optionxform = str
    tos.add_section("PacketData")
    tos.set("PacketData", "TXN", "NuGetTos")
    tos.set("PacketData", "version", "20426_17.20426_17")

    if exists("Data/termsOfUse/termsOfUse_" + self.CONNOBJ.locale):
        with open("Data/termsOfUse/termsOfUse_" + self.CONNOBJ.locale) as termsOfUseFile:
            termsOfUse = termsOfUseFile.read()
    else:
        with open("Data/termsOfUse/default") as termsOfUseFile:
            termsOfUse = termsOfUseFile.read()

    termsOfUse = quote(termsOfUse, safe=" ,.'&/()?;®@§[]").replace("%3A", "%3a").replace("%0A",
                                                                                         "%0a") + "%0a%0a%09Battlefield%3a Bad Company 2 Master Server Emulator by B1naryKill3r%0ahttps://github.com/B1naryKill3r/BFBC2_MasterServer"
    tos.set("PacketData", "tos", termsOfUse)
    return tos


def HandleNuAddAccount(self, data):
    nuid = data.get('PacketData', 'nuid')  # Email
    password = data.get('PacketData', 'password')  # Password

    bd_Day = data.get('PacketData', 'DOBDay')
    bd_Month = data.get('PacketData', 'DOBMonth')
    bd_Year = data.get('PacketData', 'DOBYear')
    birthday = datetime.strptime(bd_Day + " " + bd_Month + " " + bd_Year, "%d %m %Y")
    timeNow = datetime.now()

    country = data.get('PacketData', 'country')

    regResult = ConfigParser()
    regResult.optionxform = str
    regResult.add_section("PacketData")
    regResult.set("PacketData", "TXN", "NuAddAccount")

    if len(nuid) > 32 or len(nuid) < 3:  # Entered user name length is out of bounds
        regResult.set("PacketData", "errorContainer.[]", "1")
        regResult.set("PacketData", "errorCode", "21")
        regResult.set("PacketData", "localizedMessage",
                      'The required parameters for this call are missing or invalid')
        regResult.set("PacketData", "errorContainer.0.fieldName", "displayName")

        if len(nuid) > 32:
            regResult.set("PacketData", "errorContainer.0.fieldError", "3")
            regResult.set("PacketData", "errorContainer.0.value", "TOO_LONG")
        else:
            regResult.set("PacketData", "errorContainer.0.fieldError", "2")
            regResult.set("PacketData", "errorContainer.0.value", "TOO_SHORT")
    elif db.checkIfEmailTaken(nuid):  # Email is already taken
        regResult.set("PacketData", "errorContainer.[]", "0")
        regResult.set("PacketData", "errorCode", "160")
        regResult.set("PacketData", "localizedMessage", 'That account name is already taken')
    elif timeNow.year - birthday.year - (
            (timeNow.month, timeNow.day) < (birthday.month, birthday.day)) < 18:  # New user is not old enough
        regResult.set("PacketData", "errorContainer.[]", "1")
        regResult.set("PacketData", "errorContainer.0.fieldName", "dob")
        regResult.set("PacketData", "errorContainer.0.fieldError", "15")
        regResult.set("PacketData", "errorCode", "21")
    else:
        db.registerUser(nuid, password, str(birthday).split(" ")[0], country)

    Packet(regResult).sendPacket(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)
    self.CONNOBJ.plasmaPacketID += 1


def ReceivePacket(self, data, txn):
    if txn == 'GetCountryList':  # User wants to create a new account
        HandleGetCountryList(self)
        logger.new_message("[" + self.ip + ":" + str(self.port) + '][acct] Received GetCountryList Request!', 2)
    elif txn == 'NuGetTos':  # Get Terms of Use
        HandleNuGetTos(self, data)
        logger.new_message("[" + self.ip + ":" + str(self.port) + '][acct] Received NuGetTos Request!', 2)
    elif txn == 'NuAddAccount':  # Final add account request (with data like email, password...)
        HandleNuAddAccount(self, data)
        logger.new_message("[" + self.ip + ":" + str(self.port) + '][acct] Received AddAccount Request!', 2)
    else:
        logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown acct message (' + txn + ")", 2)