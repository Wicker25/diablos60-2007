#=====================================================================================
#           Name: DiabloS60_server.py
#         Author: Wicker25
#    Description: Server
#        License: Attribuzione-Non commerciale-Condividi allo stesso modo 2.5 Italia
#=====================================================================================

import os
import sys
import gtk
import cairo
import gobject
import ctypes
import win32api
import win32con
from thread import *
from socket import *

gdi = ctypes.windll.gdi32
user = ctypes.windll.user32
hdc = user.GetDC(None)

#--------------Informazioni sul sistema operativo-----------------

WORK_DIRECTORY = os.getcwd()

if os.path.dirname(sys.argv[0]) != "":
    WORK_DIRECTORY = os.path.dirname(sys.argv[0])

PATH_EXE = '"'+os.path.join(WORK_DIRECTORY,"DiabloS60.exe")+'"'
PATH = WORK_DIRECTORY.split(os.sep)[0]+os.sep
SYS_PATH = [os.path.join(PATH,"windows"),
            os.path.join(PATH,"windows","system32")]

sys.path.append(WORK_DIRECTORY)

#Carica la licenza
file_ = open(os.path.join(WORK_DIRECTORY,"LICENSE.txt"), "r")
LICENSE = unicode(file_.read())
file_.close()
        
#----------------------Interfacing Socket-------------------------

class SocketInterface( socket ):

    host = "localhost"
    port = 55566
    buff = 1024
    addr = (host,port)
    
    """L'oggetto socket interfacing"""  
    def __init__( self ):
        
        socket.__init__( self, AF_INET, SOCK_DGRAM )
        self.bind( self.addr )

    """Rileva i segnali"""
    def while_signal( self ):

        while 1:

            data, addr = self.recvfrom(self.buff)
            if data[:7] == "signal:":

                if "Connesso" in data[7:]:
                    trayicon.set_tooltip("DiabloS60: "+data[7:])
                if "Disconnesso" in data[7:]:
                    trayicon.set_tooltip("DiabloS60: In Attesa...")
                def make_notify():
                    Notification( "DiabloS60", data[7:], width=185, heigth=45 )
                    
                gobject.idle_add(make_notify)

#-------------------------About Dialog--------------------------

class AboutDialog( gtk.AboutDialog ):
    
    """L'oggetto about dialog"""  
    def __init__( self ):
        
        gtk.AboutDialog.__init__( self )
        self.set_position(gtk.WIN_POS_CENTER)
        global WORK_DIRECTORY
        ico = os.path.join(WORK_DIRECTORY, "DiabloS60.ico")
        ico = gtk.gdk.pixbuf_new_from_file(ico)
        self.set_logo(ico)
        self.set_name("DiabloS60")
        self.set_version("0.1.1")
        self.set_comments("Bluetooth Remote Controller")
        self.set_wrap_license(True)
        
        global LICENSE        
        self.set_license(LICENSE)
        self.set_authors(["Trudu Giacomo aka Wicker25 - wicker25@gmail.com"])
        self.set_website("http://wicker25.netsons.org/")
        self.connect("response", lambda x, y: self.destroy())
        
        self.show_all()

#-------------------------Window Settings--------------------------

class WindowSettings( gtk.Window ):
    
    """L'oggetto about dialog"""  
    def __init__( self ):
        
        gtk.Window.__init__( self )
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("Impostazioni DiabloS60")
        #self.set_size_request(300, 200)
        self.set_resizable(0)

        vbox = gtk.VBox()
        self.add(vbox)

        #Chiave di sicurezza
        hbox = gtk.HBox()
        label = gtk.Label("Chiave di Sicurezza")
        hbox.pack_start(label, False, True, 5)       

        self.key_verify_entry = gtk.Entry(12)
        self.key_verify_entry.set_visibility(False)
        hbox.pack_start(self.key_verify_entry, False, True, 5)

        self.pwd_button = gtk.ToggleButton(label=" * ")
        self.pwd_button.connect("clicked", self.hide_show_password)
        hbox.pack_start(self.pwd_button, False, True, 5)

        vbox.pack_start(hbox, False, True, 5)    

        #Velocita' Mouse
        hbox = gtk.HBox()
        label = gtk.Label("Velocita' asse X:")
        hbox.pack_start(label, False, True, 5)       

        self.entry_x = gtk.Entry(2)
        self.entry_x.set_size_request(25, 19)
        hbox.pack_start(self.entry_x, False, True, 5)
        
        label = gtk.Label("asse Y:")
        hbox.pack_start(label, False, True, 5)       

        self.entry_y = gtk.Entry(2)
        self.entry_y.set_size_request(25, 19)
        hbox.pack_start(self.entry_y, False, True, 5)

        vbox.pack_start(hbox, False, True, 5)

        #Avvio automatico
        hbox = gtk.HBox()
        self.checkbutton = gtk.CheckButton(label="Avvio automatico alla prossima sessione di Windows")
        hbox.pack_start(self.checkbutton, False, True, 5)

        vbox.pack_start(hbox, False, True, 5)

        hbox = gtk.HBox()
        label = gtk.Label()
        label.set_markup("*<i>Alcune modifiche saranno effettive solo al prossimo avvio</i>")
        hbox.pack_start(label, False, True, 5)
        vbox.pack_start(hbox, False, True, 5)
        
        hbox = gtk.HBox(True)
        self.button = gtk.Button("Salva le modifiche")
        self.button.connect("clicked", self.save_settings)
        hbox.pack_start(self.button, False, True, 5)     
        exitbutton = gtk.Button("Chiudi")
        exitbutton.connect("clicked", lambda x: self.destroy())
        hbox.pack_start(exitbutton, False, True, 5)            

        vbox.pack_start(hbox, False, False, 5)       

        self.load_settings()        
        
        self.show_all()

    """Carica le configurazioni"""  
    def load_settings( self ):

        global WORK_DIRECTORY
        secure_dat = os.path.join(WORK_DIRECTORY,"secure.dat")
        file_ = open(secure_dat, "r")
        data = file_.read()
        file_.close() 

        self.key_verify_entry.set_text(data)
        self.read_key_registry_autostart()
        self.read_settings_dat()
        
    """Scrive il file settings.dat"""  
    def read_settings_dat( self ):

        global WORK_DIRECTORY
        settings_dat = os.path.join(WORK_DIRECTORY,"settings.dat")
        file_ = open(settings_dat, "r")
        data = file_.read().split(",")
        self.entry_x.set_text(data[0])
        self.entry_y.set_text(data[1])
        file_.close()
        
    """Scrive il file settings.dat"""  
    def write_settings_dat( self ):

        global WORK_DIRECTORY
        settings_dat = os.path.join(WORK_DIRECTORY,"settings.dat")
        file_ = open(settings_dat, "w")
        x = self.entry_x.get_text()
        y = self.entry_y.get_text()
        file_.write(x+","+y)
        file_.close() 

    """Controlla se il programma e' impostato per l'autostart"""  
    def read_key_registry_autostart( self ):

        global PATH_EXE
        data = None

        try:
            regkey = win32api.RegOpenKeyEx( win32con.HKEY_CURRENT_USER, "SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, win32con.KEY_READ )
            (data,key) = win32api.RegQueryValueEx(regkey, 'DiabloS60')
            win32api.RegCloseKey(regkey)
        except:
            pass
                
        if data == PATH_EXE:
            self.checkbutton.set_active(True)

    """Configura il programma  per l'autostart"""  
    def write_key_registry_autostart( self, opz=0):

        global PATH_EXE
        if opz:
            data = "null"
        else:
            data = PATH_EXE

        try:
            regkey = win32api.RegOpenKeyEx( win32con.HKEY_CURRENT_USER, "SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, win32con.KEY_WRITE )
            win32api.RegSetValueEx(regkey, "DiabloS60", 0, win32con.REG_SZ, data)
            win32api.RegCloseKey(regkey)
        except:
            pass
    
    """Mosta/Nasconde la password"""  
    def hide_show_password( self, event ):

        entry = self.key_verify_entry
        if entry.get_visibility():
            entry.set_visibility(False)
        else:
            entry.set_visibility(True)

    """Mosta/Nasconde la password"""  
    def hide_show_password( self, event ):

        entry = self.key_verify_entry
        if entry.get_visibility():
            entry.set_visibility(False)
        else:
            entry.set_visibility(True)
        
    """Salva le configurazioni"""  
    def save_settings( self, event ):

        data = self.key_verify_entry.get_text()

        global WORK_DIRECTORY
        secure_dat = os.path.join(WORK_DIRECTORY,"secure.dat")
        file_ = open(secure_dat, "w")
        file_.write(data)
        file_.close()

        if self.checkbutton.get_active():
            self.write_key_registry_autostart()
        else:
            self.write_key_registry_autostart(opz=1)

        self.write_settings_dat()
        self.destroy()


#-------------------------Try Icon--------------------------

class Notification( gtk.Window ):
    
    """L'oggetto finestra delle notifiche"""  
    def __init__( self , title, msg, width=200, heigth=60, color="#FFFFCC", time=2500 ):

        gtk.Window.__init__( self, gtk.WINDOW_POPUP )
        self.set_position(gtk.WIN_POS_CENTER)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(color))
        self.set_size_request(width, heigth)
        
        Res = ( gdi.GetDeviceCaps(hdc, 8), gdi.GetDeviceCaps(hdc, 10))
        self.move(Res[0]-width,Res[1]-heigth-30)
        
        frame = gtk.Frame()
        frame.set_property("border-width", 1)

        vbox = gtk.VBox()
        hbox = gtk.HBox()
        label = gtk.Label()
        label.set_markup("<b>"+title+"</b>")
        hbox.pack_start(label, False, False, 4)
        vbox.pack_start(hbox, False, True, 2)

        hbox = gtk.HBox()
        label = gtk.Label()
        label.set_markup(msg)
        hbox.pack_start(label, False, False, 4)
        vbox.pack_start(hbox, False, True, 2)
        
        frame.add(vbox)
        frame.show()
        self.add(frame)        
        
        gobject.timeout_add(time, lambda x, y, z: self.destroy(), self, self, self)
        
        self.show_all()
    
class TrayIcon( gtk.StatusIcon ):
    
    """L'oggetto tray icon"""  
    def __init__( self ):
        
        gtk.StatusIcon.__init__(self)
        
        global WORK_DIRECTORY
        DiabloS60_ico = os.path.join(WORK_DIRECTORY,"DiabloS60.ico")
        self.set_from_file(DiabloS60_ico)
        self.connect('popup-menu', self.__show_menu)
        self.set_tooltip("DiabloS60: In Attesa...")
        
        self.menu = None
        self.window_settings = None
        self.aboutdialog = None
        
    """Apre il menu' delle opzioni nella tray icon"""  
    def __show_menu( self, icon, button, activate_time ):

        if self.menu: self.menu.destroy()
        self.menu = gtk.Menu()

        def _null(w):
            pass
        
        def _make_window_settings(w):

            if self.window_settings: self.window_settings.destroy()
            self.window_settings = WindowSettings()
            
        def _make_aboutdialog(w):

            if self.aboutdialog: self.aboutdialog.destroy()
            self.aboutdialog = AboutDialog()

        def _exit(w):

            try:
                global daemon_pid
                win32api.TerminateProcess(daemon_pid, 0)
            except: pass
            
            self.set_visible(False)
            sys.exit()

        list_func = (
                     ( 0, gtk.STOCK_PREFERENCES, _make_window_settings),
                     ( 0, gtk.STOCK_ABOUT, _make_aboutdialog),
                     ( 0, gtk.STOCK_QUIT, _exit),
                    )
        #( 1, "<-", _null),
        
        for key in list_func:

            if key[0]:
                item = gtk.MenuItem(label=key[1])
            else:
                item = gtk.ImageMenuItem(key[1])
                
            item.connect("activate", key[2])
            item.show()
            self.menu.append(item)
        
        gobject.idle_add(self.menu.popup, None, None, None, button, activate_time, self)
        self.time_out_id = gobject.timeout_add(2300, lambda x, y, z: self.menu.destroy(), self, self, self)

        def _close_menu(w, e):
            gobject.idle_add(self.menu.popdown)

        def _redtime_menu(w, e):
            gobject.source_remove(self.time_out_id)
            self.time_out_id = gobject.timeout_add(2000, lambda x, y, z: self.menu.destroy(), self, self, self)

        #'focus-out-event'
        self.menu.connect('enter-notify-event', _redtime_menu)

#-----------------------------------------------------------------------------------------

#log_txt = os.path.join(WORK_DIRECTORY,"log.txt")
#sys.stout = open(log_txt,"w")
#sys.stderr = sys.stout

demon_exe = os.path.join(WORK_DIRECTORY,"daemon.exe")
daemon_pid = os.spawnl(os.P_NOWAIT, demon_exe)

socket = SocketInterface()
start_new_thread(socket.while_signal, ())

def make_trayicon():
    global trayicon
    trayicon = TrayIcon()
    
gobject.idle_add(make_trayicon)

#Messaggio di benvenuto
def show_notification():
    
    Notification("DiabloS60", "DiabloS60 e' in attesa di stabilire una\nnuova connessione!")
                        
gobject.idle_add(show_notification)

while 1:
    while gtk.events_pending():
        gtk.main_iteration(False)

