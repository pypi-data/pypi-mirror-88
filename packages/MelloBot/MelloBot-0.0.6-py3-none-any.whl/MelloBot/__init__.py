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
__version__ = "0.0.6"
 
from colorama import Fore, Back, Style, init
import sanic
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
V0.0.6 {Fore.LIGHTMAGENTA_EX + "Coded"} {Fore.RED + "P"}{Fore.GREEN + "i"}{Fore.YELLOW + "r"}{Fore.BLUE + "x"}{Fore.MAGENTA + "c"}{Fore.RED + "y"} {Fore.LIGHTMAGENTA_EX + "for Mello!"} \nJoin The Discord and Contact @pirxcy or Helpers for Help!\nhttps://discord.gg/25fKfvrqwC Enjoy!
"""
os.system('cls||clear')
print(intro)
print(Fore.BLUE + "Logging In...")

def lenPartyMembers():
    members = bot.party.members
    return len(members)

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

def lenFriends():
    friends = bot.friends
    return len(friends)


with open('config.json') as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        os.system('cls||clear')
        print(intro)
        print(Fore.YELLOW + '[ERROR] ' + Fore.RED + "There was an error in one of the bot's files! (config.json)\n If you have problems trying to fix it, join the discord support server for help - https://discord.gg/25fKfvrqwC and Contact @Pirxcy!")
        print(Fore.LIGHTRED_EX + f'{e}')
        print("Hope Your Bot Gets Fixed Soon!\nBye!")
        exit(1)

with open('info.json') as f:
    try:
        info = json.load(f)
    except json.decoder.JSONDecodeError as e:
        os.system('cls||clear')
        print(intro)
        print(Fore.YELLOW + '[ERROR]' + Fore.RED + "There was an error in one of the bot's files! (info.json)\n If you have problems trying to fix it, join the discord support server for help - https://discord.gg/25fKfvrqwC and Contact @Pirxcy!")
        print(Fore.LIGHTRED_EX + f'\n {e}')
        print("Hope Your Bot Gets Fixed Soon!\nBye!")
        exit(1)

def is_admin():
    async def predicate(ctx):
        return ctx.author.id in info['FullAccess']
    return commands.check(predicate)

email = data['email']
password = data['password']
filename = data['auths']


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

@bot.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)

from sanic import Sanic
from sanic.response import text
app = Sanic(__name__)
@app.route('/')
async def hello_world(request):
    return text('Congrats Your Mello Bot IS Online\nJoin The Discord https://discord.gg/25fKfvrqwC and Contact @pirxcy to make it 24/7!')

@bot.event
async def event_ready():
    await app.create_server(host="0.0.0.0",port=8000, return_asyncio_server=True)

@bot.event
async def event_ready():
    while true:
        os.system('cls||clear')
        print(intro)
        print(Fore.BLUE + "Success")
        os.system('cls||clear')
        print(intro)
        print(Fore.BLUE + '[MelloBot] ' + Fore.RESET + 'bot ready as ' + Fore.CYAN + f'{bot.user.display_name}\n')
        os.system('cls||clear')
        print(intro)
        print(Fore.BLUE + '[MelloBot] ' + Fore.RESET + 'bot ready as ' + Fore.CYAN + f'{bot.user.display_name}\n' + Fore.RESET)

  
@bot.event
async def event_friend_request(request):
    if data['friendaccept'].lower() == 'true':
        try:
            await request.accept()
            print(f'[MelloBot] Accepted friend request from {request.display_name}' + Fore.LIGHTBLACK_EX + f' ({lenFriends()})')
        except Exception:
            pass
    elif data['friendaccept'].lower() == 'false':
        if request.id in info['FullAccess']:
            try:
                await request.accept()
                print(Fore.GREEN + ' [MelloBot] ' + Fore.RESET + 'Accepted friend request from ' + Fore.LIGHTGREEN_EX + f'{request.display_name}' + Fore.LIGHTBLACK_EX + f' ({lenFriends()})')
            except Exception:
                pass
        else:
            print(f' [MelloBot] Never accepted friend request from {request.display_name}')

@bot.event
async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
    time.sleep(0)
    await bot.party.send('__Owner Socials__\n| Instagram: xmattz\n| Youtube: Mello Modz\n| Snapchat: xmatthewzx| Tiktok: mellofn\n| Epic:vMattzOn144fps-_ \n| __ |\n\n__Our Discord__\nJoin Our Discord Server To Support Us:\nhttps://discord.gg/pKyxK6jxac')

@bot.event
async def event_party_invite(invite):
    if data['joinoninvite'].lower() == 'true':
        try:
            await invite.accept()
            print(Fore.GREEN + ' [MelloBot] ' + Fore.RESET + f'Accepted party invite from {invite.sender.display_name}')
        except Exception:
            pass
    elif data['joinoninvite'].lower() == 'false':
        if invite.sender.id in info['FullAccess']:
            await invite.accept()
            print(Fore.GREEN + ' [MelloBot] ' + Fore.RESET + 'Accepted party invite from ' + Fore.BLUE + f'{invite.sender.display_name}')
        else:
            print(Fore.GREEN + ' [MelloBot] ' + Fore.RESET + f'Never accepted party invite from {invite.sender.display_name}')


@bot.command()
@is_admin()
async def promote(ctx, *, message = None):
  await message.author.promote()


@bot.event
async def event_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'That is not a command. Try {prefix}help')
    elif isinstance(error, IndexError):
        pass
    elif isinstance(error, fortnitepy.HTTPException):
        pass
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have access to that command.")
    elif isinstance(error, TimeoutError):
        await ctx.send("You took too long to respond!")
    else:
        print(error)


@commands.dm_only()
@bot.command()
@commands.dm_only()
async def skin(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No skin was given, try: {prefix}skin (skin name)')
    elif content.upper().startswith('CID_'):
        await bot.party.me.set_outfit(asset=content.upper())
        await ctx.send(f'Skin set to: {content}')
    else:
        try:
            cosmetic = await FortniteAPIAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                name=content,
                backendType="AthenaCharacter"
            )
            await bot.party.me.set_outfit(asset=cosmetic.id)
            await ctx.send(f'Skin set to: {cosmetic.name}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {content}')

@commands.dm_only()
@bot.command()
@commands.dm_only()
async def backpack(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No backpack was given, try: {prefix}backpack (backpack name)')
    elif content.lower() == 'none':
        await bot.party.me.clear_backpack()
        await ctx.send('Backpack set to: None')
    elif content.upper().startswith('BID_'):
        await bot.party.me.set_backpack(asset=content.upper())
        await ctx.send(f'Backpack set to: {content}')
    else:
        try:
            cosmetic = await FortniteAPIAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
            await bot.party.me.set_backpack(asset=cosmetic.id)
            await ctx.send(f'Backpack set to: {cosmetic.name}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a backpack named: {content}')

@commands.dm_only()
@bot.command()
async def emote(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No emote was given, try: {prefix}emote (emote name)')
    elif content.lower() == 'floss':
        await bot.party.me.clear_emote()
        await bot.party.me.set_emote(asset='EID_Floss')
        await ctx.send(f'Emote set to: Floss')
    elif content.lower() == 'none':
        await bot.party.me.clear_emote()
        await ctx.send(f'Emote set to: None')
    elif content.upper().startswith('EID_'):
        await bot.party.me.clear_emote()
        await bot.party.me.set_emote(asset=content.upper())
        await ctx.send(f'Emote set to: {content}')
    else:
        try:
            cosmetic = await FortniteAPIAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await bot.party.me.clear_emote()
            await bot.party.me.set_emote(asset=cosmetic.id)
            await ctx.send(f'Emote set to: {cosmetic.name}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'Could not find an emote named: {content}')

@commands.dm_only()
@bot.command()
async def pickaxe(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No pickaxe was given, try: {prefix}pickaxe (pickaxe name)')
    elif content.upper().startswith('Pickaxe_'):
        await bot.party.me.set_pickaxe(asset=content.upper())
        await ctx.send(f'Pickaxe set to: {content}')
    else:
        try:
            cosmetic = await FortniteAPIAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
            await bot.party.me.set_pickaxe(asset=cosmetic.id)
            await ctx.send(f'Pickaxe set to: {cosmetic.name}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pickaxe named: {content}')

@commands.dm_only()
@bot.command()
async def pet(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No pet was given, try: {prefix}pet (pet name)')
    elif content.lower() == 'none':
        await bot.party.me.clear_pet()
        await ctx.send('Pet set to: None')
    else:
        try:
            cosmetic = await FortniteAPIAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPet"
            )
            await bot.party.me.set_pet(asset=cosmetic.id)
            await ctx.send(f'Pet set to: {cosmetic.name}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pet named: {content}')

@commands.dm_only()
@bot.command()
async def emoji(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No emoji was given, try: {prefix}emoji (emoji name)')
    try:
        cosmetic = await FortniteAPIAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaEmoji"
        )
        await bot.party.me.clear_emoji()
        await bot.party.me.set_emoji(asset=cosmetic.id)
        await ctx.send(f'Emoji set to: {cosmetic.name}')
    except FortniteAPIAsync.exceptions.NotFound:
        await ctx.send(f'Could not find an emoji named: {content}')

    
@commands.dm_only()
@bot.command()
async def current(ctx, setting = None):
    if setting is None:
        await ctx.send(f"Missing argument. Try: {prefix}current (skin, backpack, emote, pickaxe, banner)")
    elif setting.lower() == 'banner':
        await ctx.send(f'Banner ID: {bot.party.me.banner[0]}  -  Banner Color ID: {bot.party.me.banner[1]}')
    else:
        try:
            if setting.lower() == 'skin':
                    cosmetic = await FortniteAPIAsync.get_cosmetic_from_id(
                        cosmetic_id=bot.party.me.outfit
                    )

            elif setting.lower() == 'backpack':
                    cosmetic = await FortniteAPIAsync.get_cosmetic_from_id(
                        cosmetic_id=bot.party.me.backpack
                    )

            elif setting.lower() == 'emote':
                    cosmetic = await FortniteAPIAsync.get_cosmetic_from_id(
                        cosmetic_id=bot.party.me.emote
                    )

            elif setting.lower() == 'pickaxe':
                    cosmetic = await FortniteAPIAsync.get_cosmetic_from_id(
                        cosmetic_id=bot.party.me.pickaxe
                    )

            await ctx.send(f"My current {setting} is: {cosmetic.name}")
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f"I couldn't find a {setting} name for that.")


@commands.dm_only()
@bot.command()
async def name(ctx, *, content=None):
    if content is None:
        await ctx.send(f'No ID was given, try: {prefix}name (cosmetic ID)')
    else:
        try:
            cosmetic = await FortniteAPIAsync.get_cosmetic_from_id(
                cosmetic_id=content
            )
            await ctx.send(f'The name for that ID is: {cosmetic.name}')
            print(f' [+] The name for {cosmetic.id} is: {cosmetic.name}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a cosmetic name for ID: {content}')


@commands.dm_only()
@bot.command()
async def cid(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No skin was given, try: {prefix}cid (skin name)')
    else:
        try:
            cosmetic = await FortniteAPIAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaCharacter"
            )
            await ctx.send(f'The CID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The CID for {cosmetic.name} is: {cosmetic.id}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {content}')
        

@commands.dm_only()
@bot.command()
async def bid(ctx, *, content):
    if content is None:
        await ctx.send(f'No backpack was given, try: {prefix}bid (backpack name)')
    else:
        try:
            cosmetic = await FortniteAPIAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
            await ctx.send(f'The BID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The BID for {cosmetic.name} is: {cosmetic.id}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a backpack named: {content}')


@commands.dm_only()
@bot.command()
async def eid(ctx, *, content):
    if content is None:
        await ctx.send(f'No emote was given, try: {prefix}eid (emote name)')
    elif content.lower() == 'floss':
        await ctx.send(f'The EID for Floss is: EID_Floss')
    else:
        try:
            cosmetic = await FortniteAPIAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await ctx.send(f'The EID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The EID for {cosmetic.name} is: {cosmetic.id}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'Could not find an emote named: {content}')


@commands.dm_only()
@bot.command()
async def pid(ctx, *, content):
    if content is None:
        await ctx.send(f'No pickaxe was given, try: {prefix}pid (pickaxe name)')
    else:
        try:
            cosmetic = await FortniteAPIAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
            await ctx.send(f'The PID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [+] The PID for {cosmetic.name} is: {cosmetic.id}')
        except FortniteAPIAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pickaxe named: {content}')


@commands.dm_only()
@bot.command()
async def random(ctx, content = None):

    skins = await FortniteAPIAsync.get_cosmetics(
        lang="en",
        backendType="AthenaCharacter"
    )

    skin = rand.choice(skins)

    backpacks = await FortniteAPIAsync.get_cosmetics(
        lang="en",
        backendType="AthenaBackpack"
    )

    backpack = rand.choice(backpacks)

    emotes = await FortniteAPIAsync.get_cosmetics(
        lang="en",
        backendType="AthenaDance"
    )

    emote = rand.choice(emotes)

    pickaxes = await FortniteAPIAsync.get_cosmetics(
        lang="en",
        backendType="AthenaPickaxe"
    )

    pickaxe = rand.choice(pickaxes)

    
    if content is None:
        me = bot.party.me
        await me.set_outfit(asset=skin.id)
        await me.set_backpack(asset=backpack.id)
        await me.set_pickaxe(asset=pickaxe.id)

        await ctx.send(f'Loadout randomly set to: {skin.name}, {backpack.name}, {pickaxe.name}')
    else:
        if content.lower() == 'skin':
            await bot.party.me.set_outfit(asset=skin.id)
            await ctx.send(f'Skin randomly set to: {skin.name}')

        elif content.lower() == 'backpack':
            await bot.party.me.set_backpack(asset=backpack.id)
            await ctx.send(f'Backpack randomly set to: {backpack.name}')

        elif content.lower() == 'emote':
            await bot.party.me.set_emote(asset=emote.id)
            await ctx.send(f'Emote randomly set to: {emote.name}')

        elif content.lower() == 'pickaxe':
            await bot.party.me.set_pickaxe(asset=pickaxe.id)
            await ctx.send(f'Pickaxe randomly set to: {pickaxe.name}')

        else:
            await ctx.send(f"I don't know that, try: {prefix}random (skin, backpack, emote, pickaxe - og, exclusive, unreleased")


@commands.dm_only()
@bot.command()
async def point(ctx, *, content = None):
    if content is None:
        await bot.party.me.clear_emote()
        await bot.party.me.set_emote(asset='EID_IceKing')
        await ctx.send(f'Pointing with: {bot.party.me.pickaxe}')
    
    else:
        if content.upper().startswith('Pickaxe_'):
            await bot.party.me.set_pickaxe(asset=content.upper())
            await bot.party.me.clear_emote()
            asyncio.sleep(0.25)
            await bot.party.me.set_emote(asset='EID_IceKing')
            await ctx.send(f'Pointing with: {content}')
        else:
            try:
                cosmetic = await FortniteAPIAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=content,
                    backendType="AthenaPickaxe"
                )
                await bot.party.me.set_pickaxe(asset=cosmetic.id)
                await bot.party.me.clear_emote()
                await bot.party.me.set_emote(asset='EID_IceKing')
                await ctx.send(f'Pointing with: {cosmetic.name}')
            except FortniteAPIAsync.exceptions.NotFound:
                await ctx.send(f'Could not find a pickaxe named: {content}')




@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@commands.dm_only()
@bot.command()
async def admin(ctx, setting = None, *, user = None):
    if (setting is None) and (user is None):
        await ctx.send(f"Missing one or more arguments. Try: {prefix}admin (add, remove, list) (user)")
    elif (setting is not None) and (user is None):

        user = await bot.fetch_profile(ctx.message.author.id)

        if setting.lower() == 'add':
            if user.id in info['FullAccess']:
                await ctx.send("You are already an admin")

            else:
                await ctx.send("Password?")
                response = await bot.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if content == data['AdminPassword']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [MelloBot] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("Incorrect Password.")

        elif setting.lower() == 'remove':
            if user.id not in info['FullAccess']:
                await ctx.send("You are not an admin.")
            else:
                await ctx.send("Are you sure you want to remove yourself as an admin?")
                response = await bot.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if (content.lower() == 'yes') or (content.lower() == 'y'):
                    info['FullAccess'].remove(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send("You were removed as an admin.")
                        print(Fore.BLUE + " [MelloBot] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                elif (content.lower() == 'no') or (content.lower() == 'n'):
                    await ctx.send("You were kept as admin.")
                else:
                    await ctx.send("Not a correct reponse. Cancelling command.")
                
        elif setting == 'list':
            if user.id in info['FullAccess']:
                admins = []

                for admin in info['FullAccess']:
                    user = await bot.fetch_profile(admin)
                    admins.append(user.display_name)

                await ctx.send(f"The bot has {len(admins)} admins:")

                for admin in admins:
                    await ctx.send(admin)

            else:
                await ctx.send("You don't have permission to this command.")

        else:
            await ctx.send(f"That is not a valid setting. Try: {prefix}admin (add, remove, list) (user)")
            
    elif (setting is not None) and (user is not None):
        user = await bot.fetch_profile(user)

        if setting.lower() == 'add':
            if ctx.message.author.id in info['FullAccess']:
                if user.id not in info['FullAccess']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [MelloBot] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("That user is already an admin.")
            else:
                await ctx.send("You don't have access to add other people as admins. Try just: !admin add")
        elif setting.lower() == 'remove':
            if ctx.message.author.id in info['FullAccess']:
                if user.id in info['FullAccess']:
                    await ctx.send("Password?")
                    response = await bot.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if content == data['AdminPassword']:
                        info['FullAccess'].remove(user.id)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"{user.display_name} was removed as an admin.")
                            print(Fore.BLUE + " [MelloBot] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                    else:
                        await ctx.send("Incorrect Password.")
                else:
                    await ctx.send("That person is not an admin.")
            else:
                await ctx.send("You don't have permission to remove players as an admin.")
        else:
            await ctx.send(f"Not a valid setting. Try: {prefix}admin (add, remove) (user)")

bot.run()
#bot.run('NjQ5ODQ1MDQwMzYwODQ5NDE5.XeCtWw.3EsaZ1U2PAVintNxdZYOpRumxY0')
