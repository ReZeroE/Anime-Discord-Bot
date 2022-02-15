import sys
import discord
import time
from permission import PermissionIdentifier
from parse_command import ParseCommand
from log_data import LogData

from anilist import AnilistDiscord
anilist = AnilistDiscord()


client = discord.Client()
BOT_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
bot_channel_id = 000000000000000000
bot_server_id = 000000000000000000
bot_name = 'C.C.'
prefix = '>'
up_time = time.time()
        
@client.event # run the code when the bot goes online
async def on_ready():
    bot_testing = client.get_channel(bot_channel_id) 

    from datetime import datetime
    now = datetime.now()
    date_time = now.strftime("%H:%M:%S [%m/%d/%Y]")
    print("C.C. is now online!")
    #await bot_testing.send(f"C.C. is now online!")
    

@client.event
async def on_message(message):
    original_input = message.content
    server_id = message.guild.id
    user_id = message.author.id
    username = message.author.name

    if message.content.startswith(prefix) == False: return  # check bot command prefix
    if message.author == client.user: return                # check message user if bot
    if server_id != bot_server_id: return                   # check bot's operational server

    pi = PermissionIdentifier()
    permission = pi.get_permission(user_id, username)

    if permission.find('new') != -1:
        print(f"New user: [{username}] has been successfully added to the database")

    # log user input
    ld = LogData()
    ld.log_data(user_id, username, original_input, str(message.channel), message.channel.id)

    # parse command
    pc = ParseCommand()
    parsed_command = pc.parse_command(original_input)

    print(f"Input Data -> User Permission: {permission}, Parsed Command: {parsed_command}")

    # Admin comands =====================================================================================================================================
    if parsed_command.startswith('A'):
        if permission != 'C0':
            await message.channel.send(f"You do not have permission to access Admin commands (C0 clearance required).")
            return

        # purge
        if parsed_command == "A1":
            user_purge_list = original_input.replace('>', '').split(' ')
            try:
                purge_count = int(user_purge_list[1])
            except TypeError:
                await message.channel.send(f"Purge count >{user_purge_list[1]}< incorrect. Please re-enter.")

            await message.channel.purge(limit=1)
            await message.channel.send(f"Message Purge Initiated ({purge_count} messages will be purged in 3 seconds).")
            time.sleep(3)
            await message.channel.purge(limit=purge_count + 1)
            return 
            

    # Moderator commands ================================================================================================================================
    if parsed_command.startswith('M'):
        if permission != 'C1' and permission != 'C0':
            await message.channel.send(f"You do not have permission to access Moderator commands (C1 clearance required).")
            return

        # terminate
        if parsed_command == "M1":
            await message.channel.send(f"Bye!")
            sys.exit(0)


    # User commands ====================================================================================================================================

    # U1 Help
    # U2 Anime search
    # U3 Manga search
    # U4 Character search
    # U5 Get Perm
    # U6 Get Status

    if parsed_command.startswith('U'):
        if permission != 'C2' and permission != 'C2 - new' and permission != 'C1' and permission != 'C0':
            await message.channel.send(f"Error: Please try again later. (DB-1)")
            return

        # help
        if parsed_command == "U1":
            embed_obj = discord.Embed(title="Commands Panel", description="", color=0xA0DB8E)
            embed_obj.add_field(name="`>help`", value="Displays all user commands", inline=False)
            embed_obj.add_field(name="`>status`", value="Gets current bot status (including internet latency)", inline=False)
            embed_obj.add_field(name="`>get anime <anime name>`", value="Searches up an anime with the given name.\nExample: `>get anime kimetsu no yaiba`", inline=False)
            await message.channel.send(embed=embed_obj)

            # await message.channel.send(f"This is the help command. It has not been implemented yet.")
            return

        # get anime
        if parsed_command.startswith("U2"):
            import re

            temp_l = parsed_command.split('|')
            anime_name = original_input.replace('>', '').replace(temp_l[1], '').strip()

            anime_embed = anilist.get_anime_discord(anime_name=anime_name)

            if anime_embed == -1:
                await message.channel.send(f"Anime not found! Please try again or use a different name. (romaji preferred)")
            else:
                await message.channel.send(embed=anime_embed)
                
            return

        


        # get perm
        if parsed_command == "U5":
            embed_obj = discord.Embed(title="Permission Panel", description=f"Username: {username}\nPermission Level: {permission}\nUser ID: {user_id}", color=0xA0DB8E)
            await message.channel.send(embed=embed_obj)
            return

        # get status
        if parsed_command == "U6":
            from ping3 import ping
            try:
                pin = round(ping('google.com') * 1000, 2)
                import datetime
                embed_obj = discord.Embed(title=f"{bot_name} Status Panel", description=f"**Status**: Online\n**Uptime: **{str(datetime.timedelta(seconds = int(time.time() - up_time)))}\n**Internet Latency:** {pin}ms", color=0xA0DB8E)
                await message.channel.send(embed=embed_obj)
            except Exception as e:
                print(e)
                await message.channel.send(f"Warning: Status Request Failed - failed to connect (FN-1)")
            return

    await message.channel.send(f"Sorry, I can't understand your input.\nFor any help, use the command `>help`.")



if __name__ == "__main__":
    while True:
        client.run(BOT_ID)
    