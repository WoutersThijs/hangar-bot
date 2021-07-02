import discord
import os
import secrets
from telethon import TelegramClient, events, sync

dClient = discord.Client()

# Telegram API
tClient = TelegramClient('session', secrets.tel_api_id, secrets.tel_api_hash)
tClient.start()

# Discord
@dClient.event
async def on_ready():
    print("Logged in as {0.user}".format(dClient))

    @tClient.on(events.NewMessage(chats="@hangarbottest"))
    async def news_handler_1(event):
       await dClient.get_channel(844201849602572288).send(":newspaper:   The Block's News Feed    :newspaper:\n \n" + event.text)

    @tClient.on(events.NewMessage(chats="@hangarbottest"))
    async def news_handler_2(event):
       await dClient.get_channel(844201849602572288).send(":newspaper:   One Minute Letter    :newspaper:\n \n" + event.text)


@dClient.event
async def on_message(message):
    if message.author == dClient.user:
        return

    if message.content.startswith('/hangar add news'):
        await message.channel.send('Ready to send news in this channel!')
    
    if message.content.startswith('/hangar add tradinghours'):
        await message.channel.send('Ready to send trading hours in this channel!')


dClient.run(secrets.disc_client)