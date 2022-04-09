import signal
import socket

from utils import supplysToStr

HOST = "127.0.0.1"
PORT = 64353

LOGINUSER = "LOGINUSER"
LOGINCHAR = "LOGINCHAR"
RECEIVE = "RECEIVE"
ERROR = "ERROR"
DONATE = "DONATE"

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    return s


def serverConnect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    return s


def login(who, username, passwd):
    s = connect()

    s.send(str.encode(who+"\t"+username+"\t"+passwd))
    ret = s.recv(1024).decode()
    s.close()
    return ret

def receive(who, username):
    s = connect()

    s.send(str.encode(who +"\t" + username))
    ret = s.recv(1024).decode()
    s.close()
    return ret


def donate(who, charname, supply):
    s = connect()

    s.send(str.encode(who +"\t" + charname + "\t" + supplysToStr(supply)))
    ret = s.recv(1024).decode()
    s.close()
    return ret
