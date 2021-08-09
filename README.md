# HellChat
This show is a XMPP client coded with slixmpp on python 

## 1. How to run:

	python testclient.py -j <JID>

if you want to register user you must add -r parameter:

	python testclient.py -j <JID> -r true

## 2. Documentation:

### testclient.py

Main file to manage xmpp client and show menu

### Client.py

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

### Client_exist.py

This class will be helpful to check if user exists

    Atributes:

        jid: string expected with the jid as xmpp format
             example string: "test@alumchat.xyz"

        password: string expected with the password for
                  authentication

    Methods:
        Start: This method is helpful to disconect the user

### Client_file.py

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

### Client_join_group.py

This class will be helpful to subscribe to user

    Atributes:

        jid: string expected with the jid as xmpp format
             example string: "test@alumchat.xyz"

        password: string expected with the password for
                  authentication

        room_jid: string expected with the jid of the rrom
                  example test@conference.alumchat.xyz

        room_ak: Alias of the rrom

    Methods:
        Start: This method is helpful to join a group  

### Client_notification.py

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

### Client_subscripbe.py

This class will be helpful to subscribe to user

        Atributes:

            jid: string expected with the jid as xmpp format
                 example string: "test@alumchat.xyz"

            password: string expected with the password for
                      authentication

            to: string expected with the jid as xmpp 
                  format of the user

        Methods:
            Start: This method is helpful to subscribe to user

### Client_test.py

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

### Delete.py

        This class will be helpful to delte a user.

        Atributes:

            jid: string expected with the jid as xmpp format
                 example string: "test@alumchat.xyz"

            password: string expected with the password for
                      authentication

        Methods:
            Start: This method is helpful to delete the user
        

### Register.py
This class will be helpful to register a new user.

        Atributes:

            jid: string expected with the jid as xmpp format
                 example string: "test@alumchat.xyz"

            password: string expected with the password for
                      authentication

        Methods:
            Start: This method is helpful to set the presence

            