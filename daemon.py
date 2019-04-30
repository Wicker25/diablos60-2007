#=====================================================================================
#           Name: DiabloS60_server.py
#         Author: Wicker25
#    Description: Server
#        License: Attribuzione-Non commerciale-Condividi allo stesso modo 2.5 Italia
#=====================================================================================


#-----------------------Grafica iniziale----------------------

print "="*65
print "    /-- DiabloS60 0.1.1 by Trudu Giacomo aka Wicker25"
print " ==|--- (CC) Some Right Reserved."
print "    \-- See http://wicker25.netsons.org/ for more information. "
print "="*65

#--------------------Importo qualche modulo----------------------

import os
import sys
import time
import socket
import win32api
import win32con
import binascii
from bluetooth import *
from Ds60_library import *

#--------------Informazioni sul sistema operativo-----------------

WORK_DIRECTORY = os.getcwd()

if os.path.dirname(sys.argv[0]) != "":
    WORK_DIRECTORY = os.path.dirname(sys.argv[0])
    
PATH = WORK_DIRECTORY.split(os.sep)[0]+os.sep
SYS_PATH = [os.path.join(PATH,"windows"),
            os.path.join(PATH,"windows","system32")]

sys.path.append(WORK_DIRECTORY)

#--------------Carica alcune impostazioni------------------

Xvel = 5
Yvel = 5

try:
    settings_dat = os.path.join(WORK_DIRECTORY,"settings.dat")
    file_ = open(settings_dat,"r")
    data = file_.read().split(",")
    file_.close()
    
    Xvel = int(data[0])
    Yvel = int(data[1])
except:
    pass

if Xvel < 1: Xvel = 1
if Yvel < 1: Yvel = 1
if Xvel > 99: Xvel = 45
if Yvel > 99: Yvel = 45

#--------------------Server BlueTooth--------------------

class BtServer( BluetoothSocket ):
    
    uuid = "94f39d29-7d6d-437d-973b-fba39e345f4d"

    """Il Server principale"""
    def __init__( self ):

        BluetoothSocket.__init__( self, RFCOMM )
        self.bind(( "", PORT_ANY ))
        self.listen(20)
        self.port = self.getsockname()[1]

        #Socket esterna utilizzata per eventi
        self.signal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.signal_addr = ( "localhost", 55566 )

        self.check_new_connection()
        self.close()

    """Attende una nuova connessione"""
    def check_new_connection( self ):

        advertise_service( self, "Mouse controller",
                    service_id = self.uuid,
                    service_classes = [ self.uuid, SERIAL_PORT_CLASS ],
                    profiles = [ SERIAL_PORT_PROFILE ], 
                    )

        while 1:
            
            print "In attesa di una nuova connessione.."
            self.connection, self.connection_info = self.accept()
            print "Accettata connessione dal dispositivo", self.connection_info[0]

            if not self.key_verification():

                self.connection.close()
                self.signal( "Verica fallita per "+self.connection_info[0] )
                print "Fallita."
                print "-"*60
                continue                
            
            self.signal( "Connesso a "+self.connection_info[0] )
            ServerCmd( self.connection )
            self.connection.close()
            self.signal( "Disconnesso da "+self.connection_info[0] )
            
            print "Disconnesso."
            print "-"*60

    """Chiede il codice di verifica"""
    def key_verification( self ):

        try:

            global WORK_DIRECTORY
            secure_dat = os.path.join(WORK_DIRECTORY,"secure.dat")
            hash = open(secure_dat, "r").read()
            
            if hash:

                print "Procedura di verifica ...", 
                self.connection.send("securemode")
                data = binascii.a2b_base64(self.connection.recv(1024))

                if data == hash:
                    
                    print "Connesso."
                    return True
                
            else:

                self.connection.send("nosecuremode")
                return True

        except:

            return False
        
    """Invia un segnale esterno"""
    def signal( self, data ):

        self.signal_socket.sendto( "signal:"+data, self.signal_addr )

#----------------------Gestore dei Comandi----------------------------

class ServerCmd:

    """L'interprete dei commandi"""
    def __init__(self, connection):

        self.keypressed = []
        self.connection = connection

        self.CmdLoop()

    """Loop principale"""
    def CmdLoop(self):

        global Xvel, Yvel
        
        try:
            
            while 1:

                mouse_x, mouse_y = win32api.GetCursorPos()
                
                data = self.connection.recv(1024)
                
                if data == "#&#": break
                if len(data) == 0: break
                
                if data == "up":
                    win32api.SetCursorPos(( mouse_x, mouse_y-Yvel ))
                    
                if data == "left":
                    win32api.SetCursorPos(( mouse_x-Xvel, mouse_y ))
                    
                if data == "right":
                    win32api.SetCursorPos(( mouse_x+Xvel, mouse_y ))
                    
                if data == "down":
                    win32api.SetCursorPos(( mouse_x, mouse_y+Yvel ))
                    
                if data == "rpress":
                    if not "rpress" in self.keypressed:
                        win32api.mouse_event( win32con.MOUSEEVENTF_RIGHTDOWN, 0,
                                              win32con.KEYEVENTF_EXTENDEDKEY, 0 )
                        self.keypressed.append("rpress")

                if data == "lpress":
                    if not "lpress" in self.keypressed:
                        win32api.mouse_event( win32con.MOUSEEVENTF_LEFTDOWN, 0,
                                              win32con.KEYEVENTF_EXTENDEDKEY, 0 )
                        self.keypressed.append("lpress")

                if data == "cback":
                        win32api.keybd_event(win32con.VK_BACK, 0, 0, 0)
                        
                if data == "key0":
                        win32api.keybd_event( win32con.VK_SPACE, 0, 0, 0)
                if data == "key2":
                        win32api.keybd_event( win32con.VK_UP, 0, 0, 0 )
                if data == "key4":
                        win32api.keybd_event( win32con.VK_LEFT, 0, 0, 0 )
                if data == "key6":
                        win32api.keybd_event( win32con.VK_RIGHT, 0, 0, 0 )
                if data == "key8":
                        win32api.keybd_event( win32con.VK_DOWN, 0, 0, 0 )
                if data == "key5":
                        win32api.keybd_event( win32con.VK_RETURN, 0, 0, 0 )
                        
                if data[:4] == "str:":
                    data = binascii.a2b_base64(data[4:])
                    print "Ricevuta Stringa:", data
                    for t in data:
                        if t.isspace():
                            win32api.keybd_event( win32con.VK_SPACE, 0, 0, 0 )

                        elif t.isalnum():
                        
                            if t.isupper():
                                win32api.keybd_event( win32con.VK_SHIFT, 0, 0, 0 )
                                win32api.keybd_event( ord(t), 0, 0, 0 )
                                win32api.keybd_event( win32con.VK_SHIFT, 0,
                                                 win32con.KEYEVENTF_KEYUP, 0 )
                            else:
                                win32api.keybd_event( ord(t.upper()), 0, 0, 0 )
                                
                        elif t in CHARSET:
                            globals()["genchar_"+str(ord(t))]()
                            
                        time.sleep(0.05)

                if data == "nr":
                    if "rpress" in self.keypressed:
                        win32api.mouse_event( win32con.MOUSEEVENTF_RIGHTUP, 0,
                                              win32con.KEYEVENTF_KEYUP, 0 )
                        self.keypressed.remove("rpress")
                        
                if data == "nl": 
                    if "lpress" in self.keypressed:
                        win32api.mouse_event( win32con.MOUSEEVENTF_LEFTUP, 0,
                                              win32con.KEYEVENTF_KEYUP, 0 )
                        self.keypressed.remove("lpress")

                if data[:7] == "action:":

                    key = data[7:]
                    if key == "0": # Ok (Invio)
                        win32api.keybd_event( win32con.VK_RETURN, 0, 0, 0 )
                    if key == "1": # Cambia (Tab)
                        win32api.keybd_event( win32con.VK_TAB, 0, 0, 0 )
                    if key == "2": # Annulla (Esc)
                        win32api.keybd_event( win32con.VK_ESCAPE, 0, 0, 0 )
                    if key == "3": # Annulla (CTRL + Z)
                        win32api.keybd_event( win32con.VK_LCONTROL, 0, 0, 0 )
                        win32api.keybd_event( 90, 0, 0, 0 )
                        win32api.keybd_event( win32con.VK_LCONTROL, 0,
                                              win32con.KEYEVENTF_KEYUP, 0 )
                    if key == "4": # Ripeti (F4)
                        win32api.keybd_event( win32con.VK_F4, 0, 0, 0 )
                        win32api.keybd_event( win32con.VK_F4, 0,
                                               win32con.KEYEVENTF_KEYUP, 0 )
                    if key == "5": # Ripeti (CTRL + Y)
                        win32api.keybd_event( win32con.VK_LCONTROL, 0, 0, 0 )
                        win32api.keybd_event( 89, 0, 0, 0 )
                        win32api.keybd_event( win32con.VK_LCONTROL, 0,
                                              win32con.KEYEVENTF_KEYUP, 0 )
                    if key == "6": # Ripeti (CTRL + SHIFT + Z)
                        win32api.keybd_event( win32con.VK_LCONTROL, 0, 0, 0 )
                        win32api.keybd_event( win32con.VK_LSHIFT, 0, 0, 0 )
                        win32api.keybd_event( 90, 0, 0, 0 )
                        win32api.keybd_event( win32con.VK_LCONTROL, 0,
                                              win32con.KEYEVENTF_KEYUP, 0 )
                        win32api.keybd_event( win32con.VK_LSHIFT, 0,
                                              win32con.KEYEVENTF_KEYUP, 0 )
                    if key == "7": # Salva (SHIFT + F12)
                        win32api.keybd_event( win32con.VK_LSHIFT, 0, 0, 0 )
                        win32api.keybd_event( win32con.VK_F12, 0, 0, 0 )
                        win32api.keybd_event( win32con.VK_LSHIFT, 0,
                                              win32con.KEYEVENTF_KEYUP, 0 )
                    if key == "8": # Salva (CTRL + S)
                        win32api.keybd_event( win32con.VK_LCONTROL, 0, 0, 0 )
                        win32api.keybd_event( 83, 0, 0, 0 )
                        win32api.keybd_event( win32con.VK_LCONTROL, 0,
                                              win32con.KEYEVENTF_KEYUP, 0 )
                    if key == "9": # Salva con nome... (CTRL + SHIFT + S)
                        win32api.keybd_event( win32con.VK_LCONTROL, 0, 0, 0 )
                        win32api.keybd_event( win32con.VK_LSHIFT, 0, 0, 0 )
                        win32api.keybd_event( 83, 0, 0, 0 )
                        win32api.keybd_event( win32con.VK_LCONTROL, 0,
                                              win32con.KEYEVENTF_KEYUP, 0 )
                        win32api.keybd_event( win32con.VK_LSHIFT, 0,
                                              win32con.KEYEVENTF_KEYUP, 0 )
                        
                #win function
                
                if data == "winclose" or data == "key3":
                    
                     win32api.keybd_event( win32con.VK_MENU, 0, 0, 0 )
                     win32api.keybd_event( win32con.VK_F4, 0, 0, 0 )
                     win32api.keybd_event( win32con.VK_MENU, 0,
                                          win32con.KEYEVENTF_KEYUP, 0 )

                if data == "winchange" or data == "key1":
                    
                     win32api.keybd_event( win32con.VK_MENU, 0, 0, 0 )
                     win32api.keybd_event( win32con.VK_ESCAPE, 0, 0, 0 )
                     win32api.keybd_event( win32con.VK_MENU, 0,
                                           win32con.KEYEVENTF_KEYUP, 0 )

                if data == "godesktop":
                    
                     win32api.keybd_event( win32con.VK_LWIN, 0, 0, 0 )
                     win32api.keybd_event( 68, 0, 0, 0 )
                     win32api.keybd_event( win32con.VK_LWIN, 0,
                                           win32con.KEYEVENTF_KEYUP, 0 )
                     
                #sys function
                     
                if data[:5] == "exec:":

                    path = binascii.a2b_base64(data[5:])

                    if os.path.isfile(os.path.join(SYS_PATH[0], path)):
                        path = os.path.join(SYS_PATH[0], path)
                    elif os.path.isfile(os.path.join(SYS_PATH[0], path+".com")):
                        path = os.path.join(SYS_PATH[0], path+".com")
                    elif os.path.isfile(os.path.join(SYS_PATH[0], path+".exe")):
                        path = os.path.join(SYS_PATH[0], path+".exe")
                    elif os.path.isfile(os.path.join(SYS_PATH[1], path)):
                        path = os.path.join(SYS_PATH[1], path)
                    elif os.path.isfile(os.path.join(SYS_PATH[1], path+".com")):
                        path = os.path.join(SYS_PATH[1], path+".com")
                    elif os.path.isfile(os.path.join(SYS_PATH[1], path+".exe")):
                        path = os.path.join(SYS_PATH[1], path+".exe")

                    try:
                        os.spawnl(os.P_NOWAIT, path) 
                    except:
                        print "Impossibile avviare il programma."
                    finally:
                        print "Eseguito: ", path
                    
                if data == "sysoff":

                    os.system("shutdown -s -t 00")

                if data == "sysrestart":

                    os.system("shutdown -r -t 00")

        except IOError:
            
            pass
        
        if "rpress" in self.keypressed:
            win32api.mouse_event( win32con.MOUSEEVENTF_RIGHTUP, 0,
                                  win32con.KEYEVENTF_KEYUP, 0 )
            self.keypressed.remove("rpress")
            
        if "lpress" in self.keypressed:
            win32api.mouse_event( win32con.MOUSEEVENTF_LEFTUP, 0,
                                  win32con.KEYEVENTF_KEYUP, 0 )
            self.keypressed.remove("lpress")


#-----------------------------------------------------------------------------------------
 
#Avvia il Server
Server = BtServer()

