import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
import glob, os, os.path
import sys
import fileinput
import asyncio

client: Bot = commands.Bot(command_prefix='+') # Prefrix of the bot
client.remove_command('help') # removes the basic help command
TOKEN = '' #empty


#----------------------------------------
# Start of the code
#----------------------------------------

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='+help'))
    print(f'Logged in as {client.user}')
    print('----------------------------')
    print(f'ID: {client.user.id}')
    print('----------------------------')
    print(f'Guilds: {len(client.guilds)}')
    print('----------------------------')
    print(f'Members: {len(set(client.get_all_members()))}')


@client.event
async def on_guild_join(guild): # when the bot joins a guild
    f = open(f"{guild.id}-words.txt", "w")
    f.write(f"nigga\nbitch\nnegga\nfuck you\nson of a bitch\nwhore\nfuck u\nbastard")
    f.close()
    f2 = open(f"{guild.id}-modmail-checking", "w")
    f2.write('false')
    f2.close()
    open(f"./MuteRoles/{guild.id}-mute-role.txt", "x")
    channel = client.get_channel(697830313879011389)
    await channel.send(f'New guild: **{guild.name}** (ID: **{guild.id}**)')
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        client.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    channel = await guild.create_text_channel(name='welcome-tools', overwrites=overwrites)
    welcome_embed = discord.Embed(color=0xfd9fb9, title='<a:Wave:723567545927335957> Hey there!', description="Thanks for adding me to the server! <a:Dance:723567543096311892> \n \nOk, let's start with some basic information. I'd suggest setting up some stuff first. No worries, I'll help you.\n \nLet's start with setting up a log channel. You can simply do that, by typing the following command: \n**+setlog [channel]** \n \nGreat, let's move on. The next you can do, is setting up a welcome message and a welcome channel. There are some really useful parameters, that you can use for this. Let me show it to you: \n **+setmsg Hey {mention}! Welcome to {guild}, you're member number {members}!** \n \nLet's set up a channel for this messages: \n**+setwelcome [channel]** \n \nSweet! So, the last thing we should do, is tp set up a mute role. This is also very simple, just to the following: \n**+muterole [role]** \n \nRemember to **__not__** include the **[ ]** when you're executing the commands. \n \nAnyway, looks like we set up everything! If you still have any questions, feel free to join the support server [here](https://discord.gg/S9BEBux). \nYou want to invite the bot to another server? Simply click [here](https://discordapp.com/oauth2/authorize?client_id=697487580522086431&scope=bot&permissions=2146958847)! \n \nFeel free to delete this channel. You can see all my commands, by typing **+help** or **+help dm** into a channel.")
    await channel.send(embed=welcome_embed)


@client.event
async def on_guild_remove(guild): # when the bot gets removed from a guild 
    channel = client.get_channel(697830245725896705)
    await channel.send(f'Removed from guild: **{guild.name}** (ID: **{guild.id}**)')


@client.event
async def on_message(message): # Word filter event  	                                                           ffggghhuhggfdrsw                                                                      
    if message.author.guild_permissions.ban_members:
        await client.process_commands(message)
        return
    guild = message.guild
    message_content = message.content.strip().lower()
    with open(f"{guild.id}-words.txt") as f:
        bad_words = [bad_words.strip().lower() for bad_words in f.readlines()]
        for bad_words in bad_words:
            if bad_words in message_content:
                await message.delete()
                await message.channel.send(f"Hey {message.author.mention}, don't use words like that!")
    await client.process_commands(message)


@client.command()
@commands.has_permissions(ban_members=True)
async def add(ctx, *, word = None): # Adds a new word to the filter
    message_content = ctx.message.content.strip().lower()
    with open(f"{ctx.message.guild.id}-words.txt") as f2:
        bad_words = [bad_words.strip().lower() for bad_words in f2.readlines()]
        for bad_words in bad_words:
            if bad_words in message_content:
                e = discord.Embed(color=0xfd9fb9, description='Sorry, but that word is already in the filter!')
                e.set_author(name='Error: Word already registered', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
                await ctx.send(embed=e)
                return
    if word == None:
        e2 = discord.Embed(color=0xfd9fb9, description='Please enter a valid word!')
        e2.set_author(name='Error: Invalid word', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    f = open(f"{ctx.message.guild.id}-words.txt", "a")
    f.write(f"\n{word}")
    f.close()
    e3 = discord.Embed(color=0xfd9fb9, description='Succesfully added the word to the filter!')
    e3.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
    await ctx.send(embed=e3)


@client.command()
@commands.has_permissions(ban_members=True)
async def remove(ctx, *, altWord = None): # removes a word from the filter 
    guild = ctx.message.guild
    if altWord == None:
        e2 = discord.Embed(color=0xfd9fb9, description='Please enter a valid word!')
        e2.set_author(name='Error: Invalid word', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    for line in fileinput.input(f"{guild.id}-words.txt", inplace=-1):
        sys.stdout.write(line.replace(altWord, '--------------'))




#@client.command()
#async def corn(ctx):
    #welcome_embed = discord.Embed(color=0xfd9fb9, title='<a:Wave:723567545927335957> Hey there!', description="Thanks for adding me to the server! <a:Dance:723567543096311892> \n \nOk, let's start with some basic information. I'd suggest setting up some stuff first. No worries, I'll help you.\n \nLet's start with setting up a log channel. You can simply do that, by typing the following command: \n**+setlog [channel]** \n \nGreat, let's move on. The next you can do, is setting up a welcome message and a welcome channel. There are some really useful parameters, that you can use for this. Let me show it to you: \n **+setmsg Hey {mention}! Welcome to {guild}, you're member number {members}!** \n \nLet's set up a channel for this messages: \n**+setwelcome [channel]** \n \nSweet! So, the last thing we should do, is tp set up a mute role. This is also very simple, just to the following: \n**+muterole [role]** \n \nRemember to **__not__** include the **[ ]** when you're executing the commands. \n \nAnyway, looks like we set up everything! If you still have any questions, feel free to join the support server [here](https://discord.gg/S9BEBux). \nYou want to invite the bot to another server? Simply click [here](https://discordapp.com/oauth2/authorize?client_id=697487580522086431&scope=bot&permissions=2146958847)! \n \nFeel free to delete this channel. You can see all my commands, by typing **+help** or **+help dm** into a channel.")
    #await ctx.send(embed=welcome_embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def showlist(ctx): # shows the filter
    guild = ctx.message.guild
    f = open(f"{guild.id}-words.txt", "r")
    words = f.read()
    embed = discord.Embed(color=0xfd9fb9, description=f'{words}')
    embed.set_author(name=f'Filter list for {guild.name}', icon_url=guild.icon_url)
    embed.set_footer(text="-------------- = deleted words")
    await ctx.send(embed=embed)



@client.group()
async def help(ctx): # The help command
    if ctx.invoked_subcommand is None:
        bot = client.get_user(697487580522086431)
        e = discord.Embed(color=0xfd9fb9)
        e.set_author(name='Command List', icon_url=bot.avatar_url)
        e.set_footer(text=f'Invoked by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        e.add_field(name='**<:585765206769139723:701821061263785985> Word Filter**', value='+add `[word]` **|** Adds a word to the filter \n+remove `[word]` **|** Removes a word from the filter \n+showlist **|** Shows a list of the filtered words', inline=False)
        e.add_field(name='**<:dnd:705582091106123786> Warn System**', value='**If the user gets their 3rd warn, they will automatically get banned** \n+warn `[mention or id]` `[reason]` **|** Warns the user \n+warnings `[mention or id]` **|** Shows the warnings of the user \n+clearwarns `[mention or id]` **|** Clears all warnings of the user', inline=False)
        e.add_field(name='**📨 Modmail System**', value='+modmail enable **|** Enables the Modmail system \n+modmail disable **|** Disables the Modmail system \n+modmail send `[text]` **|** Sends a message to the mods \n+modmail modchannel `[ID or mention]` **|** Sets a channel for incoming messages \n+modmail userchannel `[ID or mention]` **|** Sets a channel for the users \n+modmail respond `[ID or mention]` `[text]` **|** Responds to a message \n+modmail status **|** Shows the current Modmail system status', inline=False)
        e.add_field(name='**<:585765895939424258:701821042183635046> User Commands**', value='+poll `[text]` **|** Creates a classic poll \n +av `[ID or mention]` **|** Shows the avatar \n+addrole `[ID or mention]` `[role ID/mention/name]` **|** Adds a specific role \n+removerole `[ID or mention]` `[role ID/mention/name]` **|** Removes a specific role\n +info `[ID or mention]` **|** Shows info about the user \n+nickname `[ID or mention]` `[nickname]` **|** Changes the nickname of the member \n+hug `[mention or id]` **|** Hugs the user \n+fight `[mention or id]` **|** Fights the user', inline=False)
        e.add_field(name='**<:Staff:723200944266936411> Mod Commands**', value='+setlog `[ID or mention]` **|** Sets a log channel \n+softban `[ID or mention]` `[reason]`**|** Softbans a member \n+ban `[ID or mention]` `[reason]` **|** Bans a user \n+kick `[ID or mention]` `[reason]` **|** Kicks the user \n +purge `[amount]` **|** Purges a specific amount of messages \n+muterole `[role ID, mention or name]` **|** Sets a mute role \n+mute `[mention or ID]` `[time in minutes]` `[reason]` **|** Mutes a member for a specific amount of time \n+slowmode `[mention or ID]` `[time in seconds]` **|** Sets the channel slowmode \n+guildinfo **|** Shows info about the guild ' , inline=False)
        e.add_field(name='**<:welcome:706272444864004106> Welcome System**', value='+welcomeinfo **|** Shows a list of usable welcome message args \n+setwelcome `[ID or mention]` **|** Sets a welcome channel \n+setmsg `[text]` **|** Sets a welcome message \n+welcomestatus **|** Shows the current welcome message & channel', inline=False)
        e.add_field(name='**<:697686848545488986:701821086928732161> Bot Commands**', value='+invite **|** Get an invite for the bot \n+botinfo **|** Shows info about the bot \n+help `[dm]` **|** Shows this help message. Add **dm** to get the command in DMs', inline=False)
        await ctx.message.channel.trigger_typing()
        await ctx.send(embed=e)



@help.command()
async def dm(ctx):
    bot = client.get_user(697487580522086431)
    e = discord.Embed(color=0xfd9fb9)
    e.set_author(name='Command List', icon_url=bot.avatar_url)
    e.set_footer(text=f'Invoked by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
    e.add_field(name='**<:585765206769139723:701821061263785985> Word Filter**', value='+add `[word]` **|** Adds a word to the filter \n+remove `[word]` **|** Removes a word from the filter \n+showlist **|** Shows a list of the filtered words', inline=False)
    e.add_field(name='**<:dnd:705582091106123786> Warn System**', value='**If the user gets their 3rd warn, they will automatically get banned** \n+warn `[mention or id]` `[reason]` **|** Warns the user \n+warnings `[mention or id]` **|** Shows the warnings of the user \n+clearwarns `[mention or id]` **|** Clears all warnings of the user', inline=False)
    e.add_field(name='**📨 Modmail System**', value='+modmail enable **|** Enables the Modmail system \n+modmail disable **|** Disables the Modmail system \n+modmail send `[text]` **|** Sends a message to the mods \n+modmail modchannel `[ID or mention]` **|** Sets a channel for incoming messages \n+modmail userchannel `[ID or mention]` **|** Sets a channel for the users \n+modmail respond `[ID or mention]` `[text]` **|** Responds to a message \n+modmail status **|** Shows the current Modmail system status', inline=False)
    e.add_field(name='**<:585765895939424258:701821042183635046> User Commands**', value='+poll `[text]` **|** Creates a basic poll \n+av `[ID or mention]` **|** Shows the avatar \n+addrole `[ID or mention]` `[role ID/mention/name]` **|** Adds a specific role \n+removerole `[ID or mention]` `[role ID/mention/name]` **|** Removes a specific role\n +info `[ID or mention]` **|** Shows info about the user \n+nickname `[ID or mention]` `[nickname]` **|** Changes the nickname of the member \n+hug `[mention or id]` **|** Hugs the user \n+fight `[mention or id]` **|** Fights the user', inline=False)
    e.add_field(name='**<:Staff:723200944266936411> Mod Commands**', value='+setlog `[ID or mention]` **|** Sets a log channel \n+softban `[ID or mention]` `[reason]`**|** Softbans a member \n+muterole `[role ID, mention or name]` **|** Sets a mute role \n+mute `[mention or ID]` `[time in minutes]` `[reason]` **|** Mutes a member for a specific amount of time \n+ban `[ID or mention]` `[reason]` **|** Bans a user \n+kick `[ID or mention]` `[reason]` **|** Kicks the user \n +lock `[channel]` `[time in seconds]` **|** Locks a channel \n +purge `[amount]` **|** Purges a specific amount of messages \n+slowmode `[mention or ID]` `[time in seconds]` **|** Sets the channel slowmode \n+guildinfo **|** Shows info about the guild ' , inline=False)
    e.add_field(name='**<:welcome:706272444864004106> Welcome System**', value='+welcomeinfo **|** Shows a list of usable welcome message args \n+setwelcome `[ID or mention]` **|** Sets a welcome channel \n+setmsg `[text]` **|** Sets a welcome message \n+welcomestatus **|** Shows the current welcome message & channel', inline=False)
    e.add_field(name='**<:697686848545488986:701821086928732161> Bot Commands**', value='+invite **|** Get an invite for the bot \n+botinfo **|** Shows info about the bot \n+help `[dm]` **|** Shows this help message. Add **dm** to get the command in DMs', inline=False)
    await ctx.message.channel.trigger_typing()
    e2 = discord.Embed(color=0xfd9fb9, description='Check your private messages! 📬')
    await ctx.send(embed=e2)
    await ctx.message.author.send(embed=e)




@client.command()
@commands.has_permissions(manage_messages=True)
async def av(ctx, member: discord.Member = None): # shows the avatar
    if member == None:
        member = ctx.message.author
    elif member == member.id:
        member = member
    e = discord.Embed(color=0xfd9fb9)
    e.set_author(name=f"{member}'s avatar")
    e.set_image(url=member.avatar_url)
    e.set_footer(text=f'Invoked by {ctx.message.author}')
    await ctx.send(embed=e)




@client.command()
@commands.has_permissions(ban_members=True)
async def slowmode(ctx, channel: discord.TextChannel = None, *, time: int = None): # changes the slowmode
    if channel == None:
        e2 = discord.Embed(color=0xfd9fb9, description='Please mention a valid channel or enter a valid channel id!')
        e2.set_author(name='Error: Invalid channel', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    if time == None:
        e3 = discord.Embed(color=0xfd9fb9, description='Please enter a valid time!')
        e3.set_author(name='Error: Invalid time', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e3)
        return
    if channel == channel.id:
        channel = channel
    await channel.edit(slowmode_delay=time)
    e4 = discord.Embed(color=0xfd9fb9, description=f'Succesfully changed the slowmode for {channel.mention} to **{time}** seconds!')
    e4.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
    await ctx.send(embed=e4)



@client.command()
@commands.has_permissions(manage_messages=True)
async def nickname(ctx, member: discord.Member = None, *, name = None): # changes the nickname 
    if name == None:
        e2 = discord.Embed(color=0xfd9fb9, description='Please mention a valid name!')
        e2.set_author(name='Error: Invalid name', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    if member == None:
        e3 = discord.Embed(color=0xfd9fb9, description='Please mention a valid member or enter a valid member id!')
        e3.set_author(name='Error: Invalid member', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e3)
        return
    if member == member.id:
        member = member
    await member.edit(nick=name)
    e4 = discord.Embed(color=0xfd9fb9, description=f'Succesfully changed the nickname of {member.mention} to **{name}** seconds!')
    e4.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
    await ctx.send(embed=e4)



@client.command()
@commands.has_permissions(manage_messages=True)
async def info(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.message.author
    elif member == member.id:
        member = member
    roles = [role for role in member.roles]
    e4 = discord.Embed(color=0xfd9fb9, timestamp=ctx.message.created_at, description=f'[Avatar]({member.avatar_url})')
    e4.set_author(name=f'{member}', icon_url=member.avatar_url)
    e4.add_field(name=f'Roles ({len(roles)}):', value=f' '.join([role.mention for role in roles]), inline=False)
    e4.add_field(name='Created at:', value=f"{member.created_at.strftime('%a, %m/%e/%Y, %H:%M')}", inline=False)
    e4.add_field(name='Joined at:', value=f"{member.joined_at.strftime('%a, %m/%e/%Y, %H:%M')}", inline=False)
    e4.set_footer(text=f'User ID: {member.id}')
    await ctx.send(embed=e4)

@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = None):
    if amount == None:
        e3 = discord.Embed(color=0xfd9fb9, description='Please enter a valid amount of messages between 1 and 50')
        e3.set_author(name='Error: Invalid amount', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e3)
        return
    if amount > 50:
        e7 = discord.Embed(color=0xfd9fb9, description='Sorry, but I can only delete 50 messages at one time!')
        e7.set_author(name='Error: Too many messages', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e7)
        return
    await ctx.message.channel.purge(limit=amount)
    e4 = discord.Embed(color=0xfd9fb9, description=f'Successfully deleted **{amount}** messages in {ctx.message.channel.mention}!')
    e4.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
    await ctx.send(embed=e4)
    


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason = None):
    if member == ctx.message.author:
        e7 = discord.Embed(color=0xfd9fb9, description="Sorry, but you can't kick yourself!")
        e7.set_author(name='Error: Author', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e7)
        return
    if member == None:
        e3 = discord.Embed(color=0xfd9fb9, description='Please mention a valid member or enter a valid member id!')
        e3.set_author(name='Error: Invalid member', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e3)
        return
    if member == member.id:
        member = member
    if reason == None:
        reason = 'No reason provided'
    e = discord.Embed(color=0xfd9fb9, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**) \nReason: **{reason}**")
    e.set_author(name='User kicked')
    await member.kick(reason=reason)
    e4 = discord.Embed(color=0xfd9fb9, description=f'{ctx.message.author.mention} successfully kicked {member.mention} for **{reason}**!')
    e4.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
    await ctx.send(embed=e4)
    guild = ctx.message.guild
    f = open(f"{guild.id}-log.txt", "r")
    channel_id = f.read()
    log_channel = await client.fetch_channel(channel_id)
    await log_channel.send(embed=e)



@client.command()
@commands.has_permissions(ban_members=True)
async def welcomeinfo(ctx):
    e = discord.Embed(color=0xfd9fb9, description='**{mention}** - Mentions the user \n**{members}** - Shows the current member count \n**{guild}** - Shows the guild name \n**{member}** - Shows the name of the user \n \nYou can add these arguments to your welcome message')
    e.set_author(name='Usable args for the welcome message', icon_url=ctx.message.guild.icon_url)
    await ctx.send(embed=e)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason = None): # ban command
    if member == ctx.message.author:
        e7 = discord.Embed(color=0xfd9fb9, description="Sorry, but you can't ban yourself!")
        e7.set_author(name='Error: Author', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e7)
        return
    if member == None:
        e3 = discord.Embed(color=0xfd9fb9, description='Please mention a valid member or enter a valid member id!')
        e3.set_author(name='Error: Invalid member', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e3)
        return
    if member == member.id:
        member = member
    if reason == None:
        reason = 'No reason provided'
    await member.ban(reason=reason)
    e = discord.Embed(color=0xfd9fb9, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**) \nReason: **{reason}**")
    e.set_author(name='User banned')
    e4 = discord.Embed(color=0xfd9fb9, description=f'{ctx.message.author.mention} successfully banned {member.mention} for **{reason}**!')
    e4.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
    await ctx.send(embed=e4)
    guild = ctx.message.guild
    f = open(f"{guild.id}-log.txt", "r")
    channel_id = f.read()
    log_channel = await client.fetch_channel(channel_id)
    await log_channel.send(embed=e)






@client.command()
async def botinfo(ctx): # info about teh bot
    bot = client.get_user(697487580522086431)
    e = discord.Embed(color=0xfd9fb9, description=F'**Name:** {bot} \n**ID:** {bot.id} \n**Prefix:** + \n \n**Servers:** {len(client.guilds)} \n**Members:** {len(set(client.get_all_members()))} \n**Ping:** {round(client.latency * 1000)}ms \n \n**Library:** discord.py \n**GitHub Repo:** [Click here](https://github.com/EzZz1337/Tools)')
    e.set_author(name='Info about Tools')
    e.set_thumbnail(url=bot.avatar_url)
    e.set_footer(text=f'Invoked by {ctx.message.author}')
    await ctx.send(embed=e)


@client.command()
@commands.has_permissions(administrator=True)
async def setlog(ctx, channel: discord.TextChannel = None): # sets a log channel
    if channel == None:
        e2 = discord.Embed(color=0xfd9fb9, description='Please mention a valid channel or enter a valid channel id!')
        e2.set_author(name='Error: Invalid channel', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    guild = ctx.message.guild
    f = open(f"{guild.id}-log.txt", "w")
    f.write(f"{channel.id}")
    f.close()
    e4 = discord.Embed(color=0xfd9fb9, description=f'Successfully set the log channel to {channel.mention}!')
    e4.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
    await ctx.send(embed=e4)


@client.command()
@commands.has_permissions(ban_members=True)
async def removerole(ctx, member: discord.Member = None, *, role: discord.Role = None): # reoves a role
    if member == None:
        e2 = discord.Embed(color=0xfd9fb9, description='Please mention a valid member or enter a valid member id!')
        e2.set_author(name='Error: Invalid member', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    if role == None:
        e3 = discord.Embed(color=0xfd9fb9, description='Please enter a valid role name/id or mention a valid role!')
        e3.set_author(name='Error: Invalid role', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e3)
        return
    if member == member.id:
        member = member
    if role == role.id:
        role = role
    await member.remove_roles(role)
    e4 = discord.Embed(color=0xfd9fb9, description=f'Successfully removed the role {role.mention} from {member.mention}!')
    e4.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
    await ctx.send(embed=e4)



@client.command()
@commands.has_permissions(ban_members=True)
async def addrole(ctx, member: discord.Member = None, *, role: discord.Role = None): # adds role
    if member == None:
        e2 = discord.Embed(color=0xfd9fb9, description='Please mention a valid member or enter a valid member id!')
        e2.set_author(name='Error: Invalid member', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    if role == None:
        e3 = discord.Embed(color=0xfd9fb9, description='Please enter a valid role name/id or mention a valid role!')
        e3.set_author(name='Error: Invalid role', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e3)
        return
    if member == member.id:
        member = member
    if role == role.id:
        role = role
    await member.add_roles(role)
    e4 = discord.Embed(color=0xfd9fb9, description=f'Successfully added the role {role.mention} to {member.mention}!')
    e4.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
    await ctx.send(embed=e4)


@client.command()
@commands.has_permissions(ban_members=True)
async def warn(ctx, member: discord.Member = None, *, reason = None): # warns a member
    guild = ctx.message.guild
    if member == None:
        e3 = discord.Embed(color=0xfd9fb9, description='Please mention a valid member or enter a valid member id!')
        e3.set_author(name='Error: Invalid member', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e3)
        return
    if member == ctx.message.author:
        e7 = discord.Embed(color=0xfd9fb9, description="Sorry, but you can't warn yourself!")
        e7.set_author(name='Error: Author', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e7)
        return
    if member == member.id:
        member = member
    if reason == None:
        reason = 'No reason provided'
    if not os.path.exists(f"{guild.id}-{member.id}-warns.txt"):
        with open(f"{guild.id}-{member.id}-warns.txt", "w") as f10:
            f10.write("1")
            f10.close()
            e4 = discord.Embed(color=0xfd9fb9, description=f'{ctx.message.author.mention} successfully warned {member.mention} for **{reason}**!')
            e4.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
            await ctx.send(embed=e4)
            if os.path.exists(f"{guild.id}-log.txt"):
                f9 = open(f"{guild.id}-log.txt", "r")
                log_id = f9.read()
                log_channel = await client.fetch_channel(log_id)
                e = discord.Embed(color=0xfd9fb9, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**) \nReason: **{reason}**")
                e.set_author(name='User warned')
                await log_channel.send(embed=e)
            else:
                pass
            return
    if os.path.exists(f"{guild.id}-{member.id}-warns.txt"):
        f = open(f"{guild.id}-{member.id}-warns.txt", "r")
        global warns
        warns = f.read()
        if warns == '0':
            f2 = open(f"{guild.id}-{member.id}-warns.txt", "w")
            f2.write('1')
            f2.close()
            e5 = discord.Embed(color=0xfd9fb9, description=f"{ctx.message.author.mention} successfully warned {member.mention} for **{reason}**!")
            e5.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
            await ctx.send(embed=e5)
            if os.path.exists(f"{guild.id}-log.txt"):
                f9 = open(f"{guild.id}-log.txt", "r")
                log_id = f9.read()
                log_channel = await client.fetch_channel(log_id)
                e = discord.Embed(color=0xfd9fb9, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**) \nReason: **{reason}**")
                e.set_author(name='User warned')
                await log_channel.send(embed=e)
            else:
                pass
            return
        if warns == '1':
            f3 = open(f"{guild.id}-{member.id}-warns.txt", "w")
            f3.write('2')
            f3.close()
            e6 = discord.Embed(color=0xfd9fb9, description=f'{ctx.message.author.mention} successfully warned {member.mention} for **{reason}**!')
            e6.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
            await ctx.send(embed=e6)
            if os.path.exists(f"{guild.id}-log.txt"):
                f9 = open(f"{guild.id}-log.txt", "r")
                log_id = f9.read()
                log_channel = await client.fetch_channel(log_id)
                e = discord.Embed(color=0xfd9fb9, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**) \nReason: **{reason}**")
                e.set_author(name='User warned')
                await log_channel.send(embed=e)
            else:
                pass
            return
        if warns == '2':
            f4 = open(f"{guild.id}-{member.id}-warns.txt", "w")
            f4.write('0')
            f4.close()
            await member.ban(reason=reason)
            e9 = discord.Embed(color=0xfd9fb9, description=f"Looks like {member.mention} has been warned to often and now they're banned!")
            e9.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
            await ctx.send(embed=e9)
            if os.path.exists(f"{guild.id}-log.txt"):
                f9 = open(f"{guild.id}-log.txt", "r")
                log_id = f9.read()
                log_channel = await client.fetch_channel(log_id)
                e = discord.Embed(color=0xfd9fb9, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**) \nReason: **{reason}**")
                e.set_author(name='User banned (3 warns)')
                await log_channel.send(embed=e)
            else:
                pass
            return



@client.command()
@commands.has_permissions(ban_members=True)
async def clearwarns(ctx, member: discord.Member = None): # clears the warnings of a member
    guild = ctx.message.guild
    if member == None:
        e3 = discord.Embed(color=0xfd9fb9, description='Please mention a valid member or enter a valid member id!')
        e3.set_author(name='Error: Invalid member', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e3)
        return
    if member == member.id:
        member = member
    if os.path.exists(f"{guild.id}-{member.id}-warns.txt"):
        f = open(f"{guild.id}-{member.id}-warns.txt", "w")
        f.write('0')
        e9 = discord.Embed(color=0xfd9fb9, description=f"Successfully cleard the warnings of {member.mention}!")
        e9.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
        await ctx.send(embed=e9)
        if os.path.exists(f"{guild.id}-log.txt"):
                f9 = open(f"{guild.id}-log.txt", "r")
                log_id = f9.read()
                log_channel = await client.fetch_channel(log_id)
                e = discord.Embed(color=0xfd9fb9, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**)")
                e.set_author(name='Warns cleared')
                await log_channel.send(embed=e)
        else:
            pass
    else:
        await ctx.send('Looks like something went wrong...')




@client.command()
@commands.has_permissions(ban_members=True)
async def warnings(ctx, member: discord.Member = None): # shows the amount of warnings a member currently has
    guild = ctx.message.guild
    if member == None:
        e3 = discord.Embed(color=0xfd9fb9, description='Please mention a valid member or enter a valid member id!')
        e3.set_author(name='Error: Invalid member', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e3)
        return
    if member == member.id:
        member = member
    if os.path.exists(f"{guild.id}-{member.id}-warns.txt"):
        f = open(f"{guild.id}-{member.id}-warns.txt", "r")
        warns = f.read()
        e3 = discord.Embed(color=0xfd9fb9, description=f'{member.mention} currently has **{warns}** warning(s)!')
        await ctx.send(embed=e3)
    else:
        await ctx.send('Looks like something went wrong...')



@client.command()
@commands.has_permissions(administrator=True)
async def setmsg(ctx, *, text = None): # sets a welcome message
    g = ctx.message.guild
    if text == None:
        e3 = discord.Embed(color=0xfd9fb9, description='Please enter a valid text!')
        e3.set_author(name='Error: Invalid text', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e3)
        return
    f = open(f"{g.id}-welcome-msg.txt", "w")
    f.write(text)
    f.close()
    e9 = discord.Embed(color=0xfd9fb9, description=f"Successfully set the welcome message!")
    e9.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
    await ctx.send(embed=e9)


@client.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, channel: discord.TextChannel = None): # sets a welcome message channel
    g = ctx.message.guild
    if channel == None:
        e2 = discord.Embed(color=0xfd9fb9, description='Please mention a valid channel or enter a valid channel id!')
        e2.set_author(name='Error: Invalid channel', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    if channel == channel.id:
        channel = channel
    c_id = channel.id
    f = open(f"{g.id}-welcome-channel.txt", "w")
    f.write(f"{c_id}")
    f.close()
    e9 = discord.Embed(color=0xfd9fb9, description=f"Successfully set the welcome channel to {channel.mention}!")
    e9.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
    await ctx.send(embed=e9)


@client.command()
@commands.has_permissions(administrator=True)
async def welcomestatus(ctx): # shows the current welcome message & channel
    g = ctx.message.guild
    if os.path.exists(f"{g.id}-welcome-channel.txt") and os.path.exists(f"{g.id}-welcome-msg.txt"):
        f = open(f"{g.id}-welcome-channel.txt", "r")
        welcome_channel_id = f.read()
        welcome_channel = await client.fetch_channel(welcome_channel_id)
        f2 = open(f"{g.id}-welcome-msg.txt", "r")
        welcome_msg = f2.read()
        e = discord.Embed(color=0xfd9fb9)
        e.set_author(name=f'Server welcoming status for {g.name}', icon_url=g.icon_url)
        e.add_field(name='**Welcome message channel:**', value=f'{welcome_channel.mention}', inline=False)
        e.add_field(name='**Welcome message:**', value=f'{welcome_msg}', inline=False)
        e.set_footer(text=f'Invoked by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=e)
    else:
        e2 = discord.Embed(color=0xfd9fb9, description="Sorry, but either you don't have set a welcome message or a welcome channel. Please set both to see the server welcoming status.")
        e2.set_author(name='Error: No welcome message/channel set', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)



@client.command()
@commands.has_permissions(ban_members=True)
async def guildinfo(ctx): # shows info aout the guild
    g = ctx.guild
    e = discord.Embed(color=0xfd9fb9, title=f'__Guild info for {g.name}__', description=f'Name: **{g.name}** \nID: **{g.id}** \nOwner: {g.owner.mention} \nOwner ID: **{g.owner_id}** \n \nRoles: **{len(g.roles)}** \nEmojis: **{len(g.emojis)}** \n \nCategories: **{len(g.categories)}** \nVoice channels: **{len(g.voice_channels)}** \nText channels: **{len(g.text_channels)}** \n \nMax members: **{g.max_members}** \nMembers: **{len(g.members)}**')
    e.set_thumbnail(url=g.icon_url)
    e.set_footer(text=f'Invoked by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=e)



@client.event
async def on_member_join(member): # welcome event
    guild = client.get_guild(712832986642645004)
    g = member.guild
    g2 = client.get_guild(701041308810084362)
    g3 = client.get_guild(708657755577253930)
    if g == guild:
        log = client.get_channel(713028985541623841)
        embed = discord.Embed(color=0x7289DA, description=f"**Neuer User** \nUser: {member.mention} \n \nUser Name: **{member}** \n \nUser ID: **{member.id}**")
        await log.send(embed=embed)
        return
    if g == g3:
        role = discord.utils.get(g3.roles, name="Detectives")
        await member.add_roles(role)
        await member.send(f"Thanks for joining the server **{member.name}**! \nRemember to always follow the #rules and to have fun here. \nAnyway: **Nine-Nine!**")
        return
    if g == g2:
        log2 = client.get_channel(701959960208343141)
        embed2 = discord.Embed(color=0x7289DA, description=f"**Neuer User** \nUser: {member.mention} \n \nUser Name: **{member}** \n \nUser ID: **{member.id}**")
        await log2.send(embed=embed2)
        f = open(f"{g.id}-welcome-channel.txt", "r")
        welcome_channel_id = f.read()
        welcome_channel = await client.fetch_channel(welcome_channel_id)
        f2 = open(f"{g.id}-welcome-msg.txt", "r")
        welcome_msg = f2.read()
        members = len(list(member.guild.members))
        mention = member.mention
        member = member.name
        guild = member.guild
        await welcome_channel.send(str(welcome_msg).format(members=members, member=member, guild=guild, mention=mention))
        return
    f = open(f"{g.id}-welcome-channel.txt", "r")
    welcome_channel_id = f.read()
    welcome_channel = await client.fetch_channel(welcome_channel_id)
    f2 = open(f"{g.id}-welcome-msg.txt", "r")
    welcome_msg = f2.read()
    members = len(list(member.guild.members))
    mention = member.mention
    member = member.name
    guild = member.guild
    await welcome_channel.send(str(welcome_msg).format(members=members, member=member, guild=guild, mention=mention))


@client.event
async def on_member_remove(member):
    guild = client.get_guild(712832986642645004)
    g = member.guild
    g2 = client.get_guild(701041308810084362)
    if g == guild:
        log = client.get_channel(713029013483946054)
        embed = discord.Embed(color=0x7289DA, description=f"**User hat den Server verlassen** \nUser Name: **{member}** \n \nUser ID: **{member.id}**")
        await log.send(embed=embed)
        return
    if g == g2:
        log2 = client.get_channel(701959960208343141)
        embed2 = discord.Embed(color=0x7289DA, description=f"**User hat den Server verlassen** \nUser Name: **{member}** \n \nUser ID: **{member.id}**")
        await log2.send(embed=embed2)
        return


@client.command()
async def hug(ctx, member: discord.Member = None): # hug a member
    if member == None:
        await ctx.send('Who do you want to hug?')
        return
    if member == ctx.message.author:
        await ctx.send("Sorry, but you can't hug yourself.")
        return
    if member == member.id:
        member = member
    await ctx.send(f"{member.mention}, {ctx.message.author.name} just gave you a big big hug!")



@client.command()
async def fight(ctx, member: discord.Member = None): # fight a member
    if member == None:
        await ctx.send('Who to you want to attack?')
        return
    if member == ctx.message.author:
        await ctx.send("Sorry, but you can't fight yourself.")
        return
    if member == member.id:
        member = member
    ans = [f"{ctx.message.author.name} is fighting {member.mention}, but hurt themselves in confusion!",
            f"{ctx.message.author.name} is fighting {member.mention}, but they stumbled over their shoelaces!",
            f"{ctx.message.author.name} is fighting {member.mention}, but they tripped over a rock and fell in the ocean!"]
    await ctx.send(random.choice(ans))



@client.group()
async def modmail(ctx):
    if ctx.invoked_subcommand is None:
       return


@modmail.command()
async def send(ctx, *, text = None):
    guild = ctx.message.guild
    f = open(f"{guild.id}-modmail-checking.txt", "r")
    global check
    check = f.read()
    if check == 'false':
        e2 = discord.Embed(color=0xfd9fb9, description="Sorry, but the Modmail system is disabled on this server!")
        e2.set_author(name='Error: Modmail system diabled', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    if check == 'true':
        if not os.path.exists(f"{guild.id}-modmail-users.txt"):
            e2 = discord.Embed(color=0xfd9fb9, description="Please set a modmail channel for the users!")
            e2.set_author(name='Error: No user channel', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
            await ctx.send(embed=e2)
            return
        if not os.path.exists(f"{guild.id}-modmail-mods.txt"):
            e3 = discord.Embed(color=0xfd9fb9, description="Please set a modmail channel for the moderators/admins!")
            e3.set_author(name='Error: No mod channel', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
            await ctx.send(embed=e3)
            return
        if os.path.exists(f"{guild.id}-modmail-users.txt") & os.path.exists(f"{guild.id}-modmail-mods.txt"):
            f1 = open(f"{guild.id}-modmail-users.txt", "r")
            user_channel_id = f1.read()
            global user_channel
            user_channel = await client.fetch_channel(user_channel_id)
            # --------------------------------------------------------
            f2 = open(f"{guild.id}-modmail-mods.txt", "r")
            mod_channel_id = f2.read()
            global mod_channel
            mod_channel = await client.fetch_channel(mod_channel_id)
            # --------------------------------------------------------
            if text == None:
                e3 = discord.Embed(color=0xfd9fb9, description='Please enter a valid text!')
                e3.set_author(name='Error: Invalid text', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
                await ctx.send(embed=e3)
                return
            if ctx.message.channel != user_channel:
                e3 = discord.Embed(color=0xfd9fb9, description=f"Please use the correct channel: {user_channel.mention}!")
                e3.set_author(name='Error: Wrong channel', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
                await ctx.send(embed=e3)
                return
            else:
                await mod_channel.send(f"─────────────────── \nNew message by **{ctx.message.author}**: \n \n`{text}` \n \nUser ID: **{ctx.message.author.id}**")
                e10 = discord.Embed(color=0xfd9fb9, description=f'Hey **{ctx.message.author.name}**, we received your message & will respond as fast as possible.')
                await ctx.message.author.send(embed=e10)
                await user_channel.purge(limit=5)


@modmail.command()
@commands.has_permissions(administrator=True)
async def enable(ctx):
    guild = ctx.message.guild
    f = open(f"{guild.id}-modmail-checking.txt", "w")
    f.write('true')
    f.close()
    e9 = discord.Embed(color=0xfd9fb9, description='Succesfully enabled the Modmail system. Please set the user channel with **+modmail userchannel #channel** & the mod channel with **+modmail modchannel #channel**.')
    e9.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
    await ctx.send(embed=e9)


@modmail.command()
@commands.has_permissions(administrator=True)
async def disable(ctx):
    guild = ctx.message.guild
    f = open(f"{guild.id}-modmail-checking.txt", "w")
    f.write('false')
    f.close()
    e9 = discord.Embed(color=0xfd9fb9, description='Succesfully disabled the Modmail system. You can enable the system again by typing **+modmail enable**.')
    e9.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
    await ctx.send(embed=e9)


@modmail.command()
@commands.has_permissions(administrator=True)
async def modchannel(ctx, channel: discord.TextChannel = None):
    guild = ctx.message.guild
    if channel == None:
        e2 = discord.Embed(color=0xfd9fb9, description="Please mention a valid channel or enter a valid channel id!")
        e2.set_author(name='Error: Invalid channel', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    f2 = open(f"{guild.id}-modmail-checking.txt", "r")
    global check
    check = f2.read()
    if check == 'false':
        e2 = discord.Embed(color=0xfd9fb9, description="Sorry, but the Modmail system is disabled on this server!")
        e2.set_author(name='Error: Modmail system diabled', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    if check == 'true':
        if not os.path.exists(f"{guild.id}-modmail-mods.txt"):
            with open(f"{guild.id}-modmail-mods.txt", "w") as f10:
                f10.write(f"{channel.id}")
                f10.close()
                e9 = discord.Embed(color=0xfd9fb9, description=f'Successfully set the modmail mod channel to {channel.mention}!')
                e9.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
                await ctx.send(embed=e9)
                return
        if os.path.exists(f"{guild.id}-modmail-mods.txt"):
            f = open(f"{guild.id}-modmail-mods.txt", "w")
            f.write(f"{channel.id}")
            f.close()
            e99 = discord.Embed(color=0xfd9fb9, description=f'Successfully set the modmail mod channel to {channel.mention}!')
            e99.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
            await ctx.send(embed=e99)



@modmail.command()
@commands.has_permissions(ban_members=True)
async def respond(ctx, member: discord.Member = None, *, text = None):
    guild = ctx.message.guild
    f2 = open(f"{guild.id}-modmail-checking.txt", "r")
    global check
    check = f2.read()
    if check == 'false':
        e2 = discord.Embed(color=0xfd9fb9, description="Sorry, but the Modmail system is disabled on this server!")
        e2.set_author(name='Error: Modmail system diabled', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    if check == 'true':
        if member == None:
            e22 = discord.Embed(color=0xfd9fb9, description="Please mention a valid member or enter a valid member id!")
            e22.set_author(name='Error: Invalid member', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
            await ctx.send(embed=e22)
            return
        if text == None:
            e3 = discord.Embed(color=0xfd9fb9, description='Please enter a valid text!')
            e3.set_author(name='Error: Invalid text', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
            await ctx.send(embed=e3)
            return
        if member == member.id:
            member = member
        e33 = discord.Embed(color=0xfd9fb9, description=f"Answer to your message from the **{guild.name}** server. \n \n**{ctx.message.author}**: {text}")
        await member.send(embed=e33)
        e99 = discord.Embed(color=0xfd9fb9, description=f'Successfully sent the message to {member.mention}!')
        e99.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
        await ctx.send(embed=e99)



@client.command()
@commands.has_permissions(ban_members=True)
async def softban(ctx, member: discord.Member = None, *, reason = None):
    guild = ctx.message.guild
    if member == None:
        e2 = discord.Embed(color=0xfd9fb9, description='Please mention a valid member or enter a valid member id!')
        e2.set_author(name='Error: Invalid member', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    if member == ctx.message.author:
        e7 = discord.Embed(color=0xfd9fb9, description="Sorry, but you can't ban yourself!")
        e7.set_author(name='Error: Author', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e7)
        return
    if member == member.id:
        member = member
    if reason == None:
        reason = 'No reason provided'
    await guild.ban(user=member, reason=reason, delete_message_days=7)
    await guild.unban(user=member, reason='Softban')
    e4 = discord.Embed(color=0xfd9fb9, description=f'{ctx.message.author.mention} successfully softbanned {member.mention} for **{reason}**!')
    e4.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
    await ctx.send(embed=e4)
    e = discord.Embed(color=0xfd9fb9, description=f"**User:** {member} (ID: **{member.id}**) \n**Moderator:** {ctx.message.author} (ID: **{ctx.message.author.id}**) \n**Reason:** {reason}")
    e.set_author(name='User softbanned')
    f = open(f"{guild.id}-log.txt", "r")
    channel_id = f.read()
    channel = await client.fetch_channel(channel_id)
    await channel.send(embed=e)



@modmail.command()
@commands.has_permissions(administrator=True)
async def userchannel(ctx, channel: discord.TextChannel = None):
    guild = ctx.message.guild
    if channel == None:
        e2 = discord.Embed(color=0xfd9fb9, description="Please mention a valid channel or enter a valid channel id!")
        e2.set_author(name='Error: Invalid channel', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    f2 = open(f"{guild.id}-modmail-checking.txt", "r")
    global check
    check = f2.read()
    if check == 'false':
        e2 = discord.Embed(color=0xfd9fb9, description="Sorry, but the Modmail system is disabled on this server!")
        e2.set_author(name='Error: Modmail system diabled', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    if check == 'true':
        if not os.path.exists(f"{guild.id}-modmail-users.txt"):
            with open(f"{guild.id}-modmail-users.txt", "w") as f12:
                f12.write(f"{channel.id}")
                f12.close()
                e99 = discord.Embed(color=0xfd9fb9, description=f"Successfully set the modmail user channel to {channel.mention}")
                e99.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
                await ctx.send(embed=e99)
                return
        if os.path.exists(f"{guild.id}-modmail-users.txt"):
            f = open(f"{guild.id}-modmail-users.txt", "w")
            f.write(f"{channel.id}")
            f.close()
            e99 = discord.Embed(color=0xfd9fb9, description=f"Successfully set the modmail user channel to {channel.mention}")
            e99.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
            await ctx.send(embed=e99)


@modmail.command()
@commands.has_permissions(administrator=True)
async def status(ctx):
    guild = ctx.message.guild
    f = open(f"{guild.id}-modmail-checking.txt", "r")
    global check
    check = f.read()
    if check == 'false':
        e2 = discord.Embed(color=0xfd9fb9, description="Sorry, but the Modmail system is disabled on this server!")
        e2.set_author(name='Error: Modmail system diabled', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    if check == 'true':
        if not os.path.exists(f"{guild.id}-modmail-users.txt"):
            e2 = discord.Embed(color=0xfd9fb9, description="Please set a modmail channel for the users!")
            e2.set_author(name='Error: No user channel', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
            await ctx.send(embed=e2)
            return
        if not os.path.exists(f"{guild.id}-modmail-mods.txt"):
            e3 = discord.Embed(color=0xfd9fb9, description="Please set a modmail channel for the moderators/admins!")
            e3.set_author(name='Error: No mod channel', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
            await ctx.send(embed=e3)
            return
        if os.path.exists(f"{guild.id}-modmail-users.txt") & os.path.exists(f"{guild.id}-modmail-mods.txt"):
            f1 = open(f"{guild.id}-modmail-users.txt")
            user_channel_id = f1.read()
            global user_channel
            user_channel = await client.fetch_channel(user_channel_id)
            # --------------------------------------------------------
            f2 = open(f"{guild.id}-modmail-mods.txt")
            mod_channel_id = f2.read()
            global mod_channel
            mod_channel = await client.fetch_channel(mod_channel_id)
            # --------------------------------------------------------
            e = discord.Embed(color=0xfd9fb9)
            e.set_author(name=f'Server Modmail status for {guild.name}', icon_url=guild.icon_url)
            e.add_field(name='**Mod channel:**', value=f'{mod_channel.mention}', inline=False)
            e.add_field(name='**User channel:**', value=f'{user_channel.mention}', inline=False)
            e.set_footer(text=f'Invoked by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=e)



@client.command()
async def poll(ctx, *, text = None):
    if text == None:
        e3 = discord.Embed(color=0xfd9fb9, description='Please enter a valid text!')
        e3.set_author(name='Error: Invalid text', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e3)
        return
    embed = discord.Embed(color=0xfd9fb9, description=f"{text}")
    embed.set_author(name=f"Poll by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
    embed.set_footer(text=f'User ID: {ctx.message.author.id}')
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')
    await msg.add_reaction('🤷‍♀️')




@client.command()
@commands.has_permissions(ban_members=True)
async def muterole(ctx, role: discord.Role = None):
    guild = ctx.message.guild
    if muterole == None:
        e3 = discord.Embed(color=0xfd9fb9, description='Please enter a valid role name/id or mention a valid role!')
        e3.set_author(name='Error: Invalid role', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e3)
        return
    if not os.path.exists(f"./MuteRoles/{guild.id}-mute-role.txt"):
        e33 = discord.Embed(color=0xfd9fb9, description='File not found. This is a super rare error. Please contact `@EzZz#0001` about this!')
        e33.set_author(name='Error: 404', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e33)
        return
    if os.path.exists(f"./MuteRoles/{guild.id}-mute-role.txt"):
        f = open(f"./MuteRoles/{guild.id}-mute-role.txt", "w")
        f.write(f"{role.id}")
        f.close()
        e99 = discord.Embed(color=0xfd9fb9, description=f'Successfully set the mute role to {role.mention}!')
        e99.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
        await ctx.send(embed=e99)
        return



@client.command()
@commands.has_permissions(ban_members=True)
async def mute(ctx, member: discord.Member = None, time: int = None, *, reason = None):
    guild = ctx.message.guild
    max_time = 2880
    if member == None:
        e2 = discord.Embed(color=0xfd9fb9, description='Please mention a valid member or enter a valid member id!')
        e2.set_author(name='Error: Invalid member', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    if time == None:
        e2 = discord.Embed(color=0xfd9fb9, description='Please enter a valid time!')
        e2.set_author(name='Error: Invalid time', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e2)
        return
    if time > max_time:
        e22 = discord.Embed(color=0xfd9fb9, description='Sorry, but the max mute time is 2 days (2880 minutes).')
        e22.set_author(name='Error: Max time', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e22)
        return
    if reason == None:
        reason = 'None'
    if not os.path.exists(f"./MuteRoles/{guild.id}-mute-role.txt"):
        e33 = discord.Embed(color=0xfd9fb9, description='File not found. This is a super rare error. Please contact `@EzZz#0001` about this!')
        e33.set_author(name='Error: 404', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e33)
        return
    if os.path.exists(f"./MuteRoles/{guild.id}-mute-role.txt"):
        if os.stat(f"./MuteRoles/{guild.id}-mute-role.txt").st_size == 0:
            e332 = discord.Embed(color=0xfd9fb9, description='Looks like no mute role has been set yet!')
            e332.set_author(name='Error: No mute role', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
            await ctx.send(embed=e332)
            return
        f = open(f"./MuteRoles/{guild.id}-mute-role.txt", "r")
        mute_role_id = f.read()
        mute_role = discord.utils.get(guild.roles, id=int(mute_role_id))
        await member.add_roles(mute_role, reason=reason)
        e4 = discord.Embed(color=0xfd9fb9, description=f'{ctx.message.author.mention} successfully muted {member.mention} for **{time}** minutes because of **{reason}**!')
        e4.set_author(name='Success', icon_url='https://cdn2.iconfinder.com/data/icons/greenline/512/check-512.png')
        await ctx.send(embed=e4)
        if os.path.exists(f"{guild.id}-log.txt"):
            f9 = open(f"{guild.id}-log.txt", "r")
            log_id = f9.read()
            log_channel = await client.fetch_channel(log_id)
            e = discord.Embed(color=0xfd9fb9, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**) \nTime: **{time}** Minutes \nReason: **{reason}**")
            e.set_author(name='User Muted')
            await log_channel.send(embed=e)
        else:
            pass
        await asyncio.sleep(time * 60)
        await member.remove_roles(mute_role, reason=reason)
        if os.path.exists(f"{guild.id}-log.txt"):
            f9 = open(f"{guild.id}-log.txt", "r")
            log_id = f9.read()
            log_channel = await client.fetch_channel(log_id)
            e = discord.Embed(color=0xfd9fb9, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**)")
            e.set_author(name='User Unmuted')
            await log_channel.send(embed=e)
        else:
            pass


@client.command()
async def invite(ctx):
    e = discord.Embed(color=0xfd9fb9, description='Click [here](https://discord.com/oauth2/authorize?client_id=697487580522086431&permissions=8&scope=bot) to invite the bot!')
    await ctx.send(embed=e)






@client.event
async def on_command_error(ctx, error): # error messages
    if isinstance(error, commands.BotMissingPermissions):
        e33 = discord.Embed(color=0xfd9fb9, description="I don't have proper permissions do to this action!")
        e33.set_author(name='Error: Missing bot permissions', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e33)
        return
    if isinstance(error, commands.MissingPermissions):
        e332 = discord.Embed(color=0xfd9fb9, description="Looks like you don't have proper permissions do to this action!")
        e332.set_author(name='Error: Missing user permissions', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e332)
        return
    if isinstance(error, commands.NotOwner):
        e333 = discord.Embed(color=0xfd9fb9, description="This commands can only be used by the bot's owner!")
        e333.set_author(name='Error: Owner only', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e333)
        return
    if isinstance(error, commands.BadArgument):
        e335 = discord.Embed(color=0xfd9fb9, description="Value error: One of the arguments has to be an int, not str!")
        e335.set_author(name='Error: Value error', icon_url='https://www.freeiconspng.com/uploads/error-icon-4.png')
        await ctx.send(embed=e335)
        return



client.run(TOKEN)
