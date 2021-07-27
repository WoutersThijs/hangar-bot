import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from telethon import TelegramClient, events
import json

load_dotenv()

discord_client = commands.Bot(command_prefix="/hb ")

# Telegram API
telethon_client = TelegramClient('session', os.getenv('TELEGRAM_API_ID'), os.getenv('TELEGRAM_API_HASH'))
telethon_client.start()

# Discord
@discord_client.event
async def on_ready():
    print("Logged in as {0.user}".format(discord_client))

    # Create data.json
    if not os.path.isfile("data.json"):
        data = {}
        data['discord_channels'] = []
        data['discord_channels'].append({
            "id": "844201849602572288",
            "news": 'true',
            "tradinghours": 'true',
            "telegram_channels": ["hangarbottest", "oneminuteletter"]
        })
        with open("data.json", "w") as file:
            json.dump(data, file)

    # Create telegram chat listeners
    with open('data.json') as file:
        data = json.load(file)
    telegram_channels = set()
    for discord_channel in data['discord_channels']:
        for telegram_channel in discord_channel['telegram_channels']:
            telegram_channels.add(telegram_channel)
    
    for telegram_channel in telegram_channels:
        @telethon_client.on(events.NewMessage(chats="@" + telegram_channel))
        async def listener(event):
            for discord_channel in data['discord_channels']:
                print(discord_channel)
                if  telegram_channel in discord_channel['telegram_channels']:
                    print("- " + discord_channel)
                    await discord_client.get_channel(int(discord_channel['id'])).send(":newspaper:   " + event.chat.title + "   :newspaper:\n \n" + event.text)

# Commands
# - Add
@discord_client.command(name="add")
async def hb(ctx, arg):
    # - News
    if arg == "news":
        # Load data
        with open('data.json') as file:
            data = json.load(file)
        
        # Create set with existing channel ids
        existing_channel_ids = set()
        for channel in data['discord_channels']:
            existing_channel_ids.add(int(channel['id']))

        # Existing channel
        if ctx.channel.id in existing_channel_ids:
            await ctx.channel.send("Already sending news to this channel")

        # Add new channel to data    
        else:
            data['discord_channels'].append({
                "id": ctx.channel.id,
                "news": 'true',
                "tradinghours": 'false',
                "telegram_channels": ["hangarbottest", "oneminuteletter"]
            })

            # Write to data.json
            with open("data.json", "w") as file:
                json.dump(data, file)

            # Send message in Discord
            await ctx.channel.send("Ready to send news in this channel.")
    
    # - TradingHours
    elif arg == "tradinghours":
        await ctx.channel.send("Ready to send trading hours in this channel.")
    else:
        await ctx.channel.send("'" + arg + "' is not a valid argument. Use:" +
         "\n /hb add news" +
         "\n /hb add tradinghours" )

# - Remove
@discord_client.command(name="remove")
async def hb(ctx, arg):
    if arg == "news":
         # Load data
        with open('data.json') as file:
            data = json.load(file)

        # Create set with existing channel ids
        existing_channel_ids = set()
        for channel in data['discord_channels']:
            existing_channel_ids.add(int(channel['id']))

        # Existing channel
        if ctx.channel.id in existing_channel_ids:
            await ctx.channel.send("No longer sending news in this channel.")

        else:
            await ctx.channel.send("This channel is already disabled.")
    elif arg == "tradinghours":

        await ctx.channel.send("No longer sending trading hours in this channel.")
    else:
        await ctx.channel.send("'" + arg + "' is not a valid argument. Use:" +
         "\n /hb remove news" +
         "\n /hb remove tradinghours" )


discord_client.run(os.getenv('DISCORD_TOKEN'))
