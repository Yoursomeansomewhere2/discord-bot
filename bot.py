import discord
from discord.ext import commands
import os

# ===== BOT SETUP =====
TOKEN = os.environ["TOKEN"]  # Gets token from Render environment variable

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== ON READY =====
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")
    try:
        synced = await bot.tree.sync()
        print(f"📦 Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error: {e}")

# ===== MODERATION COMMANDS =====

# /kick
@bot.tree.command(name="kick", description="Kick a member")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason given"):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("❌ You don't have permission!", ephemeral=True)
        return
    await member.kick(reason=reason)
    await interaction.response.send_message(f"👢 Kicked {member.mention} | Reason: {reason}")

# /ban
@bot.tree.command(name="ban", description="Ban a member")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason given"):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("❌ You don't have permission!", ephemeral=True)
        return
    await member.ban(reason=reason)
    await interaction.response.send_message(f"🔨 Banned {member.mention} | Reason: {reason}")

# /unban
@bot.tree.command(name="unban", description="Unban a user by ID")
async def unban(interaction: discord.Interaction, user_id: str):
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("❌ You don't have permission!", ephemeral=True)
        return
    user = await bot.fetch_user(int(user_id))
    await interaction.guild.unban(user)
    await interaction.response.send_message(f"✅ Unbanned {user.name}")

# /clear (purge messages)
@bot.tree.command(name="clear", description="Delete messages")
async def clear(interaction: discord.Interaction, amount: int):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("❌ You don't have permission!", ephemeral=True)
        return
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"🧹 Deleted {amount} messages", ephemeral=True)

# /mute (timeout)
@bot.tree.command(name="mute", description="Timeout a member")
async def mute(interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "No reason given"):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ You don't have permission!", ephemeral=True)
        return
    duration = datetime.timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await interaction.response.send_message(f"🤐 Muted {member.mention} for {minutes} minutes | Reason: {reason}")

# /unmute
@bot.tree.command(name="unmute", description="Remove timeout")
async def unmute(interaction: discord.Interaction, member: discord.Member):
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("❌ You don't have permission!", ephemeral=True)
        return
    await member.timeout(None)
    await interaction.response.send_message(f"🔊 Unmuted {member.mention}")

# ===== RUN BOT =====
bot.run(TOKEN)
