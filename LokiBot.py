#Definitions
import sys
import socket
import string
import os
import pickle
import re
HOST = 'irc.esper.net'
PORT = 6665
NICK = 'LokiBot'
IDENT = 'LokiBot'
REALNAME = 'NGatbot'
OWNER = 'Loki456789'
CHAN = '#tornkingdom'
s = socket.socket()
s.connect((HOST, PORT))
s.send('NICK '+NICK+'\r\n')
s.send('USER '+IDENT+' '+HOST+' bla :'+REALNAME+'\r\n')
while 1:
  line=s.recv(500) #Getting data
  if line.startswith("PING"):
    s.send("PONG " + line.split()[1]+"\r\n")
    print "PONG " + line.split()[1]
  if line.find('already in use')!=-1:
        NICK = NICK + "_"
        s.send('USER '+IDENT+' '+HOST+' bla :'+REALNAME+'\r\n')
        s.send('NICK '+NICK+'\r\n')
  print line
  s.send('JOIN '+CHAN+'\r\n')
  if line.find(CHAN)!=-1:
      break
while True:
    ### MANAGING CHAT ###
    line = s.recv(500) #Getting data
    man = line[1:(line.find("!"))] #Person who sent the line
    split = line.split(CHAN) #Splitting the IP etc. from the message
    mode = split[0].split()[-1] #Getting whether it is a PRIVMSG, JOIN, etc
    if line.find('Join TK')!=-1:
      s.send('JOIN '+CHAN+'\r\n')
    if CHAN.lower() in line:
        msg = split[1][2:]
        match = re.search(r"...\[...G...\] ...\[...(.*?)...\] ...(.*?)......:... (.*)", msg)
        if match:
          msg = match.group(3)
          man = match.group(2)
        searcher = msg.rstrip().lower() #What to use when searching in a msg
        msgsplit = searcher.split()
    if searcher == "ping": #PINGPONG
        s.send("PRIVMSG " + CHAN + " : PONG.\r\n")
    if mode == "PRIVMSG":
        print CHAN, man + ":", (msg).rstrip()
        
