# bot.py
def chat(sock, msg):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    sock.send("PRIVMSG {} :{}\r\n".format(cfg.CHAN, msg))

def ban(sock, user):
    """
    Ban a user from the current channel.
    Keyword arguments:
    sock -- the socket over which to send the ban command
    user -- the user to be banned
    """
    chat(sock, ".ban {}".format(user))

def timeout(sock, user, secs=600):
    """
    Time out a user for a set period of time.
    Keyword arguments:
    sock -- the socket over which to send the timeout command
    user -- the user to be timed out
    secs -- the length of the timeout in seconds (default 600)
    """
    chat(sock, ".timeout {}".format(user, secs))


import cfg
import socket
import re
import nltk
from collections import deque

# network functions go here

s = socket.socket()
s.connect((cfg.HOST, cfg.PORT))
s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))

test = ["LUL", "OMG", "WTF", "MLG", "10/10"]
q = deque([])
qSize = 6
while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        #username = re.search(r"\w+", line).group(0) # return the entire match
        #message = CHAT_MSG.sub("", line)
        #print(username + ": " + message)
        parsedResponse = response.split(":",2)
        message = str((parsedResponse[len(parsedResponse) - 1]).split("\r")[0].split("\n")[0])
        if len(q) < qSize:
            #print("We are putting this in: " + message)
            q.append((message))
        elif len(q) == qSize:
            for word in test:
                if q.count(word) == 4:
                    print("YAY")
            for x in range(0, qSize/3):
                q.popleft()
            q.append(message)

        #print(message)
        #print(len(q))
        #print(q)

        #chat(s, "Shut up, DankAss. Show me your MMR.")
    #sleep(1 / cfg.RATE)
    timeout(s, cfg.NICK, 1 / cfg.RATE)

