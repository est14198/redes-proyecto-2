import logging

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout


class EchoBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.receive_message)
        self.add_event_handler("presence_subscribe", self.presence_subscribe)

        # If you wanted more functionality, here's how to register plugins:
        # self.register_plugin('xep_0030') # Service Discovery
        # self.register_plugin('xep_0199') # XMPP Ping

        # Here's how to access plugins once you've registered them:
        # self['xep_0030'].add_feature('echo_demo')

        # If you are working with an OpenFire server, you will
        # need to use a different SSL version:
        # import ssl
        # self.ssl_version = ssl.PROTOCOL_SSLv3

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

        # Most get_*/set_* methods from plugins use Iq stanzas, which
        # can generate IqError and IqTimeout exceptions
        #
        # try:
        #     self.get_roster()
        # except IqError as err:
        #     logging.error('There was an error getting the roster')
        #     logging.error(err.iq['error']['condition'])
        #     self.disconnect()
        # except IqTimeout:
        #     logging.error('Server is taking too long to respond')
        #     self.disconnect()

    def presence_subscribe(self, presence):
        print("[" + presence['from'].user + "] te ha agregado a sus contactos")

    def receive_message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print("[" + msg['from'].user + "]: " + msg['body'])
    
    def menu(self):
        print("\n******************** OPCIONES DEL CHAT ********************\n")
        print(" 1. MOSTRAR TODOS LOS USUARIOS/CONTACTOS Y SU ESTADO")
        print(" 2. AGREGAR UN USUARIO A LOS CONTACTOS")
        print(" 3. MOSTRAR DETALLES DE CONTACTO DE UN USUARIO")
        print(" 4. COMUNICACION 1 A 1 CON CUALQUIER USUARIO/CONTACTO")
        print(" 5. PARTICIPAR EN CONVERSACIONES GRUPALES")
        print(" 6. DEFINIR MENSAJE DE PRESENCIA")
        print(" 7. ENVIAR/RECIBIR NOTIFICACIONES")
        print(" 8. ENVIAR/RECIBIR ARCHIVOS")
        print(" 9. SALIR\n")
        print("**********************************************************\n")


if __name__ == '__main__':
    # Ideally use optparse or argparse to get JID,
    # password, and log level.

    #logging.basicConfig(level=logging.DEBUG,
        #format='%(levelname)-8s %(message)s')

    user = input("Usuario: ")
    passwrd = input("Contrasena: ")

    xmpp = EchoBot(user + '@redes2020.xyz', passwrd)
    xmpp.connect()
    xmpp.process(block=False)

    while True:

        xmpp.menu()
        option = input("Ingresa la opcion: ")

        # Agregar un usuario a los contactos
        if (option == "2"):
            user_to_add = input("Usuario: ")
            xmpp.send_presence_subscription(pto=user_to_add + '@redes2020.xyz')
            print("Agregado")

        # Comunicacion 1 a 1 con cualquier usuario/contacto
        if (option == "4"):
            to_user = input("Usuario: ")
            mssg = input("Mensaje: ")
            xmpp.send_message(mto=to_user + '@redes2020.xyz', mbody=mssg, mtype='chat')
            print("Mensaje enviado")

        # Definir mensaje de presencia
        if (option == "6"):
            shw = input("Estado (chat, away, xa, dnd): ")
            stts = input("Mensaje: ")
            xmpp.send_presence(pshow=shw, pstatus=stts)
            print("Presencia cambiada")

        elif (option == "9"):
            print("\nDesconectando...")
            break
    
    xmpp.disconnect()