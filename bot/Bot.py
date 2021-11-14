import time

import discord
import pause
import requests
from discord import Embed
from discord.ext import commands
import datetime

client = commands.Bot(command_prefix=".", help_command=None)


@client.event
async def on_ready():
    print("Ready")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=".help"))
    await check_picture()

async def check_picture():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    pause.until(int(time.mktime(datetime.datetime.strptime(str(tomorrow), "%Y-%m-%d").timetuple())) + 1)
    await send_to_day_picture()
    pause.until(int(time.mktime(datetime.datetime.strptime(str(tomorrow), "%Y-%m-%d").timetuple())) + 2)
    await check_picture()


async def send_to_day_picture():
    request = requests.get("https://api.nasa.gov/planetary/apod?api_key=oQhM7q2xBtR10u4pjawCmF4HKGtc8a7ewS9mL6W6")
    response = request.json()
    embed = Embed(title=f"{response['title']}",
                  description=f"{response['explanation']}", )
    embed.set_image(url=f"{response['url']}")
    embed.set_thumbnail(url="https://imgur.com/fzL7duE.jpg")
    embed.add_field(name="\nAuthor of picture:", value=response['copyright'], inline=True)
    embed.add_field(name="Date:", value=response['date'], inline=True)
    embed.set_footer(
        text=f"Bot realized by @Kijusu#9602"
    )
    channel = client.get_channel(909529006313988106)
    await channel.send(embed=embed)

client.run("OTA4NzkxOTIyNTYxMjUzNDA2.YY64bg.tIryTPaFurQuriZ-qburrcV0K14")
