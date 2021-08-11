import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser

"""
        This class will be helpful to delte a user.

        Atributes:

            jid: string expected with the jid as xmpp format
                 example string: "test@alumchat.xyz"

            password: string expected with the password for
                      authentication

        Methods:
            Start: This method is helpful to delete the user
        
    """
class Delete(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.user = jid
        #Handle events
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        #Send presence
        self.send_presence()
        self.get_roster()

        #Define the iq and the stanza
        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = self.user
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        delete.append(fragment)

        try:
            #Send the delete iq
            delete.send(now=True)
            print("Account deleted")
        except IqError as e:
            #Something went wrong on deletition
            print("Error on deletition", e)
        except IqTimeout:
            #Server is not answering
            print("THE SERVER IS NOT WITH YOU")
        except Exception as e:
            #Something else is wrong
            print(e)  
        #Disconnect the user in case something is wrong
        self.disconnect()