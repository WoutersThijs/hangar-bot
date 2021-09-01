import os
import sys
from dotenv import load_dotenv
import discord
from discord.ext import commands
from telethon import TelegramClient, events, utils
from telethon.tl.types import PeerChannel
from telethon.tl.functions.channels import JoinChannelRequest
import asyncio

import json

load_dotenv()

discord_client = commands.Bot(command_prefix="/hb ")

# Telegram API
telethon_client = TelegramClient('session', os.getenv('TELEGRAM_API_ID'), os.getenv('TELEGRAM_API_HASH'))
telethon_client.start()

def restart_bot(): 
  os.execv(sys.executable, ['python3'] + sys.argv)

# Discord
@discord_client.event
async def on_ready():
    print("Logged in as {0.user}".format(discord_client))

    # Create data.json
    if not os.path.isfile("data.json"):
        data = {}
        data['discord_channels'] = []
        data['discord_channels'].append({
            "id": 845251997795614730,
            "telegram": True,
            "tradinghours": True,
            "telegram_channels": ["hangarbottest", "the_block_crypto"]
        })
        with open("data.json", "w") as file:
            json.dump(data, file)

    # Load data.json
    with open('data.json') as file:
        data = json.load(file)
    
    # Create set with telegram channels
    telegram_channels = set()
    for discord_channel in data['discord_channels']:
        for telegram_channel in discord_channel['telegram_channels']:
            telegram_channels.add(telegram_channel)

    # Register listener
    @telethon_client.on(events.NewMessage(chats=telegram_channels))
    async def listener(event):
        peer_channel = await telethon_client.get_entity(PeerChannel(utils.resolve_id(event.chat_id)[0]))
        for discord_channel in data['discord_channels']:
            if peer_channel.username in discord_channel['telegram_channels'] and discord_channel['telegram'] == True:
                await discord_client.get_channel(discord_channel['id']).send(":speech_balloon:   " + event.chat.title + "   :speech_balloon:\n \n" + event.text)

# Commands
# - Telegram
@discord_client.command(name="tg")
@commands.has_role('Team')
async def telegram(ctx, *args):
    # Load JSON data
    with open('data.json') as file:
        data = json.load(file)
    
    def write_json():
        # Write to data.json
        with open("data.json", "w") as file:
            json.dump(data, file)

    # Create set with existing channel ids
    existing_channel_ids = set()
    for channel in data['discord_channels']:
        existing_channel_ids.add(int(channel['id']))

    # Create new one of not exists
    if ctx.channel.id not in existing_channel_ids:
        data['discord_channels'].append({
            "id": ctx.channel.id,
            "telegram": False,
            "tradinghours": False,
            "telegram_channels": ["hangarbottest"]
        })

    # Arguments
    # - On
    if args[0] == "on":
        for index, existing_channel in enumerate(data['discord_channels'], start=0):
            if existing_channel['id'] == ctx.channel.id:
                # Telegram = true
                if(existing_channel['telegram'] == True):
                    # Delay time for message removal
                    time = 10

                    # Send message in Discord
                    msg = await ctx.channel.send("Telegram listening has already been turned **ON** for this channel." +
                                                 "\n**:no_entry_sign:  -** _This message will be removed in " + str(time) + " seconds._")
                    await asyncio.sleep(time)
                    await msg.delete()
                  
                # Telegram = false
                else:
                    # Set value 'Telegram' to 'True'
                    data['discord_channels'][index]['telegram'] = True
                    
                    # Delay time for message removal
                    time = 15

                    # Send message in Discord
                    msg = await ctx.channel.send("Telegram listening has been turned **ON** for this channel. \n" +
                                           "You can add Telegram channels using __/hb tg add__" +
                                           "\n**:white_check_mark:  -** _This message will be removed in " + str(time) + " seconds._")

                    write_json()
                    await asyncio.sleep(time)
                    await msg.delete()

    # - Off
    elif args[0] == "off":
        for index, existing_channel in enumerate(data['discord_channels'], start=0):
            if existing_channel['id'] == ctx.channel.id:
                # Delay time for message removal
                time = 10

                # Telegram = true
                if(existing_channel['telegram'] == True):
                    
                    # Set value 'News' to 'True'
                    data['discord_channels'][index]['telegram'] = False

                    # Send message in Discord
                    msg = await ctx.channel.send("Telegram listening has been turned **OFF** for this channel." +
                                           "\n**:white_check_mark:  -** _This message will be removed in " + str(time) + " econds._")

                    write_json()
                    await asyncio.sleep(time)
                    await msg.delete()

                # Telegram = false
                else:
                    # Send message in Discord
                    msg = await ctx.channel.send("Telegram listening has already been turned **OFF** for this channel." +
                                           "\n**:no_entry_sign:  -** _This message will be removed in " + str(time) + " seconds._")

                    await asyncio.sleep(time)
                    await msg.delete()

    # - Status
    elif args[0] == "status":
        for index, existing_channel in enumerate(data['discord_channels'], start=0):
            if existing_channel['id'] == ctx.channel.id:
                # Delay time for message removal
                time = 20

                if existing_channel['telegram'] == True:
                    await ctx.channel.send("Telegram listening: **ON**")
                else:
                    await ctx.channel.send("Telegram listening: **OFF**")
                    
                await ctx.channel.send("This channel listens to:")
                for telegram_channel in existing_channel['telegram_channels']:
                    await ctx.channel.send("- " + telegram_channel)

    # - Add
    elif args[0] == "add":
        for existing_channel in data['discord_channels']:
            if existing_channel['id'] == ctx.channel.id:
                # Delay time for message removal
                time = 10
                
                if args[1] in existing_channel['telegram_channels']:
                    msg = await ctx.channel.send("**@" + args[1] + "** is already on the list." +
                                           "\n**:no_entry_sign:  -** _This message will be removed in " + str(time) + " seconds._")
                    
                    await asyncio.sleep(time)
                    await msg.delete()
                else:
                    # Check if telegram channel exists
                    try:
                        # Create entity from arg1
                        entity = await telethon_client.get_entity("@" + args[1])

                        # Join Telegram chat
                        await telethon_client(JoinChannelRequest(entity))

                        existing_channel['telegram_channels'].append(args[1])
                        msg = await ctx.channel.send("Telegram channel **@" + args[1] + "** has been added." +
                                               "\n**:white_check_mark:  -** _This message will be removed in " + str(time) + " seconds._")
                                               
                        write_json()
                        await asyncio.sleep(time)
                        await msg.delete()

                    except:
                        msg = await ctx.channel.send("**@" + args[1] + "** is not a valid Telegram channel." +
                                               "\n**:no_entry_sign:  -** _This message will be removed in " + str(time) + " seconds._")
                    
                    await asyncio.sleep(time)
                    await msg.delete()


    # - Remove
    elif args[0] == "remove":
        for existing_channel in data['discord_channels']:
            if existing_channel['id'] == ctx.channel.id:
                # Delay time for message removal
                time = 10

                if args[1] in existing_channel['telegram_channels']:
                    existing_channel['telegram_channels'].remove(args[1])
                    msg = await ctx.channel.send("Telegram channel **@" + args[1] + "** has been removed." +
                                           "\n**:white_check_mark:  -** _This message will be removed in " + str(time) + " seconds._")

                    write_json()
                    await asyncio.sleep(time)
                    await msg.delete()

                else:
                    msg = await ctx.channel.send("**" + args[1] + "** has already been removed." +
                                           "\n**:no_entry_sign:  -** _This message will be removed in " + str(time) + " seconds._")

                    await asyncio.sleep(time)
                    await msg.delete()
    
    elif args[0] == "reload":
        # Delay time for message removal
        await ctx.channel.send("Reloading... It can take me a few seconds to start up again." +
                                "\n**:white_check_mark:  -** _This message has to be removed manually_")

        restart_bot()

    # - Other
    else:
        # Delay time for message removal
        time = 30

        msg = await ctx.channel.send("**" + args[0] + "** is not a valid argument. Use:" +
        "\n-  /hb tg status" +
        "\n-  /hb tg on" +
        "\n-  /hb tg off" +
        "\n-  /hb tg add [channel_name]" +
        "\n-  /hb tg remove [channel_name]" +
        "\n-  /hb tg reload" +
        "\n**:white_check_mark:  -** _This message will be removed in " + str(time) + " seconds._")

        await asyncio.sleep(time)
        await msg.delete()

@telegram.error
async def telegram_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        # Delay time for message removal
        time = 5

        msg = await ctx.channel.send("You don't have enough permissions to run this command." +
                               "\n**:no_entry_sign:  -** _This message will be removed in " + str(time) + " seconds._")
        
        await asyncio.sleep(time)
        await msg.delete()

discord_client.run(os.getenv('DISCORD_TOKEN'))