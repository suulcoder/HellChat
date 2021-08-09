import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser


class Client_notification(slixmpp.ClientXMPP):
    """
        This class will be helpful to send notifications

        Atributes:

            jid: string expected with the jid as xmpp format
                 example string: "test@alumchat.xyz"

            password: string expected with the password for
                      authentication

            user: string expected with the jid as xmpp 
                  format of the recipient, should not be
                  empty if you are asking for the details
                  of user  

            message: String expected, the message of the presence. 

            type_: String expected with the notification type

        Methods:
            Start: This method is helpful to delete the user
            notification: message notificaiton handler
        
    """
    def __init__(self, jid, password, user, message, type_):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        #Add events handlers
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.message = message
        self.user = user
        self.type_ = type_

    async def start(self, event):
        #Send presence
        self.send_presence()
        await self.get_roster()

        #Send notification
        self.notification_(self.user, self.message, 'active')

    def notification_(self, to, body, my_type):
        """
        Paramentesr:

            to: string expected with the jid as xmpp format
                 example string: "test@alumchat.xyz"

            body: String expected, the message of the presence. 

            my_type: String expected with the notification type
        """
        
        #Create stanza
        message = self.Message()
        message['to'] = to
        message['type'] = self.type_
        message['body'] = body

        #Handle type by stanza
        if (my_type == 'active'):
            fragmentStanza = ET.fromstring("<active xmlns='http://jabber.org/protocol/chatstates'/>")
        elif (my_type == 'composing'):
            fragmentStanza = ET.fromstring("<composing xmlns='http://jabber.org/protocol/chatstates'/>")
        elif (my_type == 'inactive'):
            fragmentStanza = ET.fromstring("<inactive xmlns='http://jabber.org/protocol/chatstates'/>")
        message.append(fragmentStanza)

        try:
            message.send()
        except IqError as e:
            print("Somethiing went wrong\n", e)
        except IqTimeout:
            print("THE SERVER IS NOT WITH YOU")

    #Print message
    def message(self, msg):
        recipient = msg['to']
        body = msg['body']
        print(str(recipient) +  ": " + str(body))
        #message = input("Write the message: ")
        #self.send_message(mto=self.recipient,
        #                  mbody=message)
