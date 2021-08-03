import logging
import threading
import slixmpp

from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser


class Register(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.user = jid
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.disconnect()

    def register(self, iq):
        iq = self.Iq()
        iq['type'] = 'set'
        iq['register']['username'] = self.boundjid.user
        iq['register']['password'] = self.password

        try:
            iq.send()
            print("New account created", self.boundjid,"\n")
        except IqError as e:
            print("Error on registration ", e,"\n")
            self.disconnect()
        except IqTimeout:
            print("THE SERVER IS NOT WITH YOU")
            self.disconnect()
        except Exception as e:
            print(e)
            self.disconnect()  

    def delete_account(self):
        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = self.user
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        delete.append(fragment)

        try:
            delete.send()
            print("Account deleted")
        except IqError as e:
            print("Error on deletition", e)
        except IqTimeout:
            print("THE SERVER IS NOT WITH YOU")
        except Exception as e:
            print(e)  

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.recipient = recipient
        self.msg = message
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

    def message(self, msg):
        if msg['type'] in ('chat'):
            recipient = msg['to']
            body = msg['body']
            print(str(recipient) +  ": " + str(body))
            message = input("Write the message: ")
            self.send_message(mto=self.recipient,
                              mbody=message)

class Client_exist(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        self.disconnect()

class Client_test(slixmpp.ClientXMPP):
    def __init__(self, jid, password, user=None, show=True, message=""):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.presences = threading.Event()
        self.contacts = []
        self.user = user
        self.show = show
        self.message = message

    async def start(self, event):
        self.send_presence()
        await self.get_roster()

        my_contacts = []
        try:
            self.get_roster()
        except IqError as e:
            print("Something went wrong", e)
        except IqTimeout:
            print("THE SERVER IS NOT WITH YOU")
        
        self.presences.wait(3)

        my_roster = self.client_roster.groups()
        for group in my_roster:
            for user in my_roster[group]:
                status = show = answer = priority = ''
                self.contacts.append(user)
                subs = self.client_roster[user]['subscription']
                conexions = self.client_roster.presence(user)
                username = self.client_roster[user]['name'] 
                for answer, pres in conexions.items():
                    if pres['show']:
                        show = pres['show']
                    if pres['status']:
                        status = pres['status']
                    if pres['priority']:
                        status = pres['priority']

                my_contacts.append([
                    user,
                    subs,
                    status,
                    username,
                    priority
                ])
                self.contacts = my_contacts

        if(self.show):
            if(not self.user):
                if len(my_contacts)==0:
                    print('NO CONTACTS CONNECTED')
                else:
                    print('\n USERS: \n\n')
                for contact in my_contacts:
                    print('\tJID:' + contact[0] + '\t\tSUBSCRIPTION:' + contact[1] + '\t\tSTATUS:' + contact[2])
            else:
                print('\n\n')
                for contact in my_contacts:
                    if(contact[0]==self .user):
                        print('\tJID:' + contact[0] + '\n\tSUBSCRIPTION:' + contact[1] + '\n\tSTATUS:' + contact[2] + '\n\tUSERNAME:' + contact[3] + '\n\tPRIORITY:' + contact[4])
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

class Client_subscribe(slixmpp.ClientXMPP):
    def __init__(self, jid, password, to):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.to = to

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        try:
            self.send_presence_subscription(pto=self.to) 
        except IqTimeout:
            print("THE SERVER IS NOT WITH YOU") 
        self.disconnect()
        print('\n\n')

if __name__ == '__main__':
    parser = ArgumentParser(description=Client.__doc__)

    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")
    parser.add_argument("-r", "--register", dest="register",
                        help="Is new user")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = input("Username: ")
    if args.password is None:
        args.password = getpass("Password: ")

    if (args.register) is not None:
            xmpp = Register(args.jid, args.password)
            xmpp.register_plugin('xep_0030') ### Service Discovery
            xmpp.register_plugin('xep_0004') ### Data Forms
            xmpp.register_plugin('xep_0066') ### Band Data
            xmpp.register_plugin('xep_0077') ### Band Registration

            xmpp.connect()
            xmpp.process(forever=False)
            print("Registration Done\n")

    control = True
    while control:
        print("""
-----------------------------------------------------
             WELCOME THE THE SERVER
-----------------------------------------------------
NOTE: Your credentials might be wrong, this interface
does not show that you are already logged in
-----------------------------------------------------
1.  Show all contacts                               !
2.  Add user to cantacts                            !
3.  Show details of a contact                       !
4.  Comunication 1 to 1                             !
5.  Group comunication
6.  Define presence message                         !
7.  Send/receive notifications
8.  Send/receive files
9.  Delete account                                  ?
0.  Logout                                          !
-----------------------------------------------------
            """)
        user = input("Choose your path: ") 
        if(user=="0"):
            control = False
            print('\nGoodbye! :(\n')
        if(user=="1"):
            xmpp = Client_test(args.jid, args.password)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0199') # XMPP Ping
            xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            xmpp.register_plugin('xep_0096') # Jabber Search
            xmpp.connect()
            xmpp.process(forever=False)
        if(user=="2"):
            contact = input("Write the contact JID: ") 
            xmpp = Client_subscribe(args.jid, args.password, contact)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0199') # XMPP Ping
            xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            xmpp.register_plugin('xep_0096') # Jabber Search
            xmpp.connect()
            xmpp.process(forever=False)
        if(user=="3"):
            contact = input("Write the contact JID: ") 
            xmpp = Client_test(args.jid, args.password, contact)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0199') # XMPP Ping
            xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            xmpp.register_plugin('xep_0096') # Jabber Search
            xmpp.connect()
            xmpp.process(forever=False)
        if(user=="4"):
            try:
                recipient = input("Write the recipient JID: ") 
                message = input("Write the message: ")
                xmpp = Client(args.jid, args.password, recipient, message)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                xmpp.register_plugin('xep_0096') # Jabber Search
                xmpp.connect()
                xmpp.process(forever=False)
            except KeyboardInterrupt as e:
                print('\nNice chat, dont forget I read all of it haha\n')
                xmpp.disconnect()
        if(user=="6"):
            message = input("Write the presence message : ") 
            xmpp = Client_test(args.jid, args.password, show=False, message=message)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0199') # XMPP Ping
            xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            xmpp.register_plugin('xep_0096') # Jabber Search
            xmpp.connect()
            xmpp.process(forever=False)
        if(user=="9"):
            xmpp = Register(args.jid, args.password)
            xmpp.delete_account()
            xmpp = None
            control = False
            