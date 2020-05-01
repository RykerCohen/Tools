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
TOKEN = ''


#----------------------------------------
# Start of the code
#----------------------------------------

@client.event
async def on_ready():
    await  client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='+help'))
    print(f'Logged in as {client.user}')
    print('----------------------------')
    print(f'ID: {client.user.id}')


@client.event
async def on_guild_join(guild): # when the bot joins a guild
    f = open(f"{guild.id}-words.txt", "w")
    f.write(f"nigga\nbitch\nnegga\nfuck you\nson of a bitch\nwhore\nfuck u\nbastard")
    f.close()
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


@client.event
async def on_guild_remove(guild): # when the bot gets removed from a guild 
    channel = client.get_channel(697830245725896705)
    await channel.send(f'Removed from guild: **{guild.name}** (ID: **{guild.id}**)')


@client.event
async def on_message(message): # Word filter event  	                                                                                                                                 
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



@client.command()
async def help(ctx): # The help command
    bot = client.get_user(697487580522086431)
    e = discord.Embed(color=0x7289DA)
    e.set_author(name='Help center for the Tools bot', icon_url=bot.avatar_url)
    e.set_footer(text=f'Invoked by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
    e.add_field(name='**<:Filter:697601802455220277> Word Filter**', value='+add `[word]` **|** Adds a word to the filter \n+remove `[word]` **|** Removes a word from the filter \n+showlist **|** Shows a list of the filtered words', inline=False)
    e.add_field(name='**<:dnd:705582091106123786> Warn System**', value='**If the user gets their 3rd warn, they will automatically get banned** \n+warn `[mention or id]` `[reason]` **|** Warns the user \n+warnings `[mention or id]` **|** Shows the warnings of the user \n+clearwarns `[mention or id]` **|** Clears all warnings of the user', inline=False)
    e.add_field(name='**<:hse:697604738631467008> User Commands**', value='+av `[ID or mention]` **|** Shows the avatar \n+addrole `[ID or mention]` `[role ID/mention/name]` **|** Adds a specific role \n+removerole `[ID or mention]` `[role ID/mention/name]` **|** Removes a specific role\n +info `[ID or mention]` **|** Shows info about the user \n+nickname `[ID or mention]` `[nickname]` **|** Changes the nickname of the member', inline=False)
    e.add_field(name='**<:Mod:697605229671350292> Mod Commands**', value='+setlog `[ID or mention]` **|** Sets a log channel \n+setwelcome `[ID or mention]` **|** Sets a welcome channel \n+setmsg `[text]` **|** Sets a welcome message \n+welcomestatus **|** Shows the current welcome message & channel \n+ban `[ID or mention]` `[reason]` **|** Bans a user \n+kick `[ID or mention]` `[reason]` **|** Kicks the user \n +lock `[channel]` `[time in seconds]` **|** Locks a channel \n +purge `[amount]` **|** Purges a specific amount of messages \n+slowmode `[mention or ID]` `[time in seconds]` **|** Sets the channel slowmode \n+guildinfo **|** Shows info about the guild ' , inline=False)
    e.add_field(name='**<:Tools:697605550623555635> Bot Commands**', value='+credits **|** Shows socials of the developers \n+botinfo **|** Shows info about the bot \n+support **|** Shows invite link to the support server \n+help **|** Shows this help message', inline=False)
    await ctx.send(embed=e)





@client.command()
@commands.has_permissions(manage_messages=True)
async def av(ctx, member: discord.Member = None): # shows the avatar
    if member == None:
        member = ctx.message.author
    elif member == member.id:
        member = member
    e = discord.Embed(color=0x7289DA)
    e.set_author(name=f"{member}'s avatar (ID: {member.id})")
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
@commands.has_permissions(manage_messages=True)
async def info(ctx, member: discord.Member = None): # shows info about the user
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
    await ctx.send(f'Succesfully banned user {member}')
    guild = ctx.message.guild
    f = open(f"{guild.id}-log.txt", "r")
    channel_id = f.read()
    log_channel = await client.fetch_channel(channel_id)
    await log_channel.send(embed=e)


@client.command()
@commands.has_permissions(ban_members=True)
async def lock(ctx, channel: discord.TextChannel = None, time: int = None): # locks a channel
    if time == None:
        await ctx.send('Please enter a valid time.')
        return
    if channel == None:
        channel = ctx.message.channel
    await channel.set_permissions(ctx.message.guild.default_role, send_messages=False)
    await channel.send(f'Channel is now locked for {time} seconds.')
    await asyncio.sleep(time)
    await channel.set_permissions(ctx.message.guild.default_role, send_messages=True)
    await channel.send('Channel is now unlocked again.')


@client.command()
async def credits(ctx): # credits of the developer
    bot = client.get_user(697487580522086431)
    e = discord.Embed(color=0x7289DA)
    e.set_author(name='Developer of Tools', icon_url=bot.avatar_url)
    e.add_field(name='**<:Verified:697810401496137840> Contact info**', value='<:discord:697812138772660274> Discord: `EzZz#001` \n<:logotwitter:697811990084714568>  Twitter: [@EzZz1337](https://twitter.com/ezzz1337) \n<:GitHub:705804702201413694> GitHub: [EzZz1337](https://github.com/ezzz1337) \n<:Website:697812224193986630> Website: [Click here](https://ezzz0099.ezzz1337.repl.co)', inline=False)
    e.set_footer(text='Contact me, if you need help')
    await ctx.send(embed=e)


@client.command()
async def botinfo(ctx): # info about teh bot
    bot = client.get_user(697487580522086431)
    e = discord.Embed(color=0x7289DA, description=F'**Name:** {bot} \n**ID:** {bot.id} \n**Prefix:** + \n \n**Servers:** {len(client.guilds)} \n**Members:** {len(set(client.get_all_members()))} \n**Ping:** {round(client.latency * 1000)}ms \n \n**Library:** discord.py \n**Developer:** EzZz#0001 \n**GitHub Repo:** [Click here](https://github.com/EzZz1337/Tools) \n**Bot invite:** [Click here](https://discordapp.com/api/oauth2/authorize?client_id=697487580522086431&permissions=8&scope=bot) \n**Support server:** [Join](https://discord.gg/S9BEBux)')
    e.set_author(name='Info about Tools')
    e.set_thumbnail(url=bot.avatar_url)
    e.set_footer(text=f'Invoked by {ctx.message.author}')
    await ctx.send(embed=e)


@client.command()
async def support(ctx): # support server invite
    bot = client.get_user(697487580522086431)
    e = discord.Embed(color=0x7289DA, description='[<:discord:697812138772660274> Click here to join](https://discord.gg/S9BEBux)')
    e.set_author(name='Support server for Tools', icon_url=bot.avatar_url)
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
            await ctx.send(f"Looks like **{member}** (ID: **{member.id}**) has been warned to often, and now they are banned.")
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
    g = member.guild
    f = open(f"{g.id}-welcome-channel.txt", "r")
    welcome_channel_id = f.read()
    welcome_channel = await client.fetch_channel(welcome_channel_id)
    f2 = open(f"{g.id}-welcome-msg.txt", "r")
    welcome_msg = f2.read()
    await welcome_channel.send(f"{welcome_msg}")





@client.event
async def on_command_error(ctx, error): # error messages
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, but I couldn't find that command. Maybe you made a little typo.")
        return
    if isinstance(error, commands.NotOwner):
        await ctx.send('This command can only be used by the bot owner.')
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Sorry, but you don't have the permissions to do this action.")
        return
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Sorry, but I don't have permissions to do this action.")
        return





client.run(TOKEN)
