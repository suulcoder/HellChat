import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser


class Client_file(slixmpp.ClientXMPP):
    """
        This class will be helpful to send files. xep_0065 plugin is
        needed

        Atributes:

            jid: string expected with the jid as xmpp format
                 example string: "test@alumchat.xyz"

            password: string expected with the password for
                      authentication

            receiver: string expected with the jid of receiver

            filename: path of the user

        Methods:
            Start: This method is helpful to delete the user        
    """
    def __init__(self, jid, password, receiver, filename):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.receiver = receiver

        self.file = open(filename, 'rb')
        self.add_event_handler("session_start", self.start)

    async def start(self, event):
        try:
            #Set the receiver
            proxy = await self['xep_0065'].handshake(self.receiver)
            while True:
                data = self.file.read(1048576)
                if not data:
                    break
                await proxy.write(data)

            proxy.transport.write_eof()
        except (IqError, IqTimeout) as e:
            #Something went wrong
            print('File transfer errored', e)
        else:
            #File transfer
            print('File transfer finished')
        finally:
            self.file.close()
            self.disconnect()
