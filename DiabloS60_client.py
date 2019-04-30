#=====================================================================================
#           Name: DiabloS60_client.py
#         Author: Wicker25
#    Description: Server
#        License: Attribuzione-Non commerciale-Condividi allo stesso modo 2.5 Italia
#=====================================================================================

#-----------------------------------------------------------------------

import os
import sys
import e32
import socket
import appuifw
import binascii
from graphics import *
from key_codes import *

#-----------------------------------------------------------------------

class BTReader:
    def connect(self):
        self.sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
        addr,services=socket.bt_discover()
        print "Trovati: %s, %s"%(addr,services)
        if len(services)>0:
            import appuifw
            choices=services.keys()
            choices.sort()
            choice=appuifw.popup_menu([unicode(services[x])+": "+x
                                       for x in choices],u'Scegli Porta:')
            port=services[choices[choice]]
        else:
            port=services[services.keys()[0]]
        address=(addr,port)
        print "Connesso a "+str(address)+"...",
        self.sock.connect(address)
        print "OK." 
    def sendline(self, data):
        self.sock.send(data)
    def recvline(self, buff):
        return self.sock.recv(buff)
        
class Keyboard(object):
    def __init__(self,onevent=lambda:None):
        self._keyboard_state={}
        self._downs={}
        self._onevent=onevent
    def handle_event(self,event):
        if event['type'] == appuifw.EEventKeyDown:
            xcode=event['scancode']
            if not self.is_down(xcode):
                self._downs[xcode]=self._downs.get(xcode,0)+1
            self._keyboard_state[xcode]=1
        elif event['type'] == appuifw.EEventKeyUp:
            self._keyboard_state[event['scancode']]=0
        self._onevent()
    def is_down(self,scancode):
        return self._keyboard_state.get(scancode,0)
    def pressed(self,scancode):
        if self._downs.get(scancode,0):
            self._downs[scancode]-=1
            return True
        return False

#-----------------------------------------------------------------------

bt=BTReader()
try:
    bt.connect()
except:
    sys.exit("Fallito.")

keyboard=Keyboard()

img=None

def handle_redraw(rect):
    if img:
        canvas.blit(img)
        
appuifw.app.title=u'DiabloS60'
appuifw.app.screen='full'
appuifw.app.body=canvas=appuifw.Canvas(
    event_callback=keyboard.handle_event,
    redraw_callback=handle_redraw)

def null():
    pass

def send_string():
    global bt
    string=appuifw.query(u"Invia Stringa:", "text")
    if string != "": data="str:"+binascii.b2a_base64(string.encode("utf-8"))
    bt.sendline(data)

def start_cmd():
    global bt
    string=appuifw.query(u"Esegui:", "text")
    if string != "": data="exec:"+binascii.b2a_base64(string.encode("utf-8"))
    bt.sendline(data)

def start_cmd_standard():
    global bt
    list=[u'Blocco note',
          u'Calcolatrice',
          u'Explorer',
          u'Paint',
          u'Prompt Ms-Dos',
          u'Regedit',
          u'MsConfig']
    request=appuifw.selection_list(choices=list,search_field=1)
    if request == 0: bt.sendline("exec:"+binascii.b2a_base64("notepad"))
    if request == 1: bt.sendline("exec:"+binascii.b2a_base64("calc"))
    if request == 2: bt.sendline("exec:"+binascii.b2a_base64("explorer"))
    if request == 3: bt.sendline("exec:"+binascii.b2a_base64("mspaint"))
    if request == 4: bt.sendline("exec:"+binascii.b2a_base64("cmd"))
    if request == 5: bt.sendline("exec:"+binascii.b2a_base64("regedit"))
    if request == 6: bt.sendline("exec:"+binascii.b2a_base64("PCHealth\HelpCtr\Binaries\msconfig"))
    
def send_action():

    global bt
    list=[u'Ok (Invio)',
          u'Cambia (Tab)',
          u'Annulla (Esc)',
          u'Annulla (CTRL + Z)',
          u'Ripeti (F4)',
          u'Ripeti (CTRL + Y)',
          u'Ripeti (CTRL + SHIFT + Z)',
          u'Salva (SHIFT + F12)',
          u'Salva (CTRL + S)',
          u'Salva con nome... (CTRL + SHIFT + S)']
    request=appuifw.selection_list(choices=list,search_field=1)
    if request >= 0: bt.sendline("action:"+str(request))

def win_function():
    global bt
    list=[u'Cambia finestra',u'Chiudi finestra',u'Vai al desktop']
    request=appuifw.selection_list(choices=list,search_field=1)
    if request == 0: bt.sendline("winchange")
    if request == 1: bt.sendline("winclose")
    if request == 2: bt.sendline("godesktop")
    
def sys_function():
    global bt
    list=[u'Esegui',u'Esegui utility',u'Riavvia',u'Spegni']
    request=appuifw.selection_list(choices=list,search_field=1)
    if request == 0: start_cmd()
    if request == 1: start_cmd_standard()
    if request == 2: bt.sendline("sysrestart")
    if request == 3: bt.sendline("sysoff")

def show_info():
    appuifw.note(u"DiabloS60: Bluetooth Remote Controller","info")
    appuifw.note(u"See http://wicker25.netsons.org/ !","info")

appuifw.app.exit_key_handler=null
appuifw.app.menu = [(u"Invia stringa", send_string),
(u"Azioni comuni", send_action),
(u'Finestre', win_function),
(u'Sistema', sys_function),
(u'Informazioni', show_info),                
(u'Esci',sys.exit)]

rc_xy=(35, 13)
lc_xy=(17, 13)
left_xy=(75, 29)
right_xy=(104, 29)
up_xy=(86, 19)
down_xy=(86, 47)

if os.path.isfile("C:\\System\\Apps\\DiabloS60\\DiabloS60.app"):
    disk = u'C'
else:
    disk = u'E'
    
empty=Image.new(canvas.size)
background=Image.open(disk+u':\\System\\Apps\\DiabloS60\\image.png')
rcimg=Image.open(disk+u':\\System\\Apps\\DiabloS60\\rc.png')
lcimg=Image.open(disk+u':\\System\\Apps\\DiabloS60\\lc.png')
leftimg=Image.open(disk+u':\\System\\Apps\\DiabloS60\\left.png')
rightimg=Image.open(disk+u':\\System\\Apps\\DiabloS60\\right.png')
upimg=Image.open(disk+u':\\System\\Apps\\DiabloS60\\up.png')
downimg=Image.open(disk+u':\\System\\Apps\\DiabloS60\\down.png')

img=empty
img.blit(background)

data = []

try:

    data_rcv = bt.recvline(1024)
    if data_rcv == "securemode":
        string = appuifw.query(u"Codice di Sicurezza:", "code")
        if string != "":
            bt.sendline(binascii.b2a_base64(string.encode("utf-8")))
    
    while 1:
        
        data = [ ]

        img=empty
        img.blit(background)

        if keyboard.is_down(EScancodeLeftArrow):
            data.append("left")
            img.blit(leftimg, target=left_xy)
            
        if keyboard.is_down(EScancodeRightArrow):
            data.append("right")
            img.blit(rightimg, target=right_xy)
            
        if keyboard.is_down(EScancodeUpArrow):
            data.append("up")
            img.blit(upimg, target=up_xy)
            
        if keyboard.is_down(EScancodeDownArrow):
            data.append("down")
            img.blit(downimg, target=down_xy)

        if keyboard.is_down(165):
            data.append("rpress")
            img.blit(rcimg, target=rc_xy)
            
        if keyboard.is_down(167):
            data.append("lpress")
            img.blit(lcimg, target=lc_xy)

        if keyboard.pressed(1):
            data.append("cback")
            
        for t in range(0,10):
            if keyboard.pressed(48+t): data.append("key"+str(t))

        if not "lpress" in data:
            bt.sendline("nl")
        if not "rpress" in data:
            bt.sendline("nr")
                
        if len(data) > 0:
            for t in data: bt.sendline(t)
            
        handle_redraw(())
        e32.ao_yield()

    bt.sendline("#&#")
except:
    bt.close()

