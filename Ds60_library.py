# -*- coding: cp1252 -*-
#-------------------------------------------------------------------------------------
#           Name: DiabloS60_library.py
#         Author: Wicker25
#    Description: Library
#        License: Attribuzione-Non commerciale-Condividi allo stesso modo 2.5 Italia
#-------------------------------------------------------------------------------------
# Molto da sistemare

import win32api
import win32con

#-----------------------------------------------------------------------

CHARSET = ["!",'"',"£","$",
           "%","&","/","(",
           ")","=","?",",",
           ",",";",".",":",
           "+","-","_","<",
           ">","*","'"]

def genchar_33(): #!
    
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(49, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0,
                         win32con.KEYEVENTF_KEYUP, 0)

def genchar_34(): #"
    
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(50, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0,
                         win32con.KEYEVENTF_KEYUP, 0)

def genchar_36(): #$
    
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(52, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0,
                         win32con.KEYEVENTF_KEYUP, 0)
    
def genchar_37(): #%
    
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(53, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0,
                         win32con.KEYEVENTF_KEYUP, 0)

def genchar_39(): #'
    
    win32api.keybd_event(219, 0, 0, 0)

def genchar_41(): #(
    
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(57, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0,
                         win32con.KEYEVENTF_KEYUP, 0)

def genchar_40(): #(
    
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(56, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0,
                         win32con.KEYEVENTF_KEYUP, 0)
    
def genchar_47(): #/
    
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(55, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0,
                         win32con.KEYEVENTF_KEYUP, 0)

def genchar_59(): #;
    
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(188, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0,
                         win32con.KEYEVENTF_KEYUP, 0)

def genchar_61(): #=
    
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(48, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0,
                         win32con.KEYEVENTF_KEYUP, 0)
    
def genchar_95(): #_
    
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(189, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0,
                         win32con.KEYEVENTF_KEYUP, 0)
    
def genchar_58(): #: 
    
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(190, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0,
                         win32con.KEYEVENTF_KEYUP, 0)
    
def genchar_63(): #?
    
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(219, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0,
                         win32con.KEYEVENTF_KEYUP, 0)
    
def genchar_38(): #& Da Controllare
    
    win32api.keybd_event(38, 0, 0, 0)

def genchar_42(): #* 

    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(187, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0,
                         win32con.KEYEVENTF_KEYUP, 0)
    
def genchar_43(): #+ 
    
    win32api.keybd_event(108, 0, 0, 0)
    
def genchar_44(): #, 
    
    win32api.keybd_event(188, 0, 0, 0)

def genchar_45(): #- 
    
    win32api.keybd_event(189, 0, 0, 0)

def genchar_46(): #. 
    
    win32api.keybd_event(110, 0, 0, 0)

def genchar_60(): #< Da Controllare
    
    win32api.keybd_event(60, 0, 0, 0)

def genchar_62(): #> Da Controllare
    
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
    win32api.keybd_event(60, 0, 0, 0)
    win32api.keybd_event(win32con.VK_SHIFT, 0,
                         win32con.KEYEVENTF_KEYUP, 0)

