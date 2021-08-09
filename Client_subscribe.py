import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser


class Client_subscribe(slixmpp.ClientXMPP):
    """
        This class will be helpful to subscribe to user

        Atributes:

            jid: string expected with the jid as xmpp format
                 example string: "test@alumchat.xyz"

            password: string expected with the password for
                      authentication

            to: string expected with the jid as xmpp 
                  format of the user

        Methods:
            Start: This method is helpful to subscribe to user      
    """
    def __init__(self, jid, password, to):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.to = to

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        try:
            self.send_presence_subscription(pto=self.to)        #Subscribe to user
        except IqTimeout:
            print("THE SERVER IS NOT WITH YOU") 
        self.disconnect()
        print('\n\n')
