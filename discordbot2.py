import os
from dotenv import load_dotenv

load_dotenv()

Discord_token = os.getenv('TOKEN')

from typing import Optional
import discord
import time
import asyncio
import random
import re
import copy
import json
from discord import app_commands

global loop

bot_leaderboard = {}
game_lock = []
events = {}
messages = {}

# idk might use it later? porb not
old_codes_dict = {
    "Machine Gun": ["self.down", "self.left", "self.down", "self.up", "self.right"],
    "Anti-Material Rifle": ["self.down", "self.left", "self.right", "self.up", "self.down"],
    "Stalwart": ["self.down", "self.left", "self.down", "self.up", "self.up", "self.left"],
    "Expendable Anti-Tank": ["self.down", "self.down", "self.left", "self.up", "self.right"],
    "Recoilless Rifle": ["self.down", "self.left", "self.right", "self.right", "self.left"],
    "Flamethrower": ["self.down", "self.left", "self.up", "self.down", "self.up"],
    "Autocannon": ["self.down", "self.right", "self.left", "self.down", "self.down", "self.up", "self.up",
                   "self.right"],
    "Heavy Machine Gun": ["self.down", "self.left", "self.up", "self.down", "self.down"],
    "Railgun": ["self.down", "self.right", "self.left", "self.down", "self.down", "self.up", "self.left", "self.down",
                "self.right"],
    "Spear": ["self.down", "self.down", "self.up", "self.down", "self.down"],
    "Orbital Gatling Barrage": ["self.right", "self.down", "self.left", "self.up", "self.up"],
    "Orbital Airburst Strike": ["self.right", "self.right", "self.right"],
    "Orbital 120MM HE Barrage": ["self.right", "self.down", "self.down", "self.left", "self.down", "self.right",
                                 "self.down", "self.down"],
    "Orbital 380MM HE Barrage": ["self.right", "self.down", "self.down", "self.up", "self.up", "self.left", "self.down",
                                 "self.down", "self.down"],
    "Orbital Walking Barrage": ["self.right", "self.right", "self.down", "self.left", "self.right", "self.down"],
    "Orbital Laser": ["self.right", "self.down", "self.up", "self.right", "self.down"],
    "Orbital Railcannon Strike": ["self.right", "self.up", "self.down", "self.down", "self.right"],
    "Eagle Strafing Run": ["self.up", "self.right", "self.right"],
    "Eagle Airstrike": ["self.up", "self.right", "self.down", "self.right"],
    "Eagle Cluster Bomb": ["self.up", "self.right", "self.down", "self.down", "self.right", "self.down"],
    "Eagle Napalm Airstrike": ["self.up", "self.right", "self.down", "self.up"],
    "Jump Pack": ["self.down", "self.up", "self.up", "self.down", "self.up"],
    "Eagle Smoke Strike": ["self.up", "self.right", "self.up", "self.down"],
    "Eagle 110MM Rocket Pods": ["self.up", "self.down", "self.up", "self.left"],
    "Eagle 500KG Bomb": ["self.up", "self.left", "self.down", "self.down", "self.down"],
    "Orbital Precision Strike": ["self.left", "self.left", "self.up"],
    "Orbital Gas Strike": ["self.right", "self.right", "self.down", "self.right"],
    "Orbital EMS Strike": ["self.right", "self.right", "self.left", "self.down"],
    "Orbital Smoke Strike": ["self.right", "self.right", "self.down", "self.up"],
    "HMG Emplacement": ["self.down", "self.up", "self.left", "self.right", "self.right", "self.left"],
    "Shield Generator Relay": ["self.down", "self.up", "self.left", "self.right", "self.left", "self.down"],
    "Tesla Tower": ["self.down", "self.up", "self.right", "self.up", "self.left", "self.right"],
    "Anti-Personnel Minefield": ["self.down", "self.left", "self.down", "self.up", "self.right"],
    "Supply Pack": ["self.down", "self.left", "self.down", "self.up", "self.up", "self.down"],
    "Grenade Launcher": ["self.down", "self.left", "self.down", "self.up", "self.left", "self.down", "self.down"],
    "Laser Cannon": ["self.down", "self.left", "self.down", "self.up", "self.left"],
    "Incendiary Mines": ["self.down", "self.left", "self.left", "self.down"],
    "Guard Dog Rover": ["self.down", "self.left", "self.down", "self.up", "self.left", "self.down", "self.down"],
    "Ballistic Shield Backpack": ["self.down", "self.left", "self.up", "self.up", "self.right"],
    "Arc Thrower": ["self.down", "self.right", "self.up", "self.left", "self.down"],
    "Quasar Cannon": ["self.down", "self.down", "self.up", "self.left", "self.right"],
    "Shield Generator Pack": ["self.down", "self.up", "self.left", "self.down", "self.right", "self.right"],
    "Machine Gun Sentry": ["self.down", "self.up", "self.right", "self.down", "self.right", "self.down", "self.up"],
    "Gatling Sentry": ["self.down", "self.up", "self.right", "self.left", "self.down"],
    "Mortar Sentry": ["self.down", "self.up", "self.right", "self.right", "self.down"],
    "Guard Dog": ["self.down", "self.up", "self.left", "self.down", "self.up", "self.right", "self.down"],
    "Autocannon Sentry": ["self.down", "self.up", "self.right", "self.up", "self.left", "self.up"],
    "Rocket Sentry": ["self.down", "self.up", "self.right", "self.right", "self.left"],
    "EMS Mortar Sentry": ["self.down", "self.down", "self.up", "self.up", "self.left"]
}
codes_dict = {
    "Machine Gun": [":arrow_down_small:", ":arrow_backward:", ":arrow_down_small:", ":arrow_up_small:",
                    ":arrow_forward:"],
    "Anti-Material Rifle": [":arrow_down_small:", ":arrow_backward:", ":arrow_forward:", ":arrow_up_small:",
                            ":arrow_down_small:"],
    "Stalwart": [":arrow_down_small:", ":arrow_backward:", ":arrow_down_small:", ":arrow_up_small:", ":arrow_up_small:",
                 ":arrow_backward:"],
    "Expendable Anti-Tank": [":arrow_down_small:", ":arrow_down_small:", ":arrow_backward:", ":arrow_up_small:",
                             ":arrow_forward:"],
    "Recoilless Rifle": [":arrow_down_small:", ":arrow_backward:", ":arrow_forward:", ":arrow_forward:",
                         ":arrow_backward:"],
    "Flamethrower": [":arrow_down_small:", ":arrow_backward:", ":arrow_up_small:", ":arrow_down_small:",
                     ":arrow_up_small:"],
    "Autocannon": [":arrow_down_small:", ":arrow_forward:", ":arrow_backward:", ":arrow_down_small:",
                   ":arrow_down_small:", ":arrow_up_small:", ":arrow_up_small:", ":arrow_forward:"],
    "Heavy Machine Gun": [":arrow_down_small:", ":arrow_backward:", ":arrow_up_small:", ":arrow_down_small:",
                          ":arrow_down_small:"],
    "Railgun": [":arrow_down_small:", ":arrow_forward:", ":arrow_backward:", ":arrow_down_small:", ":arrow_down_small:",
                ":arrow_up_small:", ":arrow_backward:", ":arrow_down_small:", ":arrow_forward:"],
    "Spear": [":arrow_down_small:", ":arrow_down_small:", ":arrow_up_small:", ":arrow_down_small:",
              ":arrow_down_small:"],
    "Orbital Gatling Barrage": [":arrow_forward:", ":arrow_down_small:", ":arrow_backward:", ":arrow_up_small:",
                                ":arrow_up_small:"],
    "Orbital Airburst Strike": [":arrow_forward:", ":arrow_forward:", ":arrow_forward:"],
    "Orbital 120MM HE Barrage": [":arrow_forward:", ":arrow_down_small:", ":arrow_down_small:", ":arrow_backward:",
                                 ":arrow_down_small:", ":arrow_forward:", ":arrow_down_small:", ":arrow_down_small:"],
    "Orbital 380MM HE Barrage": [":arrow_forward:", ":arrow_down_small:", ":arrow_down_small:", ":arrow_up_small:",
                                 ":arrow_up_small:", ":arrow_backward:", ":arrow_down_small:", ":arrow_down_small:",
                                 ":arrow_down_small:"],
    "Orbital Walking Barrage": [":arrow_forward:", ":arrow_forward:", ":arrow_down_small:", ":arrow_backward:",
                                ":arrow_forward:", ":arrow_down_small:"],
    "Orbital Laser": [":arrow_forward:", ":arrow_down_small:", ":arrow_up_small:", ":arrow_forward:",
                      ":arrow_down_small:"],
    "Orbital Railcannon Strike": [":arrow_forward:", ":arrow_up_small:", ":arrow_down_small:", ":arrow_down_small:",
                                  ":arrow_forward:"],
    "Eagle Strafing Run": [":arrow_up_small:", ":arrow_forward:", ":arrow_forward:"],
    "Eagle Airstrike": [":arrow_up_small:", ":arrow_forward:", ":arrow_down_small:", ":arrow_forward:"],
    "Eagle Cluster Bomb": [":arrow_up_small:", ":arrow_forward:", ":arrow_down_small:", ":arrow_down_small:",
                           ":arrow_forward:", ":arrow_down_small:"],
    "Eagle Napalm Airstrike": [":arrow_up_small:", ":arrow_forward:", ":arrow_down_small:", ":arrow_up_small:"],
    "Jump Pack": [":arrow_down_small:", ":arrow_up_small:", ":arrow_up_small:", ":arrow_down_small:",
                  ":arrow_up_small:"],
    "Eagle Smoke Strike": [":arrow_up_small:", ":arrow_forward:", ":arrow_up_small:", ":arrow_down_small:"],
    "Eagle 110MM Rocket Pods": [":arrow_up_small:", ":arrow_down_small:", ":arrow_up_small:", ":arrow_backward:"],
    "Eagle 500KG Bomb": [":arrow_up_small:", ":arrow_backward:", ":arrow_down_small:", ":arrow_down_small:",
                         ":arrow_down_small:"],
    "Orbital Precision Strike": [":arrow_backward:", ":arrow_backward:", ":arrow_up_small:"],
    "Orbital Gas Strike": [":arrow_forward:", ":arrow_forward:", ":arrow_down_small:", ":arrow_forward:"],
    "Orbital EMS Strike": [":arrow_forward:", ":arrow_forward:", ":arrow_backward:", ":arrow_down_small:"],
    "Orbital Smoke Strike": [":arrow_forward:", ":arrow_forward:", ":arrow_down_small:", ":arrow_up_small:"],
    "HMG Emplacement": [":arrow_down_small:", ":arrow_up_small:", ":arrow_backward:", ":arrow_forward:",
                        ":arrow_forward:", ":arrow_backward:"],
    "Shield Generator Relay": [":arrow_down_small:", ":arrow_up_small:", ":arrow_backward:", ":arrow_forward:",
                               ":arrow_backward:", ":arrow_down_small:"],
    "Tesla Tower": [":arrow_down_small:", ":arrow_up_small:", ":arrow_forward:", ":arrow_up_small:", ":arrow_backward:",
                    ":arrow_forward:"],
    "Anti-Personnel Minefield": [":arrow_down_small:", ":arrow_backward:", ":arrow_down_small:", ":arrow_up_small:",
                                 ":arrow_forward:"],
    "Supply Pack": [":arrow_down_small:", ":arrow_backward:", ":arrow_down_small:", ":arrow_up_small:",
                    ":arrow_up_small:", ":arrow_down_small:"],
    "Grenade Launcher": [":arrow_down_small:", ":arrow_backward:", ":arrow_down_small:", ":arrow_up_small:",
                         ":arrow_backward:", ":arrow_down_small:", ":arrow_down_small:"],
    "Laser Cannon": [":arrow_down_small:", ":arrow_backward:", ":arrow_down_small:", ":arrow_up_small:",
                     ":arrow_backward:"],
    "Incendiary Mines": [":arrow_down_small:", ":arrow_backward:", ":arrow_backward:", ":arrow_down_small:"],
    "Guard Dog Rover": [":arrow_down_small:", ":arrow_backward:", ":arrow_down_small:", ":arrow_up_small:",
                        ":arrow_backward:", ":arrow_down_small:", ":arrow_down_small:"],
    "Ballistic Shield Backpack": [":arrow_down_small:", ":arrow_backward:", ":arrow_up_small:", ":arrow_up_small:",
                                  ":arrow_forward:"],
    "Arc Thrower": [":arrow_down_small:", ":arrow_forward:", ":arrow_up_small:", ":arrow_backward:",
                    ":arrow_down_small:"],
    "Quasar Cannon": [":arrow_down_small:", ":arrow_down_small:", ":arrow_up_small:", ":arrow_backward:",
                      ":arrow_forward:"],
    "Shield Generator Pack": [":arrow_down_small:", ":arrow_up_small:", ":arrow_backward:", ":arrow_down_small:",
                              ":arrow_forward:", ":arrow_forward:"],
    "Machine Gun Sentry": [":arrow_down_small:", ":arrow_up_small:", ":arrow_forward:", ":arrow_down_small:",
                           ":arrow_forward:", ":arrow_down_small:", ":arrow_up_small:"],
    "Gatling Sentry": [":arrow_down_small:", ":arrow_up_small:", ":arrow_forward:", ":arrow_backward:",
                       ":arrow_down_small:"],
    "Mortar Sentry": [":arrow_down_small:", ":arrow_up_small:", ":arrow_forward:", ":arrow_forward:",
                      ":arrow_down_small:"],
    "Guard Dog": [":arrow_down_small:", ":arrow_up_small:", ":arrow_backward:", ":arrow_down_small:",
                  ":arrow_up_small:", ":arrow_forward:", ":arrow_down_small:"],
    "Autocannon Sentry": [":arrow_down_small:", ":arrow_up_small:", ":arrow_forward:", ":arrow_up_small:",
                          ":arrow_backward:", ":arrow_up_small:"],
    "Rocket Sentry": [":arrow_down_small:", ":arrow_up_small:", ":arrow_forward:", ":arrow_forward:",
                      ":arrow_backward:"],
    "EMS Mortar Sentry": [":arrow_down_small:", ":arrow_down_small:", ":arrow_up_small:", ":arrow_up_small:",
                          ":arrow_backward:"]
}

stratagme_names = [
    "Machine Gun",
    "Anti-Material Rifle",
    "Stalwart",
    "Expendable Anti-Tank",
    "Recoilless Rifle",
    "Flamethrower",
    "Autocannon",
    "Heavy Machine Gun",
    "Railgun",
    "Spear",
    "Orbital Gatling Barrage",
    "Orbital Airburst Strike",
    "Orbital 120MM HE Barrage",
    "Orbital 380MM HE Barrage",
    "Orbital Walking Barrage",
    "Orbital Laser",
    "Orbital Railcannon Strike",
    "Eagle Strafing Run",
    "Eagle Airstrike",
    "Eagle Cluster Bomb",
    "Eagle Napalm Airstrike",
    "Jump Pack",
    "Eagle Smoke Strike",
    "Eagle 110MM Rocket Pods",
    "Eagle 500KG Bomb",
    "Orbital Precision Strike",
    "Orbital Gas Strike",
    "Orbital EMS Strike",
    "Orbital Smoke Strike",
    "HMG Emplacement",
    "Shield Generator Relay",
    "Tesla Tower",
    "Anti-Personnel Minefield",
    "Supply Pack",
    "Grenade Launcher",
    "Laser Cannon",
    "Incendiary Mines",
    "Guard Dog Rover",
    "Ballistic Shield Backpack",
    "Arc Thrower",
    "Quasar Cannon",
    "Shield Generator Pack",
    "Machine Gun Sentry",
    "Gatling Sentry",
    "Mortar Sentry",
    "Guard Dog",
    "Autocannon Sentry",
    "Rocket Sentry",
    "EMS Mortar Sentry"
]


def sort_strats(e):
    return len(codes_dict[e])


stratagme_names.sort(key=sort_strats)

print(len(stratagme_names))

MY_GUILD = discord.Object(id=0)  # replace with your guild id


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        # self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync()

    async def on_message(self, message):
        print(message.content)
        print(re.sub("[w|a|s|d]", "", message.content.lower()))
        if re.sub("[w|a|s|d]", "", message.content) == "":
            if message.author.id in events.keys():
                message_text = copy.deepcopy(message.content).lower()
                messages[message.author.id] = message_text
                events[message.author.id].set()
                await message.delete()


intents = discord.Intents.all()
intents.message_content = True
client = MyClient(intents=intents)


@client.event
async def on_ready():
    global bot_leaderboard
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    try:
        with open('scores.json', 'r') as openfile:
            # Reading from json file
            bot_leaderboard = copy.deepcopy(json.load(openfile))
    except:
        with open("scores.json", "w") as outfile:
            json.dump(bot_leaderboard, outfile)

        with open('scores.json', 'r') as openfile:
            # Reading from json file
            bot_leaderboard = copy.deepcopy(json.load(openfile))


@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


@client.tree.command()
async def todo(interaction: discord.Interaction):
    await interaction.response.send_message("""




delete message if wrong/correct
continue system after you get 10 5 sec break then new 10 stratagems
fancy embed
icons (this will have to be done manually and will be a nightmare)
add mission objective stratagem

    """)


@client.tree.command()
async def leaderboard(interaction: discord.Interaction):
    """top 10"""
    top = sorted(bot_leaderboard, key=bot_leaderboard.get, reverse=True)
    top_string = ""

    print(bot_leaderboard)
    print(top)
    for i in range(10):

        if len(bot_leaderboard) == i: break
        person_list = bot_leaderboard[top[i]]
        print(person_list)
        top_string = top_string + f"{i + 1}. {person_list[1]}: {person_list[0]}\n"

    embed = discord.Embed(title="Leaderboard", description=top_string)
    await interaction.response.send_message(embed=embed)


@client.tree.command()
async def stratagem_hero_start(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')
    session = stratagem_hero(interaction)
    asyncio.create_task(session.main_game_loop())


def rand_sort(num, mult):
    return (mult - num) ** 2.0


class stratagem_hero:
    def __init__(self, interaction):
        self.discord_id = id

        self.up = ":arrow_up_small:"
        self.left = ":arrow_backward:"
        self.right = ":arrow_forward:"
        self.down = ":arrow_down_small:"
        self.stratagem_codes = codes_dict
        self.stratagem_names = stratagme_names
        self.interaction = interaction
        self.multiplier = 0
        self.points = 0
        self.sets = 0

    def select_random_wighted_stratagem(self):
        rand_num = []
        for x in range(4):
            i = (random.randint(0, 49 - 1))
            rand_num.append(float(i))
        return int(rand_num[0])

    async def main_game_loop(self):
        interaction = self.interaction
        print("started main game loop")
        event = asyncio.Event()
        events[interaction.user.id] = event
        await interaction.edit_original_response(
            content=f'Hi, {interaction.user.mention} starting <t:{int(time.time() + 3)}:R>')
        await asyncio.sleep(3)
        while True:
            end_time = int(time.time() + 30 - (self.sets))
            old = []
            for x in range(10):

                random_strat = self.select_random_wighted_stratagem()

                while random_strat in old:
                    random_strat = self.select_random_wighted_stratagem()

                old.append(random_strat)

                self.multiplier += 1

                strat = codes_dict[stratagme_names[random_strat]]
                strat_emoji = ""
                for i in strat:
                    strat_emoji = strat_emoji + i

                content_string = f"""
{strat_emoji}
Points: {self.points}
times up in <t:{end_time}:R>
                                """
                embed = discord.Embed(title=f"{stratagme_names[random_strat]}", description=content_string)
                print(
                    f"https://raw.githubusercontent.com/hitroll2121/Stratagem-hero-bot/main/all_strats_images/{stratagme_names[random_strat].replace(' ', '%20')}.png")
                embed.set_thumbnail(
                    url=f"https://raw.githubusercontent.com/hitroll2121/Stratagem-hero-bot/main/all_strats_images/{stratagme_names[random_strat].replace(' ', '%20')}.png")
                active_attempt = True
                while active_attempt:
                    await interaction.edit_original_response(embed=embed, content="")

                    try:
                        await asyncio.wait_for(event.wait(), timeout=end_time - int(time.time()))
                    except asyncio.TimeoutError:
                        await interaction.edit_original_response(content=f"times up points: {self.points}", embed=None)
                        return await self.reset_user()
                    event.clear()
                    wasd = strat_emoji
                    wasd = re.sub(":arrow_up_small:", "w", wasd)
                    wasd = re.sub(":arrow_backward:", "a", wasd)
                    wasd = re.sub(":arrow_down_small:", "s", wasd)
                    wasd = re.sub(":arrow_forward:", "d", wasd)

                    if wasd == messages[interaction.user.id]:
                        self.points = self.points + 1
                        active_attempt = False
            self.sets += 1
            embed2 = discord.Embed(title=f"Set complete!",
                                   description=f"Starting next 10 <t:{int(time.time() + 10)}:R>\nPoints: {self.points}")
            await interaction.edit_original_response(embed=embed2, content="")
            await asyncio.sleep(10)

    async def reset_user(self):
        del (events[self.interaction.user.id])
        name = self.interaction.user.name
        discord_id = self.interaction.user.id
        if discord_id in bot_leaderboard.keys():
            if bot_leaderboard[discord_id][0] < self.points:
                bot_leaderboard[discord_id][0] = self.points
            if bot_leaderboard[discord_id][1] != name:  bot_leaderboard[discord_id][1] = name
        else:
            bot_leaderboard[discord_id] = [self.points, name]
        print(self.points)
        with open("scores.json", "w") as outfile:
            json.dump(bot_leaderboard, outfile)


client.run(Discord_token)