import logging
from getpass import getpass
from argparse import ArgumentParser

import slixmpp

class SendMsg(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.recipient = recipient
        self.msg = message
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    async def start(self, event):
        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

    def message(self, msg):
        recipient = input("Write the recipient JID: ") 
        message = input("Write the message: ")
        self.send_message(mto=recipient,mbody=message)


if __name__ == '__main__':
    parser = ArgumentParser(description=SendMsg.__doc__)

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
    parser.add_argument("-t", "--to", dest="to",
                        help="JID to send the message to")
    parser.add_argument("-m", "--message", dest="message",
                        help="message to send")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = input("Username: ")
    if args.password is None:
        args.password = getpass("Password: ")

    control = True
    while control:
        # Connect to the XMPP server and start processing XMPP stanzas.
        
        print("""
-----------------------------------------------------
             WELCOME THE THE SERVER
-----------------------------------------------------
1.  Mostrar todos los usuarios/contactos
2.  Agregar un usuario a los contactos
3.  Mostrar detalles de un contacto
4.  Comunicación 1 a 1 
5.  Conversaciones grupales
6.  Definir mensaje de presencia
7.  Enviar/recibir notificaciones
8.  Enviar/recibir archivos
9.  Cerrar sesión con una cuenta
10. Eliminar la cuenta del servidor
0.  SALIR
-----------------------------------------------------
            """)
        user = input("Choose your path: ") 
        if(user=="0"):
            control = False
        if(user=="4"):
            recipient = input("Write the recipient JID: ") 
            message = input("Write the message: ")
            xmpp = SendMsg(args.jid, args.password, recipient, message)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0199') # XMPP Ping
            xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
            xmpp.register_plugin('xep_0096') # Jabber Search
            xmpp.connect()
            xmpp.process()