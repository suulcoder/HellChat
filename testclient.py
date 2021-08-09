import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser  
from Register import *
from Delete import *
from Client import *
from Client_exist import *
from Client_test import *
from Client_notification import *
from Client_subscribe import *
from Client_join_group import *
from MUCBot import *
from Client_file import *


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
5.  Group Comunication                              !
6.  Define presence message                         !
7.  Send/receive notifications                      !
8.  Send/receive files                              ?
9.  Delete account                                  !
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
        if(user=='5'):
            try:
                room = input("Write the room JID: ") 
                AK = input("Write your room name: ")
                if '@conference.alumchat.xyz' in room:
                    xmpp = MUCBot(args.jid, args.password, room, AK)
                    xmpp.register_plugin('xep_0030')
                    xmpp.register_plugin('xep_0045')
                    xmpp.register_plugin('xep_0199')
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
        if(user=="7"):
            try:
                recipient = input("Write the recipient JID: ") 
                message = input("Write the message: ")
                type_ = input("Write the type: ")
                xmpp = Client_notification(args.jid, args.password, recipient, message, type_)
                xmpp.register_plugin('xep_0030') # Service Discovery
                xmpp.register_plugin('xep_0199') # XMPP Ping
                xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
                xmpp.register_plugin('xep_0096') # Jabber Search
                xmpp.connect()
                xmpp.process(forever=False)
            except KeyboardInterrupt as e:
                print('\nNice notifications, dont forget I read all of it haha\n')
                xmpp.disconnect()
        if(user=="8"):
            recipient = input("Write the recipient JID: ") 
            file = input("Write the file path : ") 
            xmpp = Client_file(args.jid, args.password, recipient, file)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0065') # SOCKS5 Bytestreams
            xmpp.connect()
            xmpp.process(forever=False)
        if(user=="9"):
            xmpp = Delete(args.jid, args.password)
            xmpp = None
            control = False
            