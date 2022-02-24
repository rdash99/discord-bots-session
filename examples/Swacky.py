# Import the pycord library into your runtime.
import discord
from datetime import datetime
import time
import requests
import sqlite3
import os
import pandas as pd
db = sqlite3.connect('Methods.db')
cur = db.cursor()


client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author == client.user:
        return

    log(message)

    if message.content.startswith('$hello'):
        await message.channel.send("Don't mind me!")

    if message.content.startswith('$help'):
        return

    """ if message.content.startswith('$grab'):
        command = message.content[6:]
        print(command)
        dates = command.split(' ')
        print(dates)
        for date in dates:
            datetime().strptime(date, '%d %m %Y') """

    """ if message.content.startswith('$quit'):
        await message.channel.send("Goodbye!")
        await client.close()
        exit(0) """

    """ if message.content.startswith('$get_method'):
        search = ""
        find = str(message.content[12:])
        find = find.lower()

        search = "SELECT id FROM methods WHERE title LIKE '%" + \
            find + "%'"

        print(search)

        # print(message.content)

        await message.channel.send("Searching for methods...")
        result = db.execute(search).fetchall()
        if result == []:
            await message.channel.send("No methods found.")
            return
        elif len(result) == 1:
            await message.channel.send("Found 1 method.")
        else:
            await message.channel.send("Found " + str(len(result)) + " methods.")
            await message.channel.send("Here are all of the methods:")
        for i in result:
            await message.channel.send("https://complib.org/method/" +
                                       str(i[0])) """

    if message.content.startswith('$ping'):
        await message.channel.send('Pong!')
        await message.channel.send(file=discord.File('pong.gif'))
        """Get the bot's current websocket and API latency."""
        start_time = time.time()
        message = await message.channel.send("Testing Ping...")
        end_time = time.time()

        await message.edit(content=f"Pong! {round(client.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")

    if message.content.startswith('!give_admin'):
        await message.reply(file=discord.File('no.gif'))

    if message.content.startswith('!yoda'):
        content = message.content[6:]
        q = requests.get(
            "http://api.funtranslations.com/translate/yoda?text=" + content)
        print(q.json())
        await message.reply(q.json()['contents']['translated'])

    if message.content.startswith('!time'):
        date_time_now = datetime.now()
        await message.channel.send(date_time_now)

    if 'burger king' in message.content:
        await message.reply('Don\'t say that around me.')

    if message.content.startswith('!vertify'):
        splitMsg = message.content.split(' ')
        for word in splitMsg[1:]:
            await message.channel.send(word)

    if message.content.startswith('!xkcd'):
        await message.reply("https://xkcd.com/")


def log(message):
    data = pd.DataFrame(columns=['content', 'author', 'timestamp'])
    if message.content.startswith('$log'):
        print(message.content)

    data = data.append({'content': message.content, 'author': message.author.name,
                       'timestamp': message.created_at}, ignore_index=True)

    data.to_csv('log.csv', index=False)


def getToken():
    token = ""
    with open('token.txt', 'r') as f:
        token = f.read()
    return token


# Required to run the bot, make sure to replace <YOUR_API_TOKEN>!
client.run(getToken())
