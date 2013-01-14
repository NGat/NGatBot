#Definitions
import sys
import socket
import string
import os
import pickle
HOST = 'chat.freenode.net'
PORT = 6665
NICK = 'NGatBot'
IDENT = 'NGatBot'
REALNAME = 'NGatbot'
OWNER = 'NGat'
CHAN = '#ngat'
s = socket.socket()
spam = 0 #Used to get rid of MOTD
facts = pickle.load(open("facts.txt", "rb")) # Used for the Fact-Checker
verb = ""                              # Used for the Fact-Checker


#Connecting to the server and channel
s.connect((HOST, PORT))
s.send('USER '+IDENT+' '+HOST+' bla :'+REALNAME+'\r\n')
s.send('NICK '+NICK+'\r\n')
while 1:
    line=s.recv(500) #Getting data
    if line.find('Your host is ') !=-1:
        spam = 1 #Removing MOTD
    if spam == 0:
        print line
    if line.find('already in use')!=-1:
        NICK = NICK + "_"
        s.send('USER '+IDENT+' '+HOST+' bla :'+REALNAME+'\r\n')
        s.send('NICK '+NICK+'\r\n')
    if line.find('End of /MOTD command')!=-1: 
        s.send('JOIN '+CHAN+'\r\n') #Joining channel
        break


while True:
    ### MANAGING CHAT ###
    line = s.recv(500) #Getting data
    man = line[1:(line.find("!"))] #Person who sent the line
    split = line.split(CHAN) #Splitting the IP etc. from the message
    mode = split[0].split()[-1] #Getting whether it is a PRIVMSG, JOIN, etc
    
    if CHAN.lower() in line:
        msg = split[1][2:]
        searcher = msg.rstrip().lower() #What to use when searching in a msg
        msgsplit = searcher.split()
        if mode == "PRIVMSG":
            print CHAN, man + ":", (msg).rstrip()
    ###               ###

    #Parsing
    if mode == "JOIN" and man != NICK: #WELCOMER
        s.send("PRIVMSG " + CHAN + " : Hey, " + man + ".\r\n")
        print CHAN + " NGatBot: Hey,  " + man + "."


    if searcher.find("sad") !=-1: #HUGS
        s.send("PRIVMSG " + CHAN + " : Gives hug to " + man + ".\r\n")
        print CHAN + " NGatBot: Gives hug to " + man + "."


    if searcher == "ping": #PINGPONG
        s.send("PRIVMSG " + CHAN + " : PONG.\r\n")
        print CHAN + " NGatBot: PONG"

    if searcher == "savefacts": #savefacts
        pickle.dump(facts, open("facts.txt", "wb"))
    if searcher == "facts": #facts print
        print facts

    if searcher.startswith(("are ", "is ")):
        if msgsplit[verb+1] in facts and msgsplit[verb+2] == facts[msgsplit[verb+1]]:
            s.send("PRIVMSG " + CHAN + " : Yes.\r\n")
            print CHAN + " NGatBot: Yes."
        else:
            s.send("PRIVMSG " + CHAN + " : No.\r\n")
            print CHAN + " NGatBot: No."
    elif " are " in searcher:
            verb = msgsplit.index("are")
            facts[msgsplit[verb-1]] = msgsplit[verb+1]
    elif " is " in searcher:
            verb = msgsplit.index("is")
            facts[msgsplit[verb-1]] = msgsplit[verb+1]
    





        
