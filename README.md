# Using an existing protocol - Project 2

## Packages used
pip install sleekxmpp (version 1.3.1)

## To run program 
python proyecto2.py

## Project general description

This project consisted of creating a chat client that used an existing protocol: XMPP. I used *Python* with the library *SleekXMPP*, which is installed as mentioned above. It runs in a command line interface (CLI).

To initiate the chat you must enter your username and password registered in the server. If it is not registered, the program will automatically register the username you entered. Once you enter the chat, a menu will be displayed with 12 options:
* 1 - Show my contacts and their status
* 2 - Add user to my contacts
* 3 - Show contact details of a specific user
* 4 - Send private message to any user/contact
* 5 - Join a room (group chat)
* 6 - Leave a room (group chat)
* 7 - Send message to all members (group chat)
* 8 - Define presence message
* 9 - Send files
* 10 - Exit
* M - Show menu
* D - Delete account from server

These options are detailed below.

To use one of these functionalities, you must enter the number (or letter). In some cases you will be required either a username to send a message, a room name to create/join a group chat, or a message to send.

Also, you will be notified when one of the following activities occur:
* When you create a new account
* When you get online, you will know which users are online too
* When some user adds you to their contacts list
* When a contact changes their status and presence message
* When a contact logs in / logs out
* When you enter a group chat
* When a user/contact enters a group chat
* When you delete your account from the server

## Functionality

### Option 1

*Show my contacts and their status*

A list of your contacts (with their info) will be sent to you.

>**Example of output:**
>`msg = [1,4,1,'C','h','a','d']`

### Option 2

*Add user to my contacts*

To add a new contact, you must enter their username as shown below. The user will be notified that yu added them.

>**Example of input:**
>`Usuario: san13660`
>`** Agregado **`

### Option 3

*Show contact details of a specific user*

To show the contact details of a specific user, you must enter their username as shown below.

>**Example of input/output:**
>`Usuario: san13660`
>`**Agregado**`

### Option 4

*Send private message to any user/contact*

To send a message (1 to 1 communication), you must enter their username and the message you want to send.

>**Example of input:**
>`Usuario: san13660`
>`Mensaje: hola amigo`
>`** Mensaje enviado **`

### Option 5

*Join a room (group chat)*

To join a group chat, enter the name of the room. If it doesn't exist, the program will automatically create a new one.

>**Example of input:**
>`Nombre de la sala: grupochat`
>`** Ingresaste al grupo **`

### Option 6

*Leave a room (group chat)*

To leave a group chat, enter the name of the room.

>**Example of input:**
>`Nombre de la sala: grupochat`
>`** Saliste del grupo **`

### Option 7

*Send message to all members (group chat)*

To send a message to a group chat, enter the name of the room and the message you want to send.

>**Example of input:**
>`Nombre de la sala: grupochat`
>`Mensaje: hola companeros del grupo`
>`** Mensaje enviado **`

### Option 8

*Define presence message*

To change your presence (message and status), enter one of the 4 options for status (chat, away, xa, dnd) and the message you want to show.

>**Example of input:**
>`Estado (chat, away, xa, dnd): dnd`
>`Mensaje: no me molesten ahorita`
>`** Presencia cambiada **`

### Option 10

*Exit*

If selected, you will log out.

>**Example of output:**
>`** Cerrando sesion... **`

### Option M

*Show menu*

If selected, the menu will be displayed again.

>**Example of output:**
>`******************** OPCIONES ********************`
>`1 MOSTRAR TODOS LOS CONTACTOS Y SU ESTADO`
>`2 AGREGAR UN USUARIO A LOS CONTACTOS`
>`3 MOSTRAR DETALLES DE CONTACTO DE UN USUARIO`
>`4 COMUNICACION 1 A 1 CON CUALQUIER USUARIO/CONTACTO`
>`...`

### Option D

*Delete account from server*

If selected, your account will be removed from the server and you will be logged out.

>**Example of output:**
>`** NOTIFICACION > Usuario eliminado **`
>`** Cerrando sesion... **`

## Documentation to use SleekXMPP (and XMPP extensions)
I mainly used the following links for this project. They provide useful examples on how to use the extensions provided by XMPP.

* https://pypi.org/project/sleekxmpp/
* https://github.com/fritzy/SleekXMPP
* https://xmpp.org/extensions/