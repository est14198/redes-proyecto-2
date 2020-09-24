import logging

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout


class EchoBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0047', {
            'auto_accept': True
        }) # In-band Bytestreams

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("register", self.register)
        self.add_event_handler("message", self.receive_message)
        self.add_event_handler("presence_subscribe", self.presence_subscribe)
        self.add_event_handler('presence_available', self.handle_available_new)
        self.add_event_handler('presence_dnd', self.handle_available)
        self.add_event_handler('presence_xa', self.handle_available)
        self.add_event_handler('presence_chat', self.handle_available)
        self.add_event_handler('presence_away', self.handle_available)
        self.add_event_handler('presence_unavailable', self.handle_unavailable)

        self.add_event_handler("ibb_stream_start", self.stream_opened, threaded=True)
        self.add_event_handler("ibb_stream_data", self.stream_data)


    def session_start(self, event):
        self.send_presence()
        self.get_roster()


    def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
        resp.send(now=True)
        print("\n** NOTIFICACION > Cuenta nueva creada: [ %s ] **\n" % self.boundjid)


    def unregister(self, username):
        self.plugin['xep_0077'].cancel_registration(jid=username + '@redes2020.xyz', timeout=100)
        print("\n** NOTIFICACION > Usuario eliminado **\n")


    def presence_subscribe(self, presence):
        print("\n** NOTIFICACION > [" + presence['from'].user + "] te ha agregado a sus contactos **\n")


    def receive_message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print("\n[" + msg['from'].user + "]: " + msg['body'] + "\n")


    def handle_available_new(self, pres):
        print("\n** NOTIFICACION > [" + pres['from'].user + "] conectado **\n")


    def handle_available(self, pres):
        print("\n** NOTIFICACION > [" + pres['from'].user + "] cambio estado a -" + pres['status'] + " (" + pres['show'] + ") **\n")


    def handle_unavailable(self, pres):
        print("\n** NOTIFICACION > [" + pres['from'].user + "] se ha desconectado ** \n")


    def accept_stream(self, iq):
        return True

    def stream_opened(self, stream):
        print('Archivo abierto: %s de %s' % (stream.sid, stream.peer_jid))

    def stream_data(self, event):
        print(event['data'] + "\n")
    

    def menu(self):
        print("\n******************** OPCIONES ********************\n")
        print(" 1 MOSTRAR TODOS LOS CONTACTOS Y SU ESTADO")
        print(" 2 AGREGAR UN USUARIO A LOS CONTACTOS")
        print(" 3 MOSTRAR DETALLES DE CONTACTO DE UN USUARIO")
        print(" 4 COMUNICACION 1 A 1 CON CUALQUIER USUARIO/CONTACTO")
        print(" 5 PARTICIPAR EN CONVERSACIONES GRUPALES")
        print(" 6 DEFINIR MENSAJE DE PRESENCIA")
        print(" 7 ENVIAR ARCHIVOS")
        print(" 8 SALIR")
        print(" M VOLVER A SOLICITAR EL MENU")
        print(" D ELIMINAR CUENTA\n")
        print("**********************************************************\n")


if __name__ == '__main__':

    user = input("Usuario: ")
    passwrd = input("Contrasena: ")

    # Log in
    # Si el user no existe, lo registra con los datos ingresados
    xmpp = EchoBot(user + '@redes2020.xyz', passwrd)
    xmpp.connect()
    xmpp.process(block=False)

    xmpp.menu()

    while True:

        option = input()

        # Mostrar todos los contactos y su estado
        if (option == "1"):
            groups = xmpp.client_roster.groups()
            for group in groups:
                print('\n%s' % group)
                print('-' * 72)
                for jid in groups[group]:
                    sub = xmpp.client_roster[jid]['subscription']
                    name = xmpp.client_roster[jid]['name']
                    if xmpp.client_roster[jid]['name']:
                        print(' %s (%s) ' % (name, jid))
                    else:
                        print(' %s ' % (jid))
                    connections = xmpp.client_roster.presence(jid)
                    for res, pres in connections.items():
                        show = 'available'
                        if pres['show']:
                            show = pres['show']
                        print('   - %s (%s)' % (res, show))
                        if pres['status']:
                            print('       %s' % pres['status'])

        # Agregar un usuario a los contactos
        elif (option == "2"):
            user_to_add = input("\nUsuario: ")
            xmpp.send_presence_subscription(pto=user_to_add + '@redes2020.xyz')
            print("** Agregado **")

        # Mostrar detalles de contacto de un usuario
        elif (option == "3"):
            usr = input("\nUsuario: ")
            connections = xmpp.client_roster.presence(usr + '@redes2020.xyz')
            for res, pres in connections.items():
                show = 'available'
                if pres['show']:
                    show = pres['show']
                print('   - %s (%s)' % (res, show))
                if pres['status']:
                    print('       %s' % pres['status'] + "\n")

        # Comunicacion 1 a 1 con cualquier usuario/contacto
        elif (option == "4"):
            to_user = input("\nUsuario: ")
            mssg = input("Mensaje: ")
            xmpp.send_message(mto=to_user + '@redes2020.xyz', mbody=mssg, mtype='chat')
            print("\n** Mensaje enviado **\n")

        # Definir mensaje de presencia
        elif (option == "6"):
            shw = input("\nEstado (chat, away, xa, dnd): ")
            stts = input("Mensaje: ")
            xmpp.send_presence(pshow=shw, pstatus=stts)
            print("\n** Presencia cambiada ** \n")
        
        # Volver a solicitar el menu
        elif (option == "M"):
            xmpp.menu()

        # Eliminar cuenta y desconectarse
        elif (option == "D"):
            xmpp.unregister(user)
            print("** Desconectando... **")
            break

        # Log out
        elif (option == "8"):
            print("\n** Desconectando... **")
            break

        else:
            print("\n** ESA OPCION NO EXISTE ** \n")
    
    xmpp.disconnect()