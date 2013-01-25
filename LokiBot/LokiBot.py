######## WELCOME TO LOKIBOT.PY, A CREATION BY LOKI456789 (NATHAN GATENBY) ########
######## CHECK OUT HTTP://GITHUB.COM/NGAT ########


#### Definitions ####
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
PASS = ''
people = []
peoplestr = ""
s = socket.socket()
####

#### CONNECTION/CHANNEL JOINING ####
print "Connecting..."
s.connect((HOST, PORT))
print "Connected."
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
####


#### GETTING DATA AND PRELIMINARY ACTIONS ####
while True:
    ### MANAGING CHAT ###
  
    line = s.recv(500) #Getting data
    print line
    man = line[1:(line.find("!"))] #Person who sent the line
    splitall = line.split()
    split = line.split(CHAN) #Splitting the IP etc. from the message
    if line.find("Please choose a different nickname, or identify via /msg NickServ identify <password>")!=-1:
      s.send("PRIVMSG NickServ IDENTIFY " + NICK + PASS + "\r\n")
####





#### PARSING ####
    if CHAN in line:

        msg = split[1][2:]#gets the message
        match = re.search(r"...\[...G...\] ...\[...(.*?)...\] ...(.*?)......:... (.*)", msg) #Checks to see if the message is from Minecraft
        if match:#checks if the message is from MC
          msg = match.group(3)
          man = match.group(2)

          #### Working with Name exceptions (Admins) ####
          if man.find("Jevist")!=-1:
            man = "Jevist"
          if man.find("Geachinator")!=-1:
            man = "Geachinator"
          ####
            
          print "TK " + man + ": " + msg
        else:
          print CHAN, man, ":", msg
        searcher = msg.rstrip().lower() #What to use when searching in a msg
        msgsplit = searcher.split()


        #### PINGPONG ####
        if searcher == "ping": #PINGPONG
            s.send("PRIVMSG " + CHAN + " : PONG.\r\n")
        ####
      

        #### .users (getting who is on the IRC channel) ####
        if searcher == ".users":       #To let MC players see who is on IRC
          s.send("NAMES " + CHAN + '\r\n')
          line=s.recv(500)
          splitall = line.split()
          print "sent names"   # .users 
          peoplestr = ""
          people = splitall[splitall.index(CHAN)+1:]
          people[0] = people[0][1:]
          for count in people:
            if count[0] == "@" or count[0] == "+":
              count = count[1:]
            if count == "TornKing": #Getting rid of the bots off the list
              continue
            if count == "Minebot":
              continue
            peoplestr+=count + " "
          s.send('PRIVMSG ' + CHAN + " : On #tornkingdom: " + peoplestr + '\r\n')
        ####
          

        #### Welcomer ####
        con = re.search(r"\[(.*?) connected\]", msg)
        if con:
          name = con.group(1)
          s.send("PRIVMSG " + CHAN + " : " + "Hey %s\r\n" %name)
        ####

          
        #### 'Kingdom Server finder ####
        if searcher.find("kingdom server")!=-1 or searcher.find("kingdoms server")!=-1:
          s.send("PRIVMSG " + CHAN + " : " + "We are a Towny Server, not a Kingdom Server! See http://tornkingdom.net for more info.\r\n")
        ####

    #### Esper net's PING PONG ####
    if line.startswith("PING"):
        s.send("PONG " + line.split()[1]+"\r\n")
        print "PONG " + line.split()[1]
    ####
