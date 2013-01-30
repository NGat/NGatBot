######## WELCOME TO LOKIBOT.PY, A CREATION BY LOKI456789 (NATHAN GATENBY) ########
######## CHECK OUT HTTP://GITHUB.COM/NGAT ########


#### Definitions ####
import sys
import socket
import string
import os
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
names = {}
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
      "PONG " + line.split()[1]
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

    line = s.recv(500)  #                         #Getting data
    ingame = False

    if line.startswith("PING"): #Esper PingPong
        s.send("PONG " + line.split()[1]+"\r\n")
        print "PONG " + line.split()[1]+"\n"

    man = line[1:(line.find("!"))] #Person who sent the line
    sender=man
    splitall = line.split()
    split = line.split(CHAN) #Splitting the IP etc. from the message
    if line.find("Please choose a different nickname, or identify via /msg NickServ identify <password>")!=-1:
      s.send("PRIVMSG NickServ IDENTIFY " + NICK + PASS + "\r\n")
####





#### PARSING ####
    if CHAN in line:
        if line.index(CHAN)!=0:
          mode = splitall[splitall.index(CHAN)-1]
        msg = split[1][2:]#gets the message
        match = re.search(r"...\[...G...\] ...\[...(.*?)...\] ...(.*?)......:... (.*)", msg) #Checks to see if the message is from Minecraft
        if match:#checks if the message is from MC
          msg = match.group(3)
          sender = "TornKing"
          ingame = True
          man = match.group(2)

          #### Working with Name exceptions (Admins) ####
          if man.find("Jevist")!=-1:
            man = "Jevist"
          if man.find("Geachinator")!=-1:
            man = "Geachinator"
          if man.find("Bob_Paul")!=-1:
            man = "Bob_Paul"
          ####
            
          print "TK " + man + ": " + msg,
        elif re.search(r"\[(.*?) .?.?.?connected\]", msg):
          print "TK " + msg,
        else:
          print CHAN, man + ":", msg,
        searcher = msg.rstrip().lower() #What to use when searching in a msg
        msgsplit = searcher.split()


        #### PINGPONG ####
        if searcher == "ping": #PINGPONG
            s.send("PRIVMSG " + CHAN + " : pong\r\n")
        ####

        #### help message ####
        REhelp = re.search(r"^(help)|halp", searcher)
        if REhelp:
          s.send("PRIVMSG " + CHAN + " : %s, if you need help from staff, write them a Petition! /pe new <message>\r\n" %man)


        RETown = re.search(r'(how to start a town)|(how do i start a town)', msg.lower())
        if RETown:
          s.send("PRIVMSG " + CHAN + " : %s, you need to be Adventurer rank to start a town, that costs $1000. A town will cost you $3000. /t new <name>\r\n" %man)

        #### .users (getting who is on the IRC channel) ####
        if searcher == ".users":       #To let MC players see who is on IRC
          s.send("NAMES " + CHAN + '\r\n')
          line=s.recv(500)
          print line
          splitall = line.split() 
          peoplestr = ""
          people = splitall[splitall.index(CHAN)+1:]
          people[0] = people[0][1:]
          for count in people:
            if count[0] == "@" or count[0] == "+":
              count = count[1:]
            if count.find("TornKing")!=-1:
              continue
            if count.find("Minebot")!=-1:
              continue
            peoplestr+=count + " "
          s.send('PRIVMSG ' + CHAN + " : On #tornkingdom: " + peoplestr + '\r\n')
        ####
          


        #### Welcomer ####
        con = re.search(r"\[(.*?) connected\]", msg)  
        if mode == "JOIN":
          rename = re.search(r':(.*?)!', line)
          name = rename.group(1)
          for nam in open("names.txt", "rU"):
            names[nam.split()[0]] = nam.split(" ", 1)[1]
          if name in names:
            name = names[name]
          s.send("PRIVMSG " + CHAN + " : Hey, %s\r\n" %name)
          
        if con and sender == "TornKing":
          name = con.group(1)
          for nam in open("names.txt", "rU"):
            names[nam.split()[0]] = nam.split(" ", 1)[1]
          if name in names:
            name = names[name]
          s.send("PRIVMSG " + CHAN + " : " + "Hey %s\r\n" %name)
        ####

        TRE = re.search(r'^.tr (.*)', msg)
        if TRE and ingame:
          print "success"
          s.send("PRIVMSG BitBot :" + msg + "\r\n")
          print "PRIVMSG BitBot : " + msg


        #### 'Kingdom Server finder ####
        kingdom = re.search(r'kingdom(s)? server|join a kingdom|join ur kingdom|join your kingdom', searcher)
        if kingdom:
          s.send("PRIVMSG " + CHAN + " : " + "%s, we are a Towny Server, not a Kingdom Server! See http://tornkingdom.net for more info.\r\n" %man)
        ####
        if searcher == 'debug':
          print people
          print man
          print mode
          print names
          print ""
          print line


###End of 'if CHAN in line'###




    #### PM stuff: rules, tips, LokiChat ####
    pm = re.search(r'^:(.*?)!.*? PRIVMSG %s :(.*)' %NICK, line)
    if pm:
      user = pm.group(1)
      pmg = pm.group(2)
      if user == "Loki456789":
        s.send("PRIVMSG " + CHAN + " : %s\r\n" %pmg)
      elif pmg.find("rules")!=-1:
        s.send("PRIVMSG "+user+" : 1. Be respectful to all players and users. No abuse or bullying will be tolerated.\r\nPRIVMSG "+user+" : 2. Do not spam chat or use offensive or harsh language.\r\nPRIVMSG "+user+" : 3. Do not impersonate players, users, or members of the greater public.\r\nPRIVMSG "+user+" : 4. Do not advertise other games or servers.\r\nPRIVMSG "+user+" : Failure to adhere to these rules may result in InGame and IRC Bans.\r\n")
        print "PRIVMSG "+user+" : 1. blah"
      elif pmg.find("tips")!=-1:
         s.send("PRIVMSG "+user+" : Hi, welcome to " + CHAN + " IRC. Enjoy your stay!\r\nPRIVMSG "+user+" : Here are a few tips:\r\nPRIVMSG "+user+" : 1. When InGame, type .users to view a list of online IRC users.\r\nPRIVMSG "+user+" : 2. When on IRC, type .players to view a list of online players.\r\nPRIVMSG "+user+" : 3. Message me 'rules' to see a list of rules.\r\nPRIVMSG "+user+" : 4. Speak to Loki456789/LowQuai about changing your 'Login Nickname'\r\nPRIVMSG "+user+" : Enjoy your stay!\r\nPRIVMSG "+user+" : --LokiBot/Loki456789, and the IRC Staff.\r\n")
      elif user == "BitBot":
        s.send("PRIVMSG " + CHAN + " :"+pmg[9:-24]+")\r\n")
      print "Message from " + user + ": " + pmg + '\n'
    ####
