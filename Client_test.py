import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser


class Client_test(slixmpp.ClientXMPP):
    """
        This class will be helpful to send check all the users
        and send the presence to everyone, also is helpful to 
        show the details of an specific user. 

        Atributes:

            jid: string expected with the jid as xmpp format
                 example string: "test@alumchat.xyz"

            password: string expected with the password for
                      authentication

            user: string expected with the jid as xmpp 
                  format of the recipient, should not be
                  empty if you are asking for the details
                  of user  

            show: boolean expected true if you want details of 
                  user or users, should be false if you want to
                  send the presence message.

            message: String expected, the message of the presence. 

        Methods:
            Start: This method is helpful to delete the user
        
    """
    def __init__(self, jid, password, user=None, show=True, message=""):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        #Handle events
        self.add_event_handler("session_start", self.start)
        self.presences = threading.Event()
        self.contacts = []
        self.user = user
        self.show = show
        self.message = message

    async def start(self, event):
        #Send presence
        self.send_presence()
        await self.get_roster()

        my_contacts = []
        try:
            #Check the roster
            self.get_roster()
        except IqError as e:
            #If there is an error
            print("Something went wrong", e)
        except IqTimeout:
            #Server error
            print("THE SERVER IS NOT WITH YOU")
        
        #Wait for presences
        self.presences.wait(3)

        #For each client on roster
        my_roster = self.client_roster.groups()
        for group in my_roster:
            for user in my_roster[group]:
                status = show = answer = priority = ''
                self.contacts.append(user)
                subs = self.client_roster[user]['subscription']                         #Get subscription
                conexions = self.client_roster.presence(user)                           
                username = self.client_roster[user]['name']                             #Get username
                for answer, pres in conexions.items():
                    if pres['show']:
                        show = pres['show']                                             #Get show
                    if pres['status']:
                        status = pres['status']                                         #Get status
                    if pres['priority']:
                        priority = pres['priority']                                     #Get priority

                my_contacts.append([
                    user,
                    subs,
                    status,
                    username,
                    priority
                ])
                self.contacts = my_contacts

        #If want to show the details of user or users
        if(self.show):

            #If want to show message of eveyone
            if(not self.user):

                #Check if it is empty
                if len(my_contacts)==0:
                    print('NO CONTACTS CONNECTED')
                else:
                    print('\n USERS: \n\n')

                #Print all
                for contact in my_contacts:
                    print('\tJID:' + contact[0] + '\t\tSUBSCRIPTION:' + contact[1] + '\t\tSTATUS:' + contact[2])
            
            #If want to show message of specific user
            else:
                print('\n\n')
                for contact in my_contacts:
                    if(contact[0]==self .user):
                        print('\tJID:' + contact[0] + '\n\tSUBSCRIPTION:' + contact[1] + '\n\tSTATUS:' + contact[2] + '\n\tUSERNAME:' + contact[3] + '\n\tPRIORITY:' + contact[4])
        
        #If want to send presence message
        else:
            for JID in self.contacts:
                self.notification_(JID, self.message, 'active')

        self.disconnect()
        print('\n\n')

    def notification_(self, to, body, my_type):

        message = self.Message()
        message['to'] = to
        message['type'] = 'chat'
        message['body'] = body

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
