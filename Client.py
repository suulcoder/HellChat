import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser


"""
    This class will be helpful to send message and receive
    messages.

    Atributes:

        jid: string expected with the jid as xmpp format
             example string: "test@alumchat.xyz"

        password: string expected with the password for
                  authentication

        recipient: string expected with the jid as xmpp 
                   format of the recipient

        message: string expected with the message to send

    Methods:
        Start: This method is helpful to delete the user

        message: This method is helpful to recieve the message
                 and ask the user to send new message
    
"""
class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.recipient = recipient
        self.msg = message

        #Handle events
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    async def start(self, event):
        #Send presence
        self.send_presence()
        await self.get_roster()

        #Send message of type chat
        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

    def message(self, msg):
        #Print message
        if msg['type'] in ('chat'):
            recipient = msg['to']
            body = msg['body']
            
            #print the message and the recipient
            print(str(recipient) +  ": " + str(body))

            #Ask new message
            message = input("Write the message: ")

            #Send message
            self.send_message(mto=self.recipient,
                              mbody=message)