# Import the pycord library into your runtime.
import discord
from datetime import datetime
import os
import pandas as pd


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

    if message.content.startswith('#swack process_log'):
        processLog()
        await message.reply("Processed Log")
        return

    if not isinstance(message.channel, discord.DMChannel):
        log(message)


def log(message):
    createFile()
    data = pd.DataFrame(columns=['content', 'author', 'timestamp'])
    if message.content.startswith('$log'):
        print(message.content)

    try:
        df = pd.read_csv('log.csv')
    except:
        pass

    data = df.append({'content': message.content, 'author': message.author.name,
                      'timestamp': message.created_at}, ignore_index=True)

    data.to_csv('log.csv', index=False)


def createFile():
    if not os.path.exists('log.csv'):
        with open('log.csv', 'w') as f:
            f.write('content,author,timestamp\n')


def processLog():
    df = pd.read_csv('log.csv')
    print(len(df))
    for i in range(len(df)):
        print(df.iloc[i]['content'])
        print(df.iloc[i]['author'])
        print(df.iloc[i]['timestamp'])
        print("\n")

    authors = []
    strings = []
    # store the author and message content in a text file, each author is only allowed to have one message per day
    for i in range(len(df)):
        if not authors.__contains__(df.iloc[i]['author']):
            authors.append(df.iloc[i]['author'])
            strings.append(df.iloc[i]['content'])

    print(authors)
    print(strings)


def getToken():
    token = ""
    with open('token.txt', 'r') as f:
        token = f.read()
    return token


client.run(getToken())
