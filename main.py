import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
import os
import asyncio

bot = commands.Bot(command_prefix="^")

server = 914579638792114186

@bot.event 
async def on_ready():
    await bot.change_presence(status=nextcord.Status.dnd, activity=nextcord.Game("^help"))
    print(f"{bot.user} Is Online")
    

@bot.command()
async def ban(ctx, member : nextcord.Member, *, reason=None):
    guild = ctx.guild
    await member.ban(reason=reason)
    await ctx.send(f"**{member.name}** Has Been Banned For The Reason: `{reason}`")
    await member.send(f"You Have Been Banned From **{guild.name}** For The Reason: `{reason}`")
    
@bot.command()
async def kick(ctx, member : nextcord.Member, *, reason=None):
    guild = ctx.guild
    await member.kick(reason=reason)
    await ctx.send(f"**{member.name}** Has Been Kicked For The Reason: `{reason}`")
    await member.send(f"You Have Been Kicked From **{guild.name}** For The Reason: `{reason}`")

@bot.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member:nextcord.Member, *, reason="No reason provided"):
  guild = ctx.guild
  mutedRole = nextcord.utils.get(guild.roles, name="Muted")

  if not mutedRole:
    await ctx.send("Muted role not found, creating one...")

    mutedRole = await guild.create_role(name = "Muted")

  for channel in guild.channels:
    await ctx.channel.set_permissions(mutedRole, send_messages=False, add_reactions=False, speak=False, connect=False)

  if mutedRole in guild.roles:
    await member.add_roles(mutedRole)
    await ctx.send(f"**{member.name}** Was Muted By **{ctx.author.name}** For {reason}")
    await member.send(f"You Have Been Muted In **{guild.name}** For {reason}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member:nextcord.Member):
  guild = ctx.guild
  mutedRole = nextcord.utils.get(member.roles, name="Muted")

  if mutedRole in member.roles:
    await member.remove_roles(mutedRole)
    await ctx.send(f"**{member.name}** Was Unuted By **{ctx.author.name}**")
    await member.send(f"You Have Been Unmuted In **{guild.name}**")


@bot.command()
async def announce(ctx, *, message):
  channel = nextcord.utils.get(ctx.guild.text_channels, ipname="announcements")

  if not channel:
    await ctx.send("Could not find announcement channel")
  else:
    embed = nextcord.Embed(title="Announcement", description=message, color=nextcord.Colour.green())
    embed.set_footer(text=f"Announcement by {ctx.author.name}#{ctx.author.discriminator}")
    await channel.send(embed=embed)
    await ctx.message.delete()

@bot.slash_command(name="ping", description="latency", guild_ids=[server])
async def ping(interaction: Interaction):
  await interaction.response.send_message(f"Pong! Latency: {round(bot.latency * 1000)}ms")
  
bot.run(os.environ.get("TOKEN"))