import discord
from discord.ext import commands

# Intents are required for the bot to function correctly with modern Discord API
intents = discord.Intents.default()
intents.messages = True  # Allows the bot to read messages
intents.reactions = True  # Allows the bot to track reactions
intents.guilds = True  # Enables guild-related events
intents.members = True  # Required for managing roles and accessing member information

# Create the bot instance with a command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# ID of the role to be assigned upon verification
MEMBER_ROLE_ID = 123456789012345678  # Replace with your server's Member role ID
# Channel ID where the verification message will be sent
VERIFICATION_CHANNEL_ID = 123456789012345678  # Replace with your verification channel ID

# Verification message content
VERIFICATION_MESSAGE = "React below to verify yourself and gain access to the server!"

@bot.event
async def on_ready():
    """Triggered when the bot is ready."""
    print(f"Bot is ready and logged in as {bot.user}")

    # Send the verification message in the specified channel
    channel = bot.get_channel(VERIFICATION_CHANNEL_ID)
    async for message in channel.history(limit=100):
        if VERIFICATION_MESSAGE in message.content:
            # If the message already exists, react to it
            await message.add_reaction("✅")
            break
    else:
        # If the message doesn't exist, send it and add a reaction
        sent_message = await channel.send(VERIFICATION_MESSAGE)
        await sent_message.add_reaction("✅")

@bot.event
async def on_raw_reaction_add(payload):
    """Triggered when a user adds a reaction."""
    # Check if the reaction is in the verification channel
    if payload.channel_id != VERIFICATION_CHANNEL_ID:
        return

    # Fetch the message associated with the reaction
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    # Ensure the reaction is on the correct message
    if VERIFICATION_MESSAGE not in message.content:
        return

    # Check if the reaction is the correct emoji
    if str(payload.emoji) == "✅":
        guild = bot.get_guild(payload.guild_id)  # Get the guild (server)
        member = guild.get_member(payload.user_id)  # Get the member who reacted
        if member is not None:
            role = guild.get_role(MEMBER_ROLE_ID)  # Get the Member role
            if role not in member.roles:
                await member.add_roles(role)  # Assign the role
                print(f"Added Member role to {member.name}")

@bot.event
async def on_raw_reaction_remove(payload):
    """Triggered when a user removes a reaction."""
    # Check if the reaction is in the verification channel
    if payload.channel_id != VERIFICATION_CHANNEL_ID:
        return

    # Fetch the message associated with the reaction
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    # Ensure the reaction is on the correct message
    if VERIFICATION_MESSAGE not in message.content:
        return

    # Check if the reaction is the correct emoji
    if str(payload.emoji) == "✅":
        guild = bot.get_guild(payload.guild_id)  # Get the guild (server)
        member = guild.get_member(payload.user_id)  # Get the member who removed the reaction
        if member is not None:
            role = guild.get_role(MEMBER_ROLE_ID)  # Get the Member role
            if role in member.roles:
                await member.remove_roles(role)  # Remove the role
                print(f"Removed Member role from {member.name}")

# Replace 'YOUR_BOT_TOKEN' with your bot's token
bot.run('YOUR_BOT_TOKEN')

