import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

VERIFIED_ROLE_ID = 1234567890 #your role ID
VERIFICATION_CHANNEL_ID = 1234567890 #your channle ID

VERIFICATION_MESSAGE = "React with ✅ to verify yourself and gain access to the server!"

@bot.event
async def on_ready():
    print(f"Bot is ready and logged in as {bot.user}")

    channel = bot.get_channel(VERIFICATION_CHANNEL_ID)
    async for message in channel.history(limit=100):
        if VERIFICATION_MESSAGE in message.content:
            break
    else:
        await channel.send(VERIFICATION_MESSAGE)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != VERIFICATION_CHANNEL_ID:
        return

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if VERIFICATION_MESSAGE not in message.content:
        return

    if str(payload.emoji) == "✅":
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member is not None:
            role = guild.get_role(VERIFIED_ROLE_ID)
            if role not in member.roles:
                await member.add_roles(role)
                print(f"Added Verified role to {member.name}")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id != VERIFICATION_CHANNEL_ID:
        return

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if VERIFICATION_MESSAGE not in message.content:
        return

    if str(payload.emoji) == "✅":
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member is not None:
            role = guild.get_role(VERIFIED_ROLE_ID)
            if role in member.roles:
                await member.remove_roles(role)
                print(f"Removed Verified role from {member.name}")

bot.run('your token')
