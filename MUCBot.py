import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser


class MUCBot(slixmpp.ClientXMPP):
    """
        This class will be helpful to comunicate with room. 
        plugin xep_0045 is needed

        Atributes:

            jid: string expected with the jid as xmpp format
                 example string: "test@alumchat.xyz"

            password: string expected with the password for
                      authentication

            room: string expected with the jid of the rrom
                      example test@conference.alumchat.xyz

            nick: Alias of the room

        Methods:
            Start: This method is helpful to manage comunication        
    """
    def __init__(self, jid, password, room, nick):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.jid = jid
        self.room = room
        self.nick = nick

        #event handlers
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room,
                               self.muc_online)

    async def start(self, event):
        #Send events
        await self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].join_muc(self.room,
                                         self.nick,
                                         # password=the_room_password,
                                         )

        #Message to write
        message = input("Write the message: ")
        self.send_message(mto=self.room,
                          mbody=message,
                          mtype='groupchat')

    #Handle muc message
    def muc_message(self, msg):
        if(str(msg['from']).split('/')[1]!=self.nick):
            print(str(msg['from']).split('/')[1] + ": " + msg['body'])
            message = input("Write the message: ")
            self.send_message(mto=msg['from'].bare,
                              mbody=message,
                              mtype='groupchat')

    #Send message to group
    def muc_online(self, presence):
        if presence['muc']['nick'] != self.nick:
            self.send_message(mto=presence['from'].bare,
                              mbody="Hello, %s %s" % (presence['muc']['role'],
                                                      presence['muc']['nick']),
                              mtype='groupchat')
