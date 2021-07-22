import os
from dotenv import load_dotenv
import discord
from telethon import TelegramClient, events

load_dotenv()

discord_client = discord.Client()

# Telegram API
telethon_client = TelegramClient('session', os.getenv('TELEGRAM_API_ID'), os.getenv('TELEGRAM_API_HASH'))
telethon_client.start()

# Discord
@discord_client.event
async def on_ready():
    print("Logged in as {0.user}".format(discord_client))

    @telethon_client.on(events.NewMessage(chats="@the_block_crypto"))
    async def news_handler_1(event):
       await discord_client.get_channel(844201849602572288).send(":newspaper:   The Block's News Feed    :newspaper:\n \n" + event.text)

    @telethon_client.on(events.NewMessage(chats="@oneminuteletter"))
    async def news_handler_2(event):
       await discord_client.get_channel(844201849602572288).send(":newspaper:   One Minute Letter    :newspaper:\n \n" + event.text)

    @telethon_client.on(events.NewMessage(chats="@hangarbottest"))
    async def news_handler_3(event):
       await discord_client.get_channel(844201849602572288).send(":newspaper:   Test message   :newspaper:\n \n" + event.text)

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    if message.content.startswith('/hangar add zzzzzz'):
        await message.channel.send('Ready to send news in this channel!')
    
    if message.content.startswith('/hangar add tradinghours'):
        await message.channel.send('Ready to send trading hours in this channel!')
discord_client.run(os.getenv('DISCORD_TOKEN'))
