import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser


"""
    This class will be helpful to check if user exists

    Atributes:

        jid: string expected with the jid as xmpp format
             example string: "test@alumchat.xyz"

        password: string expected with the password for
                  authentication

    Methods:
        Start: This method is helpful to disconect the user
    
"""
class Client_exist(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        #Handle events
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.disconnect()