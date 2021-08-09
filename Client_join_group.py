import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser


class Client_join_group(slixmpp.ClientXMPP):
    """
        This class will be helpful to subscribe to user

        Atributes:

            jid: string expected with the jid as xmpp format
                 example string: "test@alumchat.xyz"

            password: string expected with the password for
                      authentication

            room_jid: string expected with the jid of the rrom
                      example test@conference.alumchat.xyz

            room_ak: Alias of the rrom

        Methods:
            Start: This method is helpful to join a group      
    """
    def __init__(self, jid, password, room_jid, room_ak):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        #Handle events
        self.add_event_handler("session_start", self.start)
        self.room = room_jid
        self.ak = room_ak

    async def start(self, event):
        #Send presence
        self.send_presence()
        await self.get_roster()
        try:
            #Join room
            self.plugin['xep_0045'].join_muc(self.room, self.ak)
            print("YOU ARE ON THE GROUP NOW")
        except IqError as e:
            print("Something went wrong", e)
        except IqTimeout:
            print("THE SERVER IS NOT WITH YOU")
        self.disconnect()
