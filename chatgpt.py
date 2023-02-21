import os
import socket
import ssl
import time
import openai
import re

openai.api_key = "apikey" #Insert your secret key between quotes

server = "irc.whatever.com"
port = 6697 # 6667 for non SSL
channel = "#insertchannel"
botnick = "ChatGPT"
password = ""

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
irc_ssl = context.wrap_socket(irc, server_hostname=server)

irc_ssl.send(("USER " + botnick + " " + botnick + " " + botnick + " :I am a bot!\r\n").encode())
irc_ssl.send(("NICK " + botnick + "\r\n").encode())

while True:
    data = irc_ssl.recv(4096).decode('utf-8')
    print(data)  # print all data received from server to console
    if data.find("PING") != -1:
        irc_ssl.send(("PONG " + data.split()[1] + "\r\n").encode())
    elif data.find("422") != -1 or data.find("376") != -1:  # if no MOTD or end of MOTD
        irc_ssl.send(("JOIN " + channel + "\r\n").encode())
    elif data.find("PRIVMSG") != -1:
        match = re.search(r'^:(.*)!(.*)@(.*) PRIVMSG (.*) :(.*)', data)
        if match:
            user = match.group(1)
            message = match.group(5)
            if message.startswith(botnick + ":"):
                prompt = message.split(botnick + ":")[1]
                try:
                    response = openai.Completion.create(
                        engine="text-davinci-003", # text-curie-001 is 10x cheaper and dumber
                        prompt=prompt,
                        max_tokens=2048, #may have to lower if you use curie
                        n=1,
                        stop=None,
                        temperature=0.2, # higher = more random
                    )
                    print(response)
                    if response.choices and response.choices[0].text.strip():
                        text = response.choices[0].text.strip()
                        lines = (line.strip() for line in text.split("\n") if line.strip())
                        for i, line in enumerate(lines):
                            if i >= 10:
                                irc_ssl.send(f"PRIVMSG {channel} :\x0308Too many lines! Sorry sosu.\x0F\r\n".encode())
                                break
                            prefix = "\x0306[ChatGPT]\x0F: " if i == 0 else ""
                            chunks = [line[x:x+400] for x in range(0, len(line), 400)]
                            for chunk in chunks:
                                irc_ssl.send(f"PRIVMSG {channel} :{prefix}\x0312{chunk}\x0F\r\n".encode())
                except Exception as e:
                    print("Error:", str(e))
                    irc_ssl.send(f"PRIVMSG {channel} :{prefix}\x0308An error occurred while processing your request. Please try again later.\x0F\r\n".encode())
                            
    time.sleep(1)
