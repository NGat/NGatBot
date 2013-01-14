#Definitions
import sys
import socket
import string
import os
HOST='chat.freenode.net'
PORT=6665
NICK='NGatBot'
IDENT='NGatBot'
REALNAME='NGatbot'
OWNER='NGat'
CHAN='#ngat'
s=socket.socket()


def connect():
    NICK = 'NGatBot'
    s.connect((HOST, PORT))
    s.send('USER '+IDENT+' '+HOST+' bla :'+REALNAME+'\r\n')
    s.send('NICK '+NICK+'\r\n')
    spam = 0
    while 1:
        line=s.recv(500)
        if line.find('Your host is ') !=-1:
            spam = 1
        if spam == 0:
            print line
        if line.find('already in use')!=-1:
            NICK = NICK + "_"
            s.send('USER '+IDENT+' '+HOST+' bla :'+REALNAME+'\r\n')
            s.send('NICK '+NICK+'\r\n')
        if line.find('End of /MOTD command')!=-1: 
            s.send('JOIN '+CHAN+'\r\n') #Joining channel
            break
def parse():
    msg = ""
    line = s.recv(500)
    man = line[1:(line.find("!"))]
    split = line.split(CHAN)
    mode = split[0].split()[-1]
    if CHAN.lower() in line:
        msg = split[1][2:]
        searcher = msg.rstrip().lower() #What to use when searching in a msg
        if line.find(".freenode.net ") ==-1:
            if mode == "PRIVMSG":
                print CHAN, man + ":", (msg).rstrip()
        if mode == "JOIN" and man != NICK: #Greeter
            s.send("PRIVMSG " + CHAN + " : Hey, " + man + ".\r\n")
            print CHAN + " NGatBot: Hey,  " + man + "."
    if searcher.find("sad") !=-1: #Hug giver
        s.send("PRIVMSG " + CHAN + " : Gives hug to " + man + ".\r\n")
        print CHAN + " NGatBot: Gives hug to " + man + "."
    if searcher == "ping":
        s.send("PRIVMSG " + CHAN + " : PONG.\r\n")
        print CHAN + " NGatBot: PONG"

connect()
while True:
    parse()
