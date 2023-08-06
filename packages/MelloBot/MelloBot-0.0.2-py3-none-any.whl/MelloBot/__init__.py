# -*- coding: utf-8 -*-
 
"""
“Commons Clause” License Condition Copyright Pirxcy/Mello 2019-2020 / 2020-202
 
The Software is provided to you by the Licensor under the
License, as defined below, subject to the following condition.
 
Without limiting other conditions in the License, the grant
of rights under the License will not include, and the License
does not grant to you, the right to Sell the Software.
 
For purposes of the foregoing, “Sell” means practicing any or
all of the rights granted to you under the License to provide
to third parties, for a fee or other consideration (including
without limitation fees for hosting or consulting/ support
services related to the Software), a product or service whose
value derives, entirely or substantially, from the functionality
of the Software. Any license notice or attribution required by
the License must also include this Commons Clause License
Condition notice.
 
Software: MelloBot (https://pypi.org/user/Pirxcy/)
 
License: Apache 2.0
"""
 
__name__ = "MelloBot"
__author__ = "Pirxcy"
__version__ = "0.0.2"
 
from colorama import Fore, Back, Style, init
import fortnitepy
import FortniteAPIAsync
import time
import json
import os
from fortnitepy.ext import commands

intro = Fore.LIGHTMAGENTA_EX + f"""
███╗   ███╗███████╗██╗     ██╗      ██████╗ 
████╗ ████║██╔════╝██║     ██║     ██╔═══██╗
██╔████╔██║█████╗  ██║     ██║     ██║   ██║
██║╚██╔╝██║██╔══╝  ██║     ██║     ██║   ██║
██║ ╚═╝ ██║███████╗███████╗███████╗╚██████╔╝
╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝ 
V0.0.2 {Fore.LIGHTMAGENTA_EX + "Coded"} {Fore.RED + "P"}{Fore.GREEN + "i"}{Fore.YELLOW + "r"}{Fore.BLUE + "x"}{Fore.MAGENTA + "c"}{Fore.RED + "y"} {Fore.LIGHTMAGENTA_EX + "for Mello!"} \nJoin The Discord and Contact @pirxcy or Helpers for Help!\nhttps://discord.gg/25fKfvrqwC Enjoy!
"""
os.system('cls||clear')
print(intro)
print(Fore.BLUE + "Logging In...")

def lenPartyMembers():
    members = client.party.members
    return len(members)

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

def lenFriends():
    friends = client.friends
    return len(friends)


with open('config.json') as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(intro)
        print(Fore.RED + ' [ERROR] ' + Fore.RESET + "There was an error in one of the bot's files! (config.json). If you have problems trying to fix it, join the discord support server for help - https://discord.gg/25fKfvrqwC and Contact @Pirxcy!")
        print(Fore.LIGHTRED_EX + f'\n {e}')
        exit(1)


email = data['email']
password = data['password']
filename = data['auths']

def is_admin():
    async def predicate(ctx):
        return ctx.author.id in info['FullAccess']
    return commands.check(predicate)

def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open(filename, 'w') as fp:
        json.dump(existing, fp)

prefix = data['prefix']
device_auth_details = get_device_auth_details().get(email, {})
bot = commands.Bot(
    command_prefix= data['prefix'],
    auth=fortnitepy.AdvancedAuth(
        email=email,
        password=password,
        prompt_authorization_code=True,
        case_insensitive=True,
        delete_existing_device_auths=True,
        **device_auth_details
    )
)
client = bot

@bot.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)



@client.event
async def event_ready():
    os.system('cls||clear')
    print(intro)
    print(Fore.BLUE + "Success")
    os.system('cls||clear')
    print(intro)
    print(Fore.BLUE + ' [+] ' + Fore.RESET + 'Client ready as ' + Fore.CYAN + f'{client.user.display_name}')

  
@client.event
async def event_friend_request(request):
    if data['friendaccept'].lower() == 'true':
        try:
            await request.accept()
            print(f' [+] Accepted friend request from {request.display_name}' + Fore.LIGHTBLACK_EX + f' ({lenFriends()})')
        except Exception:
            pass
    elif data['friendaccept'].lower() == 'false':
        if request.id in info['FullAccess']:
            try:
                await request.accept()
                print(Fore.GREEN + ' [+] ' + Fore.RESET + 'Accepted friend request from ' + Fore.LIGHTGREEN_EX + f'{request.display_name}' + Fore.LIGHTBLACK_EX + f' ({lenFriends()})')
            except Exception:
                pass
        else:
            print(f' [+] Never accepted friend request from {request.display_name}')

@bot.event
async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
    time.sleep(0)
    await bot.party.send('__Owner Socials__\n| Instagram: xmattz\n| Youtube: Mello Modz\n| Snapchat: xmatthewzx| Tiktok: mellofn\n| Epic:vMattzOn144fps-_ \n| __ |\n\n__Our Discord__\nJoin Our Discord Server To Support Us:\nhttps://discord.gg/pKyxK6jxac')

@client.event
async def event_party_invite(invite):
    if data['joinoninvite'].lower() == 'true':
        try:
            await invite.accept()
            print(Fore.GREEN + ' [+] ' + Fore.RESET + f'Accepted party invite from {invite.sender.display_name}')
        except Exception:
            pass
    elif data['joinoninvite'].lower() == 'false':
        if invite.sender.id in info['FullAccess']:
            await invite.accept()
            print(Fore.GREEN + ' [+] ' + Fore.RESET + 'Accepted party invite from ' + Fore.BLUE + f'{invite.sender.display_name}')
        else:
            print(Fore.GREEN + ' [+] ' + Fore.RESET + f'Never accepted party invite from {invite.sender.display_name}')


@client.command()
@is_admin()
async def promote(ctx, *, message = None):
  await message.author.promote()

@bot.command()
async def skin(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await FortniteAPIAsync.get_cosmetic(
            matchMethod="contains",
            name=content,
            backendType="AthenaCharacter"
        )

        await ctx.send(f'Skin set to {cosmetic.id}.')
        print(f"Set skin to: {cosmetic.id}.")
        await client.party.me.set_outfit(asset=cosmetic.id)

    except FortniteAPIAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a skin with the name: {content}.")
        print(f"Failed to find a skin with the name: {content}.")


@bot.command()
async def emote(ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
    try:
        cosmetic = await FortniteAPIAsync.get_cosmetic(
            matchMethod="contains",
            name=content,
            backendType="AthenaDance"
        )

        await ctx.send(f'Emote set to {cosmetic.id}.')
        print(f"Emote skin to: {cosmetic.id}.")
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset=cosmetic.id)

    except FortniteAPIAsync.exceptions.NotFound:
        await ctx.send(f"Failed to find a emote with the name: {content}.")
        print(f"Failed to find a emote with the name: {content}.")


@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@commands.dm_only()
@client.command()
async def admin(ctx, setting = None, *, user = None):
    if (setting is None) and (user is None):
        await ctx.send(f"Missing one or more arguments. Try: {prefix}admin (add, remove, list) (user)")
    elif (setting is not None) and (user is None):

        user = await client.fetch_profile(ctx.message.author.id)

        if setting.lower() == 'add':
            if user.id in info['FullAccess']:
                await ctx.send("You are already an admin")

            else:
                await ctx.send("Password?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if content == data['AdminPassword']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("Incorrect Password.")

        elif setting.lower() == 'remove':
            if user.id not in info['FullAccess']:
                await ctx.send("You are not an admin.")
            else:
                await ctx.send("Are you sure you want to remove yourself as an admin?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if (content.lower() == 'yes') or (content.lower() == 'y'):
                    info['FullAccess'].remove(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send("You were removed as an admin.")
                        print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                elif (content.lower() == 'no') or (content.lower() == 'n'):
                    await ctx.send("You were kept as admin.")
                else:
                    await ctx.send("Not a correct reponse. Cancelling command.")
                
        elif setting == 'list':
            if user.id in info['FullAccess']:
                admins = []

                for admin in info['FullAccess']:
                    user = await client.fetch_profile(admin)
                    admins.append(user.display_name)

                await ctx.send(f"The bot has {len(admins)} admins:")

                for admin in admins:
                    await ctx.send(admin)

            else:
                await ctx.send("You don't have permission to this command.")

        else:
            await ctx.send(f"That is not a valid setting. Try: {prefix}admin (add, remove, list) (user)")
            
    elif (setting is not None) and (user is not None):
        user = await client.fetch_profile(user)

        if setting.lower() == 'add':
            if ctx.message.author.id in info['FullAccess']:
                if user.id not in info['FullAccess']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("That user is already an admin.")
            else:
                await ctx.send("You don't have access to add other people as admins. Try just: !admin add")
        elif setting.lower() == 'remove':
            if ctx.message.author.id in info['FullAccess']:
                if user.id in info['FullAccess']:
                    await ctx.send("Password?")
                    response = await client.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if content == data['AdminPassword']:
                        info['FullAccess'].remove(user.id)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"{user.display_name} was removed as an admin.")
                            print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                    else:
                        await ctx.send("Incorrect Password.")
                else:
                    await ctx.send("That person is not an admin.")
            else:
                await ctx.send("You don't have permission to remove players as an admin.")
        else:
            await ctx.send(f"Not a valid setting. Try: {prefix}admin (add, remove) (user)")

bot.run()
#client.run('NjQ5ODQ1MDQwMzYwODQ5NDE5.XeCtWw.3EsaZ1U2PAVintNxdZYOpRumxY0')
