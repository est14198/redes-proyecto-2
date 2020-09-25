# Universidad del Valle de Guatemala
# Redes - Seccion 10
# Maria Fernanda Estrada 14198
# Proyecto 2 - Usando un protocolo existente
# 24/09/2020


# Librerias
import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout


# Inicializando EchoBot
class EchoBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        # Nickname para grupos
        self.nick = "mynickname"

        # Plugins utilizados
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0047', {
            'auto_accept': True
        }) # In-band Bytestreams
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0199') # XMPP Ping

        # Handler de eventos
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
        self.add_event_handler("groupchat_message", self.muc_message_receive)

        self.add_event_handler("ibb_stream_start", self.stream_opened, threaded=True)
        self.add_event_handler("ibb_stream_data", self.stream_data)


    # Iniciar sesion
    def session_start(self, event):
        self.send_presence()
        self.get_roster()


    # Registrar un nuevo usuario si al ingresar no existe
    def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
        resp.send(now=True)
        print("\n** NOTIFICACION > Cuenta nueva creada: [ %s ] **\n" % self.boundjid)


    # Eliminar cuenta del server
    def unregister(self, username):
        self.plugin['xep_0077'].cancel_registration(jid=username + '@redes2020.xyz', timeout=100)
        print("\n** NOTIFICACION > Usuario eliminado **\n")


    # Mostrar notificacion cuando alguien me agrega de contacto
    def presence_subscribe(self, presence):
        print("\n** NOTIFICACION > [" + presence['from'].user + "] te ha agregado a sus contactos **\n")


    # Mostrar mensaje que me envian 1 a 1
    def receive_message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print("\n[" + msg['from'].user + "]: " + msg['body'] + "\n")


    # Mostrar notificacion cuando alguien esta disponible
    def handle_available_new(self, pres):
        print("\n** NOTIFICACION > [" + pres['from'].user + "] disponible **\n")


    # Mostrar notificacion cuando alguien cambia su presencia
    def handle_available(self, pres):
        print("\n** NOTIFICACION > [" + pres['from'].user + "] cambio estado a -" + pres['status'] + " (" + pres['show'] + ") **\n")


    # Mostrar notificacion cuando alguien se desconecta
    def handle_unavailable(self, pres):
        print("\n** NOTIFICACION > [" + pres['from'].user + "] no disponible ** \n")

    
    # Ingresar a un grupo. Si no existe, lo crea. Si ya existe, solo ingresa
    def join_group(self, room):
        self.plugin['xep_0045'].joinMUC(room, self.nick)
        try:
            self.plugin['xep_0045'].configureRoom(room)
            print('')
        except ValueError:
            print('')
        print("\n** Ingresaste al grupo **\n")


    # Salir de grupo
    def leave_group(self, room):
        self.plugin['xep_0045'].leaveMUC(room, self.nick)


    # Recibir mensajes de un grupo
    def muc_message_receive(self, msg):
        print('[{}][{}] {} \n'.format(msg['from'].bare, msg['mucnick'], msg['body']))


    # Enviar mensaje a un grupo
    def send_group_msg(self, group, msg):
        self.send_message(mto=group, mbody=msg, mtype='groupchat')


    # Aceptar archivos de txt
    def accept_stream(self, iq):
        return True


    # Mostrar quien envio el archivo
    def stream_opened(self, stream):
        print('\n** NOTIFICACION > Archivo abierto: %s' % (stream.sid))


    # Mostrar data de archivos
    def stream_data(self, event):
        f = open("my_new_file.txt", "wb")
        f.write(event['data'])
        f.close()
        print("")

    # Enviar un archivo
    def send_file(self, receiver, file_name):
        try:
            stream = self['xep_0047'].open_stream(receiver)
            with open(file_name) as f:
                data = f.read()
                stream.sendall(data)
            print('\n** NOTIFICACION > Archivo enviado **')
        except:
            print('\n** NOTIFICACION > No se pudo enviar el archivo **')
    
    # Menu de opciones
    def menu(self):
        print("\n******************** OPCIONES ********************\n")
        print(" 1 MOSTRAR TODOS LOS CONTACTOS Y SU ESTADO")
        print(" 2 AGREGAR UN USUARIO A LOS CONTACTOS")
        print(" 3 MOSTRAR DETALLES DE CONTACTO DE UN USUARIO")
        print(" 4 COMUNICACION 1 A 1 CON CUALQUIER USUARIO/CONTACTO")
        print(" 5 UNIRSE A UN GRUPO")
        print(" 6 SALIR DE UN GRUPO")
        print(" 7 ENVIAR MENSAJE GRUPAL")
        print(" 8 DEFINIR MENSAJE DE PRESENCIA")
        print(" 9 ENVIAR ARCHIVO")
        print(" 10 SALIR")
        print(" M VOLVER A SOLICITAR EL MENU")
        print(" D ELIMINAR CUENTA\n")
        print("**********************************************************\n")


if __name__ == '__main__':

    # Ingresar usuario y contrasena
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

        # Unirse a un grupo
        elif (option == "5"):
            rm_join = input("\nNombre de la sala: ")
            xmpp.join_group(rm_join + '@conference.redes2020.xyz')
        
        # Salirse de un grupo
        elif (option == "6"):
            rm_getout = input("\nNombre de la sala: ")
            xmpp.leave_group(rm_getout + '@conference.redes2020.xyz')
            print("\n** Saliste del grupo **\n")

        # Enviar mensaje grupal
        elif (option == "7"):
            rm_msg = input("\nNombre de la sala: ")
            msg_body = input("\nMensaje: ")
            xmpp.send_message(mto=rm_msg + '@conference.redes2020.xyz', mbody=msg_body, mtype='groupchat')
            print("\n** Mensaje enviado **\n")

        # Definir mensaje de presencia
        elif (option == "8"):
            shw = input("\nEstado (chat, away, xa, dnd): ")
            stts = input("Mensaje: ")
            xmpp.send_presence(pshow=shw, pstatus=stts)
            print("\n** Presencia cambiada ** \n")
        
        # Enviar archivo
        elif (option == "9"):
            recvr = input("\nUsuario: ")
            resrc = input("Recurso: ")
            filepath = input("Nombre del archivo: ")
            xmpp.send_file(recvr + "@redes2020.xyz/" + resrc, filepath)
        
        # Volver a solicitar el menu
        elif (option == "M"):
            xmpp.menu()

        # Eliminar cuenta y desconectarse
        elif (option == "D"):
            xmpp.unregister(user)
            print("** Cerrando sesion... **")
            break

        # Log out
        elif (option == "10"):
            print("\n** Cerrando sesion... **")
            break

        else:
            print("\n** ESA OPCION NO EXISTE ** \n")
    
    xmpp.disconnect()