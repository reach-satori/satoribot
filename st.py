#!/usr/bin/python3
from random import choice
from os import environ
import re
import glob
#######
import discord
import requests
from googleapiclient.discovery import build
######
from draw_ascii import doimage

def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/ ]*[@-~]')
    return ansi_escape.sub('', line)

def get_first_utube_vid(query):
    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        q=query,
        type="video"
        )
    response = request.execute()
    items = response.get("items")
    if len(items) == 0:
        return "No videos found!"
    return "https://www.youtube.com/watch?v={}".format(items[0].get("id").get("videoId"))

class Satorin(discord.Client):
    motifs = [x.rstrip() for x in open("motifs.txt", "r").readlines()]
    toohus = [x.rstrip() for x in open("2hus.txt", "r").readlines()] # overriden just below
    win = [toohu[:-2] for toohu in toohus if toohu.split()[-1] == "w"]
    pc98 = [toohu[:-2] for toohu in toohus if toohu.split()[-1] == "p"]
    del toohus
    def __init__(self):
        discord.Client.__init__(self)
        self.prefix = "!"
        self.dispatcho = {
            "yt" : self.get_ytlink,
            "touhou" : self.get_touhouchoice,
            "2hu" : self.get_touhouchoice,
            "motif" : self.get_motif,
            "weather" : self.get_weather,
            "w" : self.get_weather,
            "aa" : self.get_aa,
        }

    def get_touhouchoice(self, message):
        msgtext = message.content
        msg = msgtext.split()
        if len(msg) > 1:
            if msgtext.split()[1].lower() in ["windows", "win", "winblows"]:
                chosen = choice(self.win)
            elif msgtext.split()[1].lower() in ["pc98","pc-98"]:
                chosen = choice(self.pc98)
            else:
                chosen = choice(self.pc98 + self.win)
        else:
            chosen = choice(self.pc98 + self.win)
        return f"In your heart of hearts, you're thinking of... {chosen}!"

    def get_motif(self, message):
        return f"Your mythologic motif is {choice(self.motifs)}."

    def get_weather(self, message):
        msgtext = message.content
        msg = msgtext.split()
        if len(msg) == 1:
            return "Add the name of your city to get the weather."
        city = msgtext.split(maxsplit=1)[1].replace(" ", "+")
        weather = requests.get(f"https://wttr.in/{city}")
        weather = weather.content.decode("utf-8")
        if city.lower() == "moon":
            weather = "\n".join(weather.split("\n")[:22])
            weather = escape_ansi(weather)
        else:
            weather = "\n".join(weather.split("\n")[:7])
            weather = escape_ansi(weather)
        return f"```{weather}```"

    def get_aa(self, message):
        aalist = glob.glob("./ascii/ascii_*")
        chosen = choice(aalist)
        doimage(chosen)

    def get_ytlink(self, message):
        msgtext = message.content
        query = msgtext.split(maxsplit=1)
        if len(query) < 2:
            return "Give me a term to search!"

        query = query[1]
        url = get_first_utube_vid(" ".join(query))
        return url

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author == self.user:
            return
        msgtext = message.content
        if msgtext.startswith(self.prefix):
            msgtext = msgtext[1:].split()
            key = msgtext[0]
            if key in self.dispatcho:
                ret = self.dispatcho[key](message)
                if key == "aa":
                    await message.channel.send(file=discord.File("ascii.png"))
                else:
                    await message.channel.send(ret)

bot = Satorin()

DISCORD_TOKEN = environ["DISCORD_TOKEN"]
GOOGLE_API_KEY = environ["GOOGLE_API_KEY"]

youtube = build("youtube", "v3", developerKey=GOOGLE_API_KEY)

bot.run(DISCORD_TOKEN)
