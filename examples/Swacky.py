# Import the pycord library into your runtime.
import discord
from datetime import datetime
import os
import pandas as pd
from fpdf import FPDF
import random


client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    # channel id for the sandbox channel
    channel = client.get_channel(519591466058907669)
    # await channel.send('This is sent every time the bot is started, sorry if it gets annoying during testing :)')
    # await channel.send('Any messages sent in this channel after this message which are not from bots will be stored in a log file, this includes messages which are just a single emoji, or a single word.')
    # await channel.send('Please do not send any messages which contain emojis as this can cause issues when generating the output pdf')


@client.event
async def on_message(message):

    if message.author.bot:
        return

    if message.author == client.user:
        return

    if message.content.startswith('#swack process_log'):
        async with message.channel.typing():
            processLog()
        await message.reply("Processed Log")
        await message.reply(file=discord.File('Swack.pdf'))
        # await message.reply(file=discord.File('log.csv'))
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

    # Remove emojis from the data
    data = data.astype(str).apply(lambda x: x.str.encode(
        'ascii', 'ignore').str.decode('ascii'))

    # Remove double spaces from the data
    data['content'] = data['content'].str.replace(' {2,}', ' ', regex=True)

    data.to_csv('log.csv', index=False)


def createFile():
    if not os.path.exists('log.csv'):
        with open('log.csv', 'w') as f:
            f.write('content,author,timestamp\n')


def processLog():
    df = pd.read_csv('log.csv')
    """ print(len(df))
    for i in range(len(df)):
        print(df.iloc[i]['content'])
        print(df.iloc[i]['author'])
        print(df.iloc[i]['timestamp'])
        print("\n") """

    authors = []
    strings = []
    # store the author and message content in a text file, each author is only allowed to have one message per day
    for i in range(len(df)):
        if not authors.__contains__(df.iloc[i]['author']):
            authors.append(df.iloc[i]['author'])
            strings.append(df.iloc[i]['content'])

    print(authors)
    print(strings)

    pdf = FPDF()

    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size=15)

    random.shuffle(authors)

    contributors = "Contributors: "

    outString = ""
    for i in range(len(authors)):
        outString += strings[i] + ". "
        contributors += authors[i] + ", "
    outString += " \n"

    # create a cell
    pdf.multi_cell(200, 10, txt=outString,
                   align='L', border=0)

    # add another cell
    pdf.multi_cell(200, 10, txt=contributors,
                   align='J')

    pdf.image(name='swan_hack_logo.png', w=25, h=25)

    # save the pdf with name .pdf
    pdf.output("Swack.pdf")


def getToken():
    token = ""
    with open('token.txt', 'r') as f:
        token = f.read()
    return token


client.run(getToken())
