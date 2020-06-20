import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import random


client = commands.Bot(command_prefix="l!")

cluster = MongoClient("mongodb+srv://dbUser:1234@cluster0-fnm6p.mongodb.net/lyricbotdb?retryWrites=true&w=majority")

db = cluster["lyricbotdb"]
#idCollection = db["id"]

@client.event
async def on_ready():
    print("Bot is ready")

@client.command(name="create", help="Creates a question")
async def create(ctx, lyric, title):
    id = random.randint(1, 1000000)
    collection = db["questions"]
    collection.insert_one({"lyric":lyric, "title":title, "id":id})
    await ctx.send("Successfully created question.")

@client.command(name="guess", help="Guess a song genius")
async def guess(ctx, id : int, title):
    collection = db["questions"]
    results = collection.find({})

    for question in results:
        if question["id"] == id:
            if (question["title"].lower() == title.lower()):
                await ctx.send("Correct")
            else:
                await ctx.send("Incorrect (but there is a possibility that the bot is still searching for a song with the same ID)")
    

@client.command(name="list", help="List all question")
async def list(ctx):
    collection = db["questions"]
    string = ""
    cursor = collection.find({})
    for question in cursor:
            string += "id: " + str(question["id"]) + " lyrics: " + question["lyric"] + "\n"
    await ctx.send(string)
    
    
@client.command(name="clear", help="Clears things")
async def clear(ctx):
    collection = db["questions"]
    collection.remove({})

    await ctx.send("Successfully deleted questions.")
client.run("NzIzNTkwMDkyOTQxMjk1NzA3.Xuz14Q.EO2g5PrMNl4OnG99Zwt6c8eVypI")