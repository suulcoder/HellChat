import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser  


class Register(slixmpp.ClientXMPP):
    """
        This class will be helpful to register a new user.

        Atributes:

            jid: string expected with the jid as xmpp format
                 example string: "test@alumchat.xyz"

            password: string expected with the password for
                      authentication

        Methods:
            Start: This method is helpful to set the presence
            Register: This method allows the user registration
        
    """
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.user = jid

        #Handle events
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)

    def start(self, event):
        #Set presence and get roster
        self.send_presence()
        self.get_roster()

    def register(self, iq):
        iq = self.Iq()
        iq['type'] = 'set'
        iq['register']['username'] = self.boundjid.user
        iq['register']['password'] = self.password

        #Send the iq so we can register

        try:
            iq.send()
            print("New account created", self.boundjid,"\n")
            self.disconnect()
        except IqError as e:
            #Something went wrong
            print("Error on registration ", e,"\n")
            self.disconnect()
        except IqTimeout:
            #Server is not answering
            print("THE SERVER IS NOT WITH YOU")
            self.disconnect()
        except Exception as e:
            #Something else went wrong
            print(e)
            self.disconnect()