import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
import glob, os, os.path
import sys
import fileinput
import asyncio

client: Bot = commands.Bot(command_prefix='+') # Prefix of the bot
client.remove_command('help') # removes the basic help command
TOKEN = '' # Token


#----------------------------------------
# Start of the code
#----------------------------------------

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='+help'))
    print(f'Logged in as {client.user}')
    print('----------------------------')
    print(f'ID: {client.user.id}')


@client.event
async def on_guild_join(guild): # when the bot joins a guild
    f = open(f"{guild.id}-words.txt", "w")
    f.write(f"nigga\nbitch\nnegga\nfuck you\nson of a bitch\nwhore\nfuck u\nbastard")
    f.close()
    f2 = open(f"{guild.id}-modmail-checking", "w")
    f2.write('false')
    f2.close()
    channel = client.get_channel(697830313879011389)
    await channel.send(f'New guild: **{guild.name}** (ID: **{guild.id}**)')
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        client.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    channel = await guild.create_text_channel(name='welcome-tools', overwrites=overwrites)
    welcome_embed = discord.Embed(color=0x7289DA, title=f'<a:dabhi:705608735225020506> Hey there!')
    welcome_embed.add_field(name=f'**And thanks for inviting me to your server**', value=f"**{guild.name}** is the **{len(client.guilds)}.** server I joined! \nBut first things first: to use the bot like a real pro, you should do some things first. \nTo make this as easy as possible for you, we put the steps separately and well-ordered among themselves.", inline=False)
    welcome_embed.add_field(name='**Setting up a log channel:**', value="You can easily set up a log channel by typing **+setlog #channel** or **+setlog channelID**", inline=False)
    welcome_embed.add_field(name='**Setting up a welcome message & channel:**', value="You can set up a welcome message channel by typing **+setwelcome #channel** or **+setwelcome channelID**. \nIn addition to that, you can also set up a custom welcome message, by typing **#setmsg YourText**", inline=False)
    welcome_embed.add_field(name='**Other useful things:**', value="You see all commands by typing **+help**. \nIf you need help with the bot, you can join the [support server](https://discord.gg/S9BEBux) and we'll help you there. \nYou think the bot is cool & your friends might be interested in it as well? Feel free to invite the bot via [this link](https://discordapp.com/api/oauth2/authorize?client_id=697487580522086431&permissions=8&scope=bot) \nOne last thing: Yes, you can delete this channel if you want to 😉", inline=False)
    welcome_embed.set_footer(text=f'Bot ID: {client.user.id}', icon_url=guild.icon_url)
    await channel.send(embed=welcome_embed)
    open(f"./MuteRoles/{guild.id}-mute-role.txt", "x")


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
                await message.channel.send("Hey, don't use words like that.")
    await client.process_commands(message)


@client.command()
@commands.has_permissions(ban_members=True)
async def add(ctx, *, word = None): # Adds a new word to the filter
    message_content = ctx.message.content.strip().lower()
    with open(f"{ctx.message.guild.id}-words.txt") as f2:
        bad_words = [bad_words.strip().lower() for bad_words in f2.readlines()]
        for bad_words in bad_words:
            if bad_words in message_content:
                await ctx.send('Sorry, but that word is already in the filter.')
                return
    if word == None:
        await ctx.send('Please enter a valid word.')
        return
    f = open(f"{ctx.message.guild.id}-words.txt", "a")
    f.write(f"\n{word}")
    f.close()
    await ctx.send('Succesfully added the word to the filter.')


@client.command()
@commands.has_permissions(ban_members=True)
async def remove(ctx, *, altWord): # removes a word from the filter 
    guild = ctx.message.guild
    for line in fileinput.input(f"{guild.id}-words.txt", inplace=-1):
        sys.stdout.write(line.replace(altWord, '--------------'))



@client.command()
@commands.has_permissions(ban_members=True)
async def showlist(ctx): # shows the filter
    guild = ctx.message.guild
    f = open(f"{guild.id}-words.txt", "r")
    words = f.read()
    embed = discord.Embed(color=0x7289DA, title=f'Filter List for {ctx.message.guild.name}', description=f'{words}')
    embed.set_footer(text="-------------- = deleted words")
    await ctx.send(embed=embed)



@client.group()
async def help(ctx): # The help command
    if ctx.invoked_subcommand is None:
        bot = client.get_user(697487580522086431)
        e = discord.Embed(color=0x7289DA)
        e.set_author(name='Commands List', icon_url=bot.avatar_url)
        e.set_footer(text=f'Invoked by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        e.add_field(name='**<:585765206769139723:701821061263785985> Word Filter**', value='+add `[word]` **|** Adds a word to the filter \n+remove `[word]` **|** Removes a word from the filter \n+showlist **|** Shows a list of the filtered words', inline=False)
        e.add_field(name='**<:dnd:705582091106123786> Warn System**', value='**If the user gets their 3rd warn, they will automatically get banned** \n+warn `[mention or id]` `[reason]` **|** Warns the user \n+warnings `[mention or id]` **|** Shows the warnings of the user \n+clearwarns `[mention or id]` **|** Clears all warnings of the user', inline=False)
        e.add_field(name='**📨 Modmail System**', value='+modmail enable **|** Enables the Modmail system \n+modmail disable **|** Disables the Modmail system \n+modmail send `[text]` **|** Sends a message to the mods \n+modmail modchannel `[ID or mention]` **|** Sets a channel for incoming messages \n+modmail userchannel `[ID or mention]` **|** Sets a channel for the users \n+modmail respond `[ID or mention]` `[text]` **|** Responds to a message \n+modmail status **|** Shows the current Modmail system status', inline=False)
        e.add_field(name='**<:585765895939424258:701821042183635046> User Commands**', value='+poll `[text]` **|** Creates a classic poll \n +av `[ID or mention]` **|** Shows the avatar \n+addrole `[ID or mention]` `[role ID/mention/name]` **|** Adds a specific role \n+removerole `[ID or mention]` `[role ID/mention/name]` **|** Removes a specific role\n +info `[ID or mention]` **|** Shows info about the user \n+nickname `[ID or mention]` `[nickname]` **|** Changes the nickname of the member \n+hug `[mention or id]` **|** Hugs the user \n+fight `[mention or id]` **|** Fights the user', inline=False)
        e.add_field(name='**<:Staff:723200944266936411> Mod Commands**', value='+setlog `[ID or mention]` **|** Sets a log channel \n+softban `[ID or mention]` `[reason]`**|** Softbans a member \n+ban `[ID or mention]` `[reason]` **|** Bans a user \n+kick `[ID or mention]` `[reason]` **|** Kicks the user \n +purge `[amount]` **|** Purges a specific amount of messages \n+muterole `[role ID, mention or name]` **|** Sets a mute role \n+mute `[mention or ID]` `[time in minutes]` `[reason]` **|** Mutes a member for a specific amount of time \n+slowmode `[mention or ID]` `[time in seconds]` **|** Sets the channel slowmode \n+guildinfo **|** Shows info about the guild ' , inline=False)
        e.add_field(name='**<:welcome:706272444864004106> Welcome System**', value='+welcomeinfo **|** Shows a list of usable welcome message args \n+setwelcome `[ID or mention]` **|** Sets a welcome channel \n+setmsg `[text]` **|** Sets a welcome message \n+welcomestatus **|** Shows the current welcome message & channel', inline=False)
        e.add_field(name='**<:697686848545488986:701821086928732161> Bot Commands**', value='+botinfo **|** Shows info about the bot \n+help `[dm]` **|** Shows this help message. Add **dm** to get the command in DMs', inline=False)
        await ctx.message.channel.trigger_typing()
        await ctx.send(embed=e)



@help.command()
async def dm(ctx):
    bot = client.get_user(697487580522086431)
    e = discord.Embed(color=0x7289DA)
    e.set_author(name='Command List', icon_url=bot.avatar_url)
    e.set_footer(text=f'Invoked by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
    e.add_field(name='**<:585765206769139723:701821061263785985> Word Filter**', value='+add `[word]` **|** Adds a word to the filter \n+remove `[word]` **|** Removes a word from the filter \n+showlist **|** Shows a list of the filtered words', inline=False)
    e.add_field(name='**<:dnd:705582091106123786> Warn System**', value='**If the user gets their 3rd warn, they will automatically get banned** \n+warn `[mention or id]` `[reason]` **|** Warns the user \n+warnings `[mention or id]` **|** Shows the warnings of the user \n+clearwarns `[mention or id]` **|** Clears all warnings of the user', inline=False)
    e.add_field(name='**📨 Modmail System**', value='+modmail enable **|** Enables the Modmail system \n+modmail disable **|** Disables the Modmail system \n+modmail send `[text]` **|** Sends a message to the mods \n+modmail modchannel `[ID or mention]` **|** Sets a channel for incoming messages \n+modmail userchannel `[ID or mention]` **|** Sets a channel for the users \n+modmail respond `[ID or mention]` `[text]` **|** Responds to a message \n+modmail status **|** Shows the current Modmail system status', inline=False)
    e.add_field(name='**<:585765895939424258:701821042183635046> User Commands**', value='+poll `[text]` **|** Creates a basic poll \n+av `[ID or mention]` **|** Shows the avatar \n+addrole `[ID or mention]` `[role ID/mention/name]` **|** Adds a specific role \n+removerole `[ID or mention]` `[role ID/mention/name]` **|** Removes a specific role\n +info `[ID or mention]` **|** Shows info about the user \n+nickname `[ID or mention]` `[nickname]` **|** Changes the nickname of the member \n+hug `[mention or id]` **|** Hugs the user \n+fight `[mention or id]` **|** Fights the user', inline=False)
    e.add_field(name='**<:Staff:723200944266936411> Mod Commands**', value='+setlog `[ID or mention]` **|** Sets a log channel \n+softban `[ID or mention]` `[reason]`**|** Softbans a member \n+muterole `[role ID, mention or name]` **|** Sets a mute role \n+mute `[mention or ID]` `[time in minutes]` `[reason]` **|** Mutes a member for a specific amount of time \n+ban `[ID or mention]` `[reason]` **|** Bans a user \n+kick `[ID or mention]` `[reason]` **|** Kicks the user \n +lock `[channel]` `[time in seconds]` **|** Locks a channel \n +purge `[amount]` **|** Purges a specific amount of messages \n+slowmode `[mention or ID]` `[time in seconds]` **|** Sets the channel slowmode \n+guildinfo **|** Shows info about the guild ' , inline=False)
    e.add_field(name='**<:welcome:706272444864004106> Welcome System**', value='+welcomeinfo **|** Shows a list of usable welcome message args \n+setwelcome `[ID or mention]` **|** Sets a welcome channel \n+setmsg `[text]` **|** Sets a welcome message \n+welcomestatus **|** Shows the current welcome message & channel', inline=False)
    e.add_field(name='**<:697686848545488986:701821086928732161> Bot Commands**', value='+botinfo **|** Shows info about the bot \n+help `[dm]` **|** Shows this help message. Add **dm** to get the command in DMs', inline=False)
    await ctx.message.channel.trigger_typing()
    e2 = discord.Embed(color=0x7289DA, description='Check your private messages! 📬')
    await ctx.send(embed=e2)
    await ctx.message.author.send(embed=e)




@client.command()
@commands.has_permissions(manage_messages=True)
async def av(ctx, member: discord.Member = None): # shows the avatar
    if member == None:
        member = ctx.message.author
    elif member == member.id:
        member = member
    e = discord.Embed(color=0x7289DA)
    e.set_author(name=f"{member}'s avatar")
    e.set_image(url=member.avatar_url)
    e.set_footer(text=f'Invoked by {ctx.message.author}')
    await ctx.send(embed=e)




@client.command()
@commands.has_permissions(ban_members=True)
async def slowmode(ctx, channel: discord.TextChannel = None, *, time: int = None): # changes the slowmode
    if channel == None:
        await ctx.send('Please mention valid channel or enter a valid channel id.')
        return
    if time == None:
        await ctx.send('Please enter a valid time')
        return
    if channel == channel.id:
        channel = channel
    await channel.edit(slowmode_delay=time)
    await ctx.send(f'Slowmode for channel {channel.mention} has been set to **{time}** seconds')



@client.command()
@commands.has_permissions(manage_messages=True)
async def nickname(ctx, member: discord.Member = None, *, name = None): # changes the nickname 
    if name == None:
        await ctx.send('Please enter a valid name.')
        return
    if member == None:
        await ctx.send('Please mention a valid member or enter a valid id.')
        return
    if member == member.id:
        member = member
    await member.edit(nick=name)
    await ctx.send(f"Succesfully changed the username of **{member}** to **{name}**.")


@client.command()
async def info(ctx, member: discord.Member = None):
    guild = client.get_guild(701041308810084362)
    if ctx.message.guild == guild:
        if member == None:
            member = ctx.message.author
        elif member == member.id:
            member = member
        e = discord.Embed(color=0x7289DA, title=f'User Info for {member}', description=f"**Name:** {member} \n**Nickname:** {member.nick} \n**ID:** {member.id} \n \n**Joined Discord:** {member.created_at.strftime('%a, %m/%e/%Y, %H:%M')} \n**Joined server:** {member.joined_at.strftime('%a, %m/%e/%Y, %H:%M')} \n**Highest role:** {member.top_role.mention}")
        e.set_footer(text=f'Invoked by {ctx.message.author}')
        e.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=e)
        return
    else:
        if not ctx.message.author.guild_permissions.manage_messages:
            await ctx.send("Sorry, but you don't have permissions to do this action.")
            return
        else:
            if member == None:
                member = ctx.message.author
            elif member == member.id:
                member = member
            e = discord.Embed(color=0x7289DA, title=f'User Info for {member}', description=f"**Name:** {member} \n**Nickname:** {member.nick} \n**ID:** {member.id} \n \n**Joined Discord:** {member.created_at.strftime('%a, %m/%e/%Y, %H:%M')} \n**Joined server:** {member.joined_at.strftime('%a, %m/%e/%Y, %H:%M')} \n**Highest role:** {member.top_role.mention}")
            e.set_footer(text=f'Invoked by {ctx.message.author}')
            e.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=e)



@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=5):
    if amount >= 50:
        await ctx.send('Sorry, but I can only delete a maximum of 49 messages at once')
        return
    await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason = None):
    if member == ctx.message.author:
        await ctx.send("Sorry, but you can't ban yourself.")
        return
    if member == None:
        await ctx.send('Please mention a valid user or enter a valid id.')
        return
    if member == member.id:
        member = member
    if reason == None:
        reason = 'No reason provided'
    e = discord.Embed(color=0x7289DA, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**) \nReason: **{reason}**")
    e.set_author(name='User kicked')
    await member.kick(reason=reason)
    await ctx.send(f'Succesfully kicked user {member}')
    guild = ctx.message.guild
    f = open(f"{guild.id}-log.txt", "r")
    channel_id = f.read()
    log_channel = await client.fetch_channel(channel_id)
    await log_channel.send(embed=e)



@client.command()
@commands.has_permissions(ban_members=True)
async def welcomeinfo(ctx):
    e = discord.Embed(color=0x7289DA, description='**{mention}** - Mentions the user \n**{members}** - Shows the current member count \n**{guild}** - Shows the guild name \n**{member}** - Shows the name of the user \n \nYou can add these arguments to your welcome message')
    e.set_author(name='Usable args for the welcome message', icon_url=ctx.message.guild.icon_url)
    await ctx.send(embed=e)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason = None): # ban command
    if member == ctx.message.author:
        await ctx.send("Sorry, but you can't ban yourself.")
        return
    if member == None:
        await ctx.send('Please mention a valid user or enter a valid id.')
        return
    if member == member.id:
        member = member
    if reason == None:
        reason = 'No reason provided'
    await member.ban(reason=reason)
    e = discord.Embed(color=0x7289DA, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**) \nReason: **{reason}**")
    e.set_author(name='User banned')
    await ctx.send(f'Succesfully banned user **{member}** (ID: **{member.id}**) for **{reason}**')
    guild = ctx.message.guild
    f = open(f"{guild.id}-log.txt", "r")
    channel_id = f.read()
    log_channel = await client.fetch_channel(channel_id)
    await log_channel.send(embed=e)






@client.command()
async def botinfo(ctx): # info about teh bot
    bot = client.get_user(697487580522086431)
    e = discord.Embed(color=0x7289DA, description=F'**Name:** {bot} \n**ID:** {bot.id} \n**Prefix:** + \n \n**Servers:** {len(client.guilds)} \n**Members:** {len(set(client.get_all_members()))} \n**Ping:** {round(client.latency * 1000)}ms \n \n**Library:** discord.py \n**GitHub Repo:** [Click here](https://github.com/EzZz1337/Tools)')
    e.set_author(name='Info about Tools')
    e.set_thumbnail(url=bot.avatar_url)
    e.set_footer(text=f'Invoked by {ctx.message.author}')
    await ctx.send(embed=e)


@client.command()
@commands.has_permissions(administrator=True)
async def setlog(ctx, channel: discord.TextChannel = None): # sets a log channel
    if channel == None:
        await ctx.send('Please enter mention a valid channel')
        return
    guild = ctx.message.guild
    f = open(f"{guild.id}-log.txt", "w")
    f.write(f"{channel.id}")
    f.close()
    await ctx.send(f'Log channel has been set to {channel.mention}')


@client.command()
@commands.has_permissions(ban_members=True)
async def removerole(ctx, member: discord.Member = None, *, role: discord.Role = None): # reoves a role
    if member == None:
        await ctx.send('Please mention a valid member or enter a valid member id.')
        return
    if role == None:
        await ctx.send('Please enter a valid role name, mention a valid role or enter a valid role id.')
        return
    if member == member.id:
        member = member
    if role == role.id:
        role = role
    await member.remove_roles(role)
    await ctx.send(f'Successfully removed the role **{role.name}** from user **{member}**')



@client.command()
@commands.has_permissions(ban_members=True)
async def addrole(ctx, member: discord.Member = None, *, role: discord.Role = None): # adds role
    if member == None:
        await ctx.send('Please mention a valid member or enter a valid member id.')
        return
    if role == None:
        await ctx.send('Please enter a valid role name, mention a valid role or enter a valid role id.')
        return
    if member == member.id:
        member = member
    if role == role.id:
        role = role
    await member.add_roles(role)
    await ctx.send(f'Successfully added the role **{role.name}** to user **{member}**')


@client.command()
@commands.has_permissions(ban_members=True)
async def warn(ctx, member: discord.Member = None, *, reason = None): # warns a member
    guild = ctx.message.guild
    if member == None:
        await ctx.send('Please mention a valid user or enter a valid id.')
        return
    if member == ctx.message.author:
        await ctx.send("Sorry, but you can't warn yourself.")
        return
    if member == member.id:
        member = member
    if reason == None:
        reason = 'No reason provided'
    if not os.path.exists(f"{guild.id}-{member.id}-warns.txt"):
        with open(f"{guild.id}-{member.id}-warns.txt", "w") as f10:
            f10.write("1")
            f10.close()
            await ctx.send(f"Succesfully warned user **{member}** (ID: **{member.id}**). Reason: **{reason}**")
            if os.path.exists(f"{guild.id}-log.txt"):
                f9 = open(f"{guild.id}-log.txt", "r")
                log_id = f9.read()
                log_channel = await client.fetch_channel(log_id)
                e = discord.Embed(color=0x7289DA, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**) \nReason: **{reason}**")
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
            await ctx.send(f"Succesfully warned user **{member}** (ID: **{member.id}**). Reason: **{reason}**")
            if os.path.exists(f"{guild.id}-log.txt"):
                f9 = open(f"{guild.id}-log.txt", "r")
                log_id = f9.read()
                log_channel = await client.fetch_channel(log_id)
                e = discord.Embed(color=0x7289DA, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**) \nReason: **{reason}**")
                e.set_author(name='User warned')
                await log_channel.send(embed=e)
            else:
                pass
            return
        if warns == '1':
            f3 = open(f"{guild.id}-{member.id}-warns.txt", "w")
            f3.write('2')
            f3.close()
            await ctx.send(f"Succesfully warned user **{member}** (ID: **{member.id}**). Reason: **{reason}**")
            if os.path.exists(f"{guild.id}-log.txt"):
                f9 = open(f"{guild.id}-log.txt", "r")
                log_id = f9.read()
                log_channel = await client.fetch_channel(log_id)
                e = discord.Embed(color=0x7289DA, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**) \nReason: **{reason}**")
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
            await ctx.send(f"Looks like **{member}** (ID: **{member.id}**) has been warned too often, and now they are banned.")
            if os.path.exists(f"{guild.id}-log.txt"):
                f9 = open(f"{guild.id}-log.txt", "r")
                log_id = f9.read()
                log_channel = await client.fetch_channel(log_id)
                e = discord.Embed(color=0x7289DA, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**) \nReason: **{reason}**")
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
        await ctx.send('Please mention a valid user or enter a valid id.')
        return
    if member == member.id:
        member = member
    if os.path.exists(f"{guild.id}-{member.id}-warns.txt"):
        f = open(f"{guild.id}-{member.id}-warns.txt", "w")
        f.write('0')
        await ctx.send(f"Successfully cleared warns for user **{member}**")
        if os.path.exists(f"{guild.id}-log.txt"):
                f9 = open(f"{guild.id}-log.txt", "r")
                log_id = f9.read()
                log_channel = await client.fetch_channel(log_id)
                e = discord.Embed(color=0x7289DA, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**)")
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
        await ctx.send('Please mention a valid user or enter a valid id.')
        return
    if member == member.id:
        member = member
    if os.path.exists(f"{guild.id}-{member.id}-warns.txt"):
        f = open(f"{guild.id}-{member.id}-warns.txt", "r")
        warns = f.read()
        await ctx.send(f'The user **{member}** currently has **{warns}** warning(s).')
    else:
        await ctx.send('Looks like something went wrong...')



@client.command()
@commands.has_permissions(administrator=True)
async def setmsg(ctx, *, text = None): # sets a welcome message
    g = ctx.message.guild
    if text == None:
        await ctx.send('Please enter a text.')
        return
    f = open(f"{g.id}-welcome-msg.txt", "w")
    f.write(text)
    f.close()
    await ctx.send('Successfully set the welcome message')


@client.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, channel: discord.TextChannel = None): # sets a welcome message channel
    g = ctx.message.guild
    if channel == None:
        await ctx.send('Please mention a valid channel or enter a valid channel id.')
        return
    if channel == channel.id:
        channel = channel
    c_id = channel.id
    f = open(f"{g.id}-welcome-channel.txt", "w")
    f.write(f"{c_id}")
    f.close()
    await ctx.send(f'Welcome channel has been set to {channel.mention}')


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
        e = discord.Embed(color=0x7289DA)
        e.set_author(name=f'Server welcoming status for {g.name}', icon_url=g.icon_url)
        e.add_field(name='**Welcome message channel:**', value=f'{welcome_channel.mention}', inline=False)
        e.add_field(name='**Welcome message:**', value=f'{welcome_msg}', inline=False)
        e.set_footer(text=f'Invoked by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=e)
    else:
        await ctx.send("Sorry, but either you don't have set a welcome message or a welcome channel. Please set both to see the server welcoming status.")



@client.command()
@commands.has_permissions(ban_members=True)
async def guildinfo(ctx): # shows info aout the guild
    g = ctx.guild
    e = discord.Embed(color=0x7289DA, title=f'__Guild info for {g.name}__', description=f'Name: **{g.name}** \nID: **{g.id}** \nOwner: {g.owner.mention} \nOwner ID: **{g.owner_id}** \n \nRoles: **{len(g.roles)}** \nEmojis: **{len(g.emojis)}** \n \nCategories: **{len(g.categories)}** \nVoice channels: **{len(g.voice_channels)}** \nText channels: **{len(g.text_channels)}** \n \nMax members: **{g.max_members}** \nMembers: **{len(g.members)}**')
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
        user = member.name
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
    user = member.name
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
        await ctx.send('Please enter a modmail command.')


@modmail.command()
async def send(ctx, *, text = None):
    guild = ctx.message.guild
    f = open(f"{guild.id}-modmail-checking.txt", "r")
    global check
    check = f.read()
    if check == 'false':
        await ctx.send('Sorry, but the Modmail system is disabled on this server.')
        return
    if check == 'true':
        if not os.path.exists(f"{guild.id}-modmail-users.txt"):
            await ctx.send('Please set a modmail channel for the users')
            return
        if not os.path.exists(f"{guild.id}-modmail-mods.txt"):
            await ctx.send('Please set a modmail channel for the mods')
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
            if ctx.message.channel != user_channel:
                await ctx.send(f"Please use the correct modmail channel: {user_channel.mention}")
                return
            else:
                await mod_channel.send(f"─────────────────── \nNew message by **{ctx.message.author}**: \n \n`{text}` \n \nUser ID: **{ctx.message.author.id}**")
                await ctx.message.author.send(f'Hey **{ctx.message.author.name}**, we received your message & will respond as fast as possible.')
                await user_channel.purge(limit=5)


@modmail.command()
@commands.has_permissions(administrator=True)
async def enable(ctx):
    guild = ctx.message.guild
    f = open(f"{guild.id}-modmail-checking.txt", "w")
    f.write('true')
    f.close()
    await ctx.send('Succesfully enabled the Modmail system. Please set the user channel with **+modmail userchannel #channel** & the mod channel with **+modmail modchannel #channel**.')


@modmail.command()
@commands.has_permissions(administrator=True)
async def disable(ctx):
    guild = ctx.message.guild
    f = open(f"{guild.id}-modmail-checking.txt", "w")
    f.write('false')
    f.close()
    await ctx.send('Succesfully disabled the Modmail system. You can enable the system again by typing **+modmail enable**.')


@modmail.command()
@commands.has_permissions(administrator=True)
async def modchannel(ctx, channel: discord.TextChannel = None):
    guild = ctx.message.guild
    if channel == None:
        await ctx.send('Please mention a valid channel or enter a valid channel id.')
        return
    f2 = open(f"{guild.id}-modmail-checking.txt", "r")
    global check
    check = f2.read()
    if check == 'false':
        await ctx.send('Sorry, but the Modmail system is disabled on this server.')
        return
    if check == 'true':
        if not os.path.exists(f"{guild.id}-modmail-mods.txt"):
            with open(f"{guild.id}-modmail-mods.txt", "w") as f10:
                f10.write(f"{channel.id}")
                f10.close()
                await ctx.send(f"Successfully set the modmail mod channel to {channel.mention}")
                return
        if os.path.exists(f"{guild.id}-modmail-mods.txt"):
            f = open(f"{guild.id}-modmail-mods.txt", "w")
            f.write(f"{channel.id}")
            f.close()
            await ctx.send(f"Successfully set the modmail mod channel to {channel.mention}")



@modmail.command()
@commands.has_permissions(ban_members=True)
async def respond(ctx, member: discord.Member = None, *, text = None):
    guild = ctx.message.guild
    f2 = open(f"{guild.id}-modmail-checking.txt", "r")
    global check
    check = f2.read()
    if check == 'false':
        await ctx.send('Sorry, but the Modmail system is disabled on this server.')
        return
    if check == 'true':
        if member == None:
            await ctx.send('Please enter mention a valid member or enter a valid id.')
            return
        if text == None:
            await ctx.send('Please enter a valid text.')
            return
        if member == member.id:
            member = member
        await member.send(f"Answer to your message from the **{guild.name}** server. \n \n**{ctx.message.author}**: {text}")
        await ctx.send('Responded!')



@client.command()
@commands.has_permissions(ban_members=True)
async def softban(ctx, member: discord.Member = None, *, reason = None):
    guild = ctx.message.guild
    if member == None:
        await ctx.send('Please mention a valid user or enter a valid user id.')
        return
    if member == ctx.message.author:
        await ctx.send("Sorry, but you can't ban yourself.")
        return
    if member == member.id:
        member = member
    if reason == None:
        reason = 'No reason provided'
    await guild.ban(user=member, reason=reason, delete_message_days=7)
    await guild.unban(user=member, reason='Softban')
    await ctx.send(f'Succesfully softbanned user `{member}`')
    e = discord.Embed(color=0x7289DA, description=f"**User:** {member} (ID: **{member.id}**) \n**Moderator:** {ctx.message.author} (ID: **{ctx.message.author.id}**) \n**Reason:** {reason}")
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
        await ctx.send('Please mention a valid channel or enter a valid channel id.')
        return
    f2 = open(f"{guild.id}-modmail-checking.txt", "r")
    global check
    check = f2.read()
    if check == 'false':
        await ctx.send('Sorry, but the Modmail system is disabled on this server.')
        return
    if check == 'true':
        if not os.path.exists(f"{guild.id}-modmail-users.txt"):
            with open(f"{guild.id}-modmail-users.txt", "w") as f12:
                f12.write(f"{channel.id}")
                f12.close()
                await ctx.send(f"Successfully set the modmail user channel to {channel.mention}")
                return
        if os.path.exists(f"{guild.id}-modmail-users.txt"):
            f = open(f"{guild.id}-modmail-users.txt", "w")
            f.write(f"{channel.id}")
            f.close()
            await ctx.send(f"Successfully set the modmail user channel to {channel.mention}")


@modmail.command()
@commands.has_permissions(administrator=True)
async def status(ctx):
    guild = ctx.message.guild
    f = open(f"{guild.id}-modmail-checking.txt", "r")
    global check
    check = f.read()
    if check == 'false':
        await ctx.send('Sorry, but the Modmail system is disabled on this server.')
        return
    if check == 'true':
        if not os.path.exists(f"{guild.id}-modmail-users.txt"):
            await ctx.send('Please set a modmail channel for the users')
            return
        if not os.path.exists(f"{guild.id}-modmail-mods.txt"):
            await ctx.send('Please set a modmail channel for the mods')
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
            e = discord.Embed(color=0x7289DA)
            e.set_author(name=f'Server Modmail status for {guild.name}', icon_url=guild.icon_url)
            e.add_field(name='**Mod channel:**', value=f'{mod_channel.mention}', inline=False)
            e.add_field(name='**User channel:**', value=f'{user_channel.mention}', inline=False)
            e.set_footer(text=f'Invoked by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=e)



@client.command()
async def poll(ctx, *, text = None):
    if text == None:
        await ctx.send('Please enter a valid text.')
        return
    embed = discord.Embed(color=0x7289DA, description=f"{text}")
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
        await ctx.send('Please enter a valid role name, role id or mention a valid role.')
        return
    if not os.path.exists(f"./MuteRoles/{guild.id}-mute-role.txt"):
        await ctx.send('Error 404: File not found.')
        return
    if os.path.exists(f"./MuteRoles/{guild.id}-mute-role.txt"):
        f = open(f"./MuteRoles/{guild.id}-mute-role.txt", "w")
        f.write(f"{role.id}")
        f.close()
        await ctx.send(f"Mute role has been set (**{role.name}**)")
        return



@client.command()
@commands.has_permissions(ban_members=True)
async def mute(ctx, member: discord.Member = None, time: int = None, *, reason = None):
    guild = ctx.message.guild
    max_time = 2880
    if member == None:
        await ctx.send('Please enter a valid member id or mention a valid member.')
        return
    if time == None:
        await ctx.send('Please enter a valid time.')
        return
    if time >= max_time:
        await ctx.send('Sorry, but the max mute time is 2 days (2880 minutes).')
        return
    if reason == None:
        reason = 'None'
    if not os.path.exists(f"./MuteRoles/{guild.id}-mute-role.txt"):
        await ctx.send('Error 404: File not found.')
        return
    if os.path.exists(f"./MuteRoles/{guild.id}-mute-role.txt"):
        if os.stat(f"./MuteRoles/{guild.id}-mute-role.txt").st_size == 0:
            await ctx.send('Error: No mute role has been set yet.')
            return
        f = open(f"./MuteRoles/{guild.id}-mute-role.txt", "r")
        mute_role_id = f.read()
        mute_role = discord.utils.get(guild.roles, id=int(mute_role_id))
        await member.add_roles(mute_role, reason=reason)
        if os.path.exists(f"{guild.id}-log.txt"):
            f9 = open(f"{guild.id}-log.txt", "r")
            log_id = f9.read()
            log_channel = await client.fetch_channel(log_id)
            e = discord.Embed(color=0x7289DA, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**) \nTime: **{time}** Minutes \nReason: **{reason}**")
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
            e = discord.Embed(color=0x7289DA, description=f"User: **{member}** (ID: **{member.id}**) \nModerator: **{ctx.message.author}** (ID: **{ctx.message.author.id}**)")
            e.set_author(name='User Unmuted')
            await log_channel.send(embed=e)
        else:
            pass



@client.event
async def on_message_delete(message):
    guild = client.get_guild(708657755577253930)
    log_channel = client.get_channel(708663916233752617)
    if message.guild != guild:
        return
    if message.guild == guild:
        embed = discord.Embed(color=0x7289DA)
        embed.set_author(name='Message deleted')
        embed.add_field(name=f"**User:**", value=f"{message.author} (ID: {message.author.id})", inline=False)
        embed.add_field(name='**Content:**', value=f"{message.content}", inline=False)
        await log_channel.send(embed=embed)
        return


@client.event
async def on_message_edit(before, after):
    guild = client.get_guild(708657755577253930)
    log_channel = client.get_channel(708663916233752617)
    if before.guild != guild:
        return
    if before.guild == guild:
        if before.content != after.content:
            embed = discord.Embed(color=0x7289DA)
            embed.set_author(name='Message edited')
            embed.add_field(name=f"**User:**", value=f"{before.author} (ID: {before.author.id})", inline=False)
            embed.add_field(name='**Old content**', value=f"{before.content}", inline=False)
            embed.add_field(name='**New content**', value=f"{after.content}", inline=False) 
            await log_channel.send(embed=embed)   
            return


@client.command()
@commands.has_permissions(ban_members=True)
async def lockdown(ctx):
    guild = client.get_guild(712832986642645004)
    if ctx.message.guild != guild:
        return
    if ctx.message.guild == guild:
        c1 = client.get_channel(712833603687415859)
        c2 = client.get_channel(712841539805773827)
        c3 = client.get_channel(712839233726840874)
        c4 = client.get_channel(712839248172285952)
        c5 = client.get_channel(712839274059268158)
        log = client.get_channel(712838409202303008)
        await c1.edit(name='🔒-allgemeiner-chat')
        await c2.edit(name='🔒-essen')
        await c3.edit(name='🔒-musik')
        await c4.edit(name='🔒-filme')
        await c5.edit(name='🔒-feedback')
        await c1.set_permissions(guild.default_role, send_messages=False, send_tts_messages=False, attach_files=False, add_reactions=False)
        await c2.set_permissions(guild.default_role, send_messages=False, send_tts_messages=False, attach_files=False, add_reactions=False)
        await c3.set_permissions(guild.default_role, send_messages=False, send_tts_messages=False, attach_files=False, add_reactions=False)
        await c4.set_permissions(guild.default_role, send_messages=False, send_tts_messages=False, attach_files=False, add_reactions=False)
        await c5.set_permissions(guild.default_role, send_messages=False, send_tts_messages=False, attach_files=False, add_reactions=False)
        embed = discord.Embed(color=0xF83207, description=f"🔒 Server gelocked von **{ctx.message.author}**! 🔒")
        await c1.send(embed=embed)
        await c2.send(embed=embed)
        await c3.send(embed=embed)
        await c4.send(embed=embed)
        await c5.send(embed=embed)
        await log.send(embed=embed)




@client.command()
@commands.has_permissions(ban_members=True)
async def endlock(ctx):
    guild = client.get_guild(712832986642645004)
    if ctx.message.guild != guild:
        return
    else:
        c1 = client.get_channel(712833603687415859)
        c2 = client.get_channel(712841539805773827)
        c3 = client.get_channel(712839233726840874)
        c4 = client.get_channel(712839248172285952)
        c5 = client.get_channel(712839274059268158)
        log = client.get_channel(712838409202303008)
        await c1.edit(name='allgemeiner-chat')
        await c2.edit(name='essen')
        await c3.edit(name='musik')
        await c4.edit(name='filme')
        await c5.edit(name='feedback')
        await c1.set_permissions(guild.default_role, send_messages=True, send_tts_messages=False, attach_files=True, add_reactions=True)
        await c2.set_permissions(guild.default_role, send_messages=True, send_tts_messages=False, attach_files=True, add_reactions=True)
        await c3.set_permissions(guild.default_role, send_messages=True, send_tts_messages=False, attach_files=True, add_reactions=True)
        await c4.set_permissions(guild.default_role, send_messages=True, send_tts_messages=False, attach_files=True, add_reactions=True)
        await c5.set_permissions(guild.default_role, send_messages=True, send_tts_messages=False, attach_files=True, add_reactions=True)
        embed = discord.Embed(color=0x44F807, description=f"Server unlocked von **{ctx.message.author}**!")
        await c1.send(embed=embed)
        await c2.send(embed=embed)
        await c3.send(embed=embed)
        await c4.send(embed=embed)
        await c5.send(embed=embed)
        await log.send(embed=embed)






@client.event
async def on_command_error(ctx, error): # error messages
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, but I couldn't find that command. Maybe you made a little typo.")
        return
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Sorry, but I don't have permissions to do this action.")
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Sorry, but you don't have the permissions to do this action.")
        return
    if isinstance(error, commands.NotOwner):
        await ctx.send('This command can only be used by the bot owner.')
        return





client.run(TOKEN)
