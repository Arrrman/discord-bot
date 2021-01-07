import discord
from discord.ext import commands
import random
import youtube_dl
import asyncio

bot = commands.Bot(command_prefix = "$", description = "Je vous observe OwO")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="$help"))
    print("Ready !")

@bot.command()
async def serverInfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    message = f"Le serveur **{serverName}** :computer: contient **{numberOfPerson}** personnes :person_in_manual_wheelchair:. \n La description du serveur **{serverDescription}** :notebook_with_decorative_cover: . \n Ce serveur possède **{numberOfTextChannels}** salon écrit ainsi que **{numberOfVoiceChannels}** vocaux"
    await ctx.send(message)

@bot.command()
async def serverinfo(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    message = f"Le serveur **{serverName}** :computer: contient **{numberOfPerson}** personnes :person_in_manual_wheelchair:. \n La description du serveur **{serverDescription}** :notebook_with_decorative_cover: . \n Ce serveur possède **{numberOfTextChannels}** salon écrit ainsi que **{numberOfVoiceChannels}** vocaux"
    await ctx.send(message)

@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
    message = await ctx.channel.history(limit = nombre + 1).flatten()
    for message in message:
        await message.delete()

@bot.command()
@commands.has_permissions(kick_members = True)
@commands.has_permissions(ban_members = True)
async def kick(ctx, user : discord.User, *, reason= "Aucune raison"):
    await ctx.guild.kick(user, reason = reason)
    embed = discord.Embed(title = "**Kick**", description = "Un modérateur a frappé !", color=0xFF0000)
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/6773_Alert.png")
    embed.add_field(name = "Membre Kick", value = user.name, inline = True)
    embed.add_field(name = "Raison", value = reason, inline = True)
    embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
    embed.set_footer(text = "Le Régiment est meilleur que vous")
    await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user : discord.User, *, reason= "Aucune raison"):
    await ctx.guild.ban(user, reason = reason)
    embed = discord.Embed(title = "**Banissement**", description = "Un modérateur a frappé !", color=0xFF0000)
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    embed.set_thumbnail(url = "https://discordemoji.com/assets/emoji/BanneHammer.png")
    embed.add_field(name = "Membre banni", value = user.name, inline = True)
    embed.add_field(name = "Raison", value = reason, inline = True)
    embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
    embed.set_footer(text = "Le Régiment est meilleur que vous")
    await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	#Ici on sait que lutilisateur na pas ete trouvé
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

@bot.command()
@commands.has_permissions(kick_members = True)
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    embed = discord.Embed(title = "**Mute**", description = "Un modérateur a frappé !", color=0xFF0000)
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/1558_muted.gif")
    embed.add_field(name = "Raison", value = reason, inline = True)
    embed.add_field(name = "Membre", value = member.name, inline = True)
    embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
    embed.set_footer(text = "Le Régiment est meilleur que vous")
    await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions(kick_members = True)
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    embed = discord.Embed(title = "**Unmute**", description = "Un modérateur a frappé !", color=0xFF0000)
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    embed.set_thumbnail(url = "https://emoji.gg/assets/emoji/7466_Cards.png")
    embed.add_field(name = "Raison", value = reason, inline = True)
    embed.add_field(name = "Membre", value = member.name, inline = True)
    embed.add_field(name = "Modérateur", value = ctx.author.name, inline = True)
    embed.set_footer(text = "Le Régiment est meilleur que vous")
    await ctx.send(embed = embed)

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, id="<role ID>")
    await bot.add_roles(member, role)

bot.run("Nzk2NzIzODEzNjg4ODAzMzQ4.X_cE3w.yUPZoOuwMLwjeUMEjfOU7OO-MmY")