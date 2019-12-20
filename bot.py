# -*- coding: utf-8 -*-
import config
import utils
import socket
import time
import re
import thread
from time import sleep


def main():
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(config.CHAN).encode("utf-8"))

    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    utils.mess(s, "Бот работает")

    thread.start_new_thread(utils.fillOpList, ())
    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = chat_message.sub("", response)
            print(response)
            if message.strip() == "!time":
                utils.mess(s, "it's currently: " + time.strftime("%I:%M %p %Z on %A %B %d %Y"))
            if message.strip() == "!dotabuff":
                utils.mess(s, "Мой дотабафф: https://ru.dotabuff.com/players/79638171\n Мой профиль OpenDota: https://www.opendota.com/players/79638171")
            if message.strip() == "!song":
                utils.mess(s,"Проверь статус в вк: https://vk.com/nikita_kulikov")
            if message.strip() == "!socials":
                utils.mess(s, "ВК: https://vk.com/nikita_kulikov\nInstagram: https://www.instagram.com/pocketkurt/")
            if message.strip() == "!commands":
                utils.mess(s, "!time !dotabuff !song !socials !commands")
        sleep(1)



if __name__ == "__main__":
    main()