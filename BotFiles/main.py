import asyncio
import developers
global dev_list
from generate import *
import helpText

@bot.event
async def on_guild_join(self):  # Logs when the bot joins a guild (does not log ID, so don't worry)
    servers = list(bot.guilds)
    channel = bot.get_channel(811010228945682432)
    joinServerEmbed = discord.Embed(title="Added to a new server!", description=f"New Server Total: **{str(len(servers))}**")
    await channel.send(embed=joinServerEmbed)


# ------General Commands------
@bot.command()
async def help(ctx):  # The help command
    helpEmbed = discord.Embed(title="Help Page",
                              description="__Bot Prefix is: **;**__\n**<>** - optional tag\n**[]** - required tag",
                              color=0xB87DDF
                              )
    helpEmbed.add_field(name="General Commands",
                        value=helpText.general,
                        inline=False
                        )
    helpEmbed.add_field(name="Random Generator Commands",
                        value=helpText.random,
                        inline=False
                        )
    helpEmbed.set_footer(text="Creator: Xarvatium#6561", icon_url="https://cdn.discordapp.com/avatars/514866599400833034/88a61a2683879b72622d4f9990dc6d2b.png?size=128")
    helpEmbed.set_author(name="The Random Bot", icon_url="https://cdn.discordapp.com/avatars/755986454907191319/5ff8f9b7b1eebb4650e8ee94e65c03d6.png?size=128")
    message = await ctx.channel.send(embed=helpEmbed)
    await message.add_reaction("❌")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["❌"]
        # This makes sure nobody except the command sender can interact with the "menu".

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
async def ping(ctx):  # ping command
    ping = bot.latency * 1000
    pingEmbed = discord.Embed(title="Pong! :ping_pong:", description=f"My latency is: **{int(ping)}ms**", color=0xB87DDF)
    await ctx.send(embed=pingEmbed)


@bot.command()
async def monke(ctx):  # :)
    await ctx.send(
        "https://tenor.com/view/obese-monkey-fat-monkey-summer-belly-eating-lettuce-summer-look-gif-13014350"
    )


@bot.command()
async def repeat(ctx, *, userinput = None):  # Repeat command
    sentByMention = str(ctx.author.mention)
    for s in ['/', ':', '***REMOVED***', '***REMOVED***', '***REMOVED***', '***REMOVED***']:  # A blacklist that changes the characters below with blank text
        userinput.replace(s, '')
    # Defining the embed to be used and it's field
    repeatEmbed = discord.Embed(description=userinput, color=0xB87DDF)
    repeatEmbed.add_field(name="Sent by:", value=sentByMention)
    if userinput:  # The If statement that checks for "im" or "@everyone"/"@here"
        if userinput.lower().startswith("im"):
            await ctx.send("yea we know")
        elif userinput.lower().startswith('i '):
            await ctx.send("yea we know")
        elif userinput.lower().startswith("i'm"):
            await ctx.send("yea we know")
        elif userinput.lower() == "@everyone":
            await ctx.send("no :)")
        elif userinput.lower() == "@here":
            await ctx.send("no :)")
        else:  # The else statement that sends the full message if it passes the previous el/if statements
            await ctx.send(embed=repeatEmbed)
    else:  # The else statement that checks if there is no user input argument
        # The error embed that sends if there is no argument
        noUserIn = discord.Embed(title="Error",
                                    description="Sorry! It appears you didn't include something for me to repeat!",
                                    color=0xC73333
                                )
        await ctx.channel.send(embed=noUserIn)


@bot.command()
async def ask(ctx, *, content):  # 8Ball module (used to be a separate file but caused issues)
    import random
    responses = ["It is certain", "Without a doubt", "You may rely on it", "Yes, definitely", "It is decidedly so",
            "As I see it, yes", "Most likely", "Yes", "Outlook good", "Signs point to yes", "Reply hazy try again",
            "Better not tell you now", "Ask again later", "Cannot predict now", "Concentrate and ask again",
            "Don't count on it", "Outlook not so good", "My sources say no", "Very doubtful", "My reply is no"]
    answer = random.choice(responses)
    await ctx.channel.send(answer)


# ------Developer Commands------
@bot.command()
async def servers(ctx):  # Developer command
    import developers
    servers = list(bot.guilds)
    serversEmbedTitle = f"Connected on {str(len(servers))} servers"
    serversEmbedDesc = "- " + '\n- '.join(guild.name for guild in servers)
    dev_list = developers.dev_list["Developers"]["User IDs"]
    serversEmbed = discord.Embed(title=serversEmbedTitle, description=serversEmbedDesc, color=0xB87DDF)

    notDevEmbed = discord.Embed(title="Error",
                                description="Sorry! It appears you don't have permission to use this command.",
                                color=0xC73333)
    if ctx.message.author.id in dev_list:
        await ctx.send(embed=serversEmbed)

    else:
        await ctx.channel.send(embed=notDevEmbed)


@bot.command()
async def status(ctx, *, content):  # Developer command that changes the bot's status
    dev_list = developers.dev_list["Developers"]["User IDs"]
    notDevEmbed = discord.Embed(title="Error",
                              description="Sorry! It appears you don't have permission to use this command.",
                              color=0xC73333)
    if ctx.message.author.id in dev_list:
        await bot.change_presence(
            activity=discord.Game(
                name=content
            )
        )
    else:
        await ctx.channel.send(embed=notDevEmbed)


# The Token initialization and Checking if config.json exists
if __name__ == '__main__':
    if not os.path.exists('config.json'):
        keysGen = str(input("ERROR: DID NOT FIND A CONFIG.JSON FILE\nWould you like to make a config.json file? (Y/N) ")).lower()
        if keysGen == 'y':
            config = {} # Create the empty dictionary for configuration
            print("----Note: We do not receive your API keys, these are stored in a file on your computer.----")
            print("The config.json file created by this should be considered sensitive. DO NOT share it with anyone.")
            config['ytApiKey'] = str(input("Please input your YouTube API Developer Key: "))
            config['lastFmKey'] = str(input("Please input your last.fm API key: "))
            config['lastFmUA'] = str(input("Please input the User Agent that should be used when requesting from the last.fm API: "))
            config['discordToken'] = str(input("Please input your Discord bot token: "))
            config['bannedWords'] = str(input("Please input a list of words you don't want the bot to repeat, seperated by a comma.")).split(',')
            config['developers'] = {} # Create the empty developers dictionary
            print("The next section will allow you to choose who to give access to developer commands. Developers will be able to change the bot's status, see bot statistics, and add other developers. Make sure you trust anyone you add.")
            print("Who will your first developer be? You'll be able to add other ones through the bot later.")
            config['developers'][str(input("User ID of the first dev: "))] = str(input("Name of the first dev: "))
            print("Setup complete, running the bot...")
            with open('config.json', 'w+') as configFile:
                json.dump(config, configFile, indent=4)
            generate_config_reload()
        elif keysGen == 'n':
            print("Exiting... Please remember to make a config.json file in order for the bot to be fully functional.")
            quit()
        print("Creating... Done! Your self-hosted bot is now live!")
        bot.run(config['discordToken'])
    elif os.path.exists('config.json'):
        with open('config.json') as configFile:
            config = json.load(configFile)
        generate_config_reload()
        bot.run(config['discordToken'])

