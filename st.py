#!/usr/bin/python3
from random import choice
from os import environ
#######
import discord
import requests
from googleapiclient.discovery import build

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
        self.load_2hus()
        self.motifs = [x.rstrip() for x in open("motifs.txt", "r").readlines()]

    def load_2hus(self):
        toohus = [x.rstrip() for x in open("2hus.txt", "r").readlines()]
        win = [toohu[:-2] for toohu in toohus if toohu.split()[-1] == "w"]
        pc98 = [toohu[:-2] for toohu in toohus if toohu.split()[-1] == "p"]
        self.toohus ={"windows":win, "pc98":pc98}

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author == self.user:
            return

        if message.content.startswith(f"{self.prefix}touhou"):
            msg = message.content.split()
            if len(msg) > 1:
                if message.content.split()[1].lower() in ["windows", "win", "winblows"]:
                    chosen = choice(self.toohus["windows"])
                elif message.content.split()[1].lower() in ["pc98","pc-98"]:
                    chosen = choice(self.toohus["pc98"])
                else:
                    chosen = choice(self.toohus["pc98"] + self.toohus["windows"])
            else:
                chosen = choice(self.toohus["pc98"] + self.toohus["windows"])
            await message.channel.send(
                    "In your heart of hearts, you're thinking of... {}!".format(chosen)
                    )

        if message.content.startswith(f"{self.prefix}motif"):
            chosen = choice(self.motifs)
            await message.channel.send(
                    "Your mythologic motif is...\n`{}`".format(chosen)
                    )

        if message.content.startswith(f"{self.prefix}yt"):
            query = message.content.split()
            print(query)
            if len(query) < 2:
                await message.channel.send("Give me a term to search!")
                return
            query = query[1:]
            url = await get_first_utube_vid(" ".join(query))
            await message.channel.send(url)

bot = Satorin()

DISCORD_TOKEN = environ["DISCORD_TOKEN"]
GOOGLE_API_KEY = environ["GOOGLE_API_KEY"]

youtube = build("youtube", "v3", developerKey=GOOGLE_API_KEY)

bot.run(DISCORD_TOKEN)
