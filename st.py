#!/usr/bin/python3
from random import choice
from os import environ
import re
#######
import discord
import requests
from googleapiclient.discovery import build

def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/ ]*[@-~]')
    return ansi_escape.sub('', line)

async def get_first_utube_vid(query):
    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        q=query,
        type="video"
        )
    response = request.execute()
    return "https://www.youtube.com/watch?v={}".format(response.get("items")[0].get("id").get("videoId"))

class Satorin(discord.Client):
    def __init__(self):
        discord.Client.__init__(self)
        self.prefix = "!"
        self.toohus = [x.rstrip() for x in open("2hus.txt", "r").readlines()]
        self.motifs = [x.rstrip() for x in open("motifs.txt", "r").readlines()]

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

        if msgtext.startswith(f"{self.prefix}w")\
        or msgtext.startswith(f"{self.prefix}weather"):
            if len(msgtext.split()) == 1:
                await message.channel.send("Add the name of your city to get the weather.")
            else:
                city = msgtext.split(maxsplit=1)[1].replace(" ", "+")
                weather = requests.get("https://wttr.in/{}".format(city))
                weather = weather.content.decode("utf-8")
                weather = "\n".join(weather.split("\n")[:7])
                weather = escape_ansi(weather)
                print(weather)
                await message.channel.send("```{}```".format(weather))

        if msgtext.startswith(f"{self.prefix}touhou"):
            chosen = choice(self.toohus)
            await message.channel.send(
                    "In your heart of hearts, you're thinking of... {}!".format(chosen)
                    )

        if msgtext.startswith(f"{self.prefix}motif"):
            chosen = choice(self.motifs)
            await message.channel.send(
                    "Your mythologic motif is...\n`{}`".format(chosen)
                    )

        if msgtext.startswith(f"{self.prefix}yt"):
            query = msgtext.split()
            print(query)
            if len(query) < 2:
                await message.channel.send( "Give me a term to search!" )
                return
            query = query[1:]
            url = await get_first_utube_vid(" ".join(query))
            await message.channel.send(url)

bot = Satorin()

DISCORD_TOKEN = environ["DISCORD_TOKEN"]
GOOGLE_API_KEY = environ["GOOGLE_API_KEY"]

youtube = build("youtube", "v3", developerKey=GOOGLE_API_KEY)

bot.run(DISCORD_TOKEN)
