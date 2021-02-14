import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

from generate import *

@bot.command()
async def help(ctx):
    helpEmbed = discord.Embed(title="Help Page",
                              description="__Bot Prefix is: **;**__",
                              color=0xB87DDF
                              )
    helpEmbed.add_field(name="General Commands",
                        value="\;ping - checks the bot's latency\n;repeat - repeats what you say (in beta)\n;ask - gives 8Ball answers",
                        inline=False
                        )
    helpEmbed.add_field(name="Random Generator Commands",
                        value=";generate article - gives a random wikipedia article\n;generate video - gives a random YouTube video\n;generate number [low] [high] - gives a random number in between the two given values\n;generate color - gives a random color + it's hex and RGB code",
                        inline=False
                        )
    helpEmbed.set_footer(text="Creator: Xarvatium#6561", icon_url="https://cdn.discordapp.com/avatars/514866599400833034/88a61a2683879b72622d4f9990dc6d2b.png?size=128")
    helpEmbed.set_author(name="The Random Bot", icon_url="https://cdn.discordapp.com/avatars/755986454907191319/5ff8f9b7b1eebb4650e8ee94e65c03d6.png?size=128")
    message = await ctx.channel.send(embed=helpEmbed)
    await message.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️", "❌"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=180, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            if str(reaction.emoji) == "❌":
                await message.delete()
        except asyncio.TimeoutError:
            await message.delete()
            break
            # ending the loop if user doesn't react after x seconds


@bot.command()
async def status(ctx, *, content):
    import developers
    dev_list = developers.dev_list["Developers"]["User IDs"]
    if ctx.message.author.id in dev_list:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=content))

    else:
        await ctx.channel.send("Sorry! It appears you don't have permission to use this command.")


@bot.command()
async def ping(ctx):
    ping = bot.latency * 1000
    pingEmbed = discord.Embed(title="Pong! :ping_pong:", description=f"My latency is: {int(ping)}ms", color=0xB87DDF)
    await ctx.send(embed=pingEmbed)


@bot.command()
async def monke(ctx):
    await ctx.send(
        "https://tenor.com/view/obese-monkey-fat-monkey-summer-belly-eating-lettuce-summer-look-gif-13014350"
    )


@bot.command()
async def repeat(ctx, *, user_in: str):
    if user_in.lower().startswith("im"):
        await ctx.send("yea we know")
    elif user_in.lower().startswith('i '):
        await ctx.send("yea we know")
    elif user_in.lower().startswith("i'm"):
        await ctx.send("yea we know")
    elif user_in.lower() == "@everyone":
        await ctx.send("no :)")
    else:
        await ctx.send(user_in)

@bot.command()
async def ask(ctx, *, content):
    import random
    responses = ["It is certain", "Without a doubt", "You may rely on it", "Yes, definitely", "It is decidedly so",
            "As I see it, yes", "Most likely", "Yes", "Outlook good", "Signs point to yes", "Reply hazy try again",
            "Better not tell you now", "Ask again later", "Cannot predict now", "Concentrate and ask again",
            "Don't count on it", "Outlook not so good", "My sources say no", "Very doubtful", "My reply is no"]
    answer = random.choice(responses)
    await ctx.channel.send(answer)

# The Token initialization
with open("token.txt", 'r') as token:
    token1 = token.read()
bot.run(token1)

