import nextcord
from nextcord.ext import commands, tasks, application_checks
from nextcord import Interaction, SlashOption, Embed, ButtonStyle
from nextcord.ui import Button, View, button, Modal, TextInput, Select, UserSelect
import datetime
import re
import asyncio
import time
import random
from datetime import timedelta, timezone
import sqlite3
import os
import sys
import requests  # For the Heartbeat
import yt_dlp

authorized_user_id = "Your Owner ID"
GUILD_ID = "Your Discord Server ID"
LOG_CHANNEL_ID = "Your Log Channel ID"

# Better Stack Heartbeat URL
HEARTBEAT_URL = "Your Heartbeat URL from Better Stack"

intents = nextcord.Intents.default()
intents.reactions = True
intents.members = True
intents.bans = True
intents.invites = True
intents.message_content = True
intents.dm_messages = True
intents.messages = True
intents.guilds = True
intents.guild_messages = True
intents.voice_states = True
bot = commands.Bot(command_prefix='uszgfkugljsfgjsgf!', intents=intents)
bot.load_extension("music")
bot.load_extension("premium")
bot.load_extension("serverinfo")

def format_time(timestamp):
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


@tasks.loop(minutes=1) 
async def send_heartbeat():
    try:
        response = requests.get(HEARTBEAT_URL)
        if response.status_code == 200:
            print("Heartbeat erfolgreich gesendet!")
        else:
            print(f"Fehler beim Senden des Heartbeats: {response.status_code}")
    except Exception as e:
        print(f"Fehler beim Senden des Heartbeats: {e}")

@bot.event
async def on_ready():
    await bot.sync_application_commands()
    await bot.wait_until_ready() 

    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('>------------------------<')

    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        current_time = datetime.datetime.now()
        formatted_time = format_time(current_time)
        embed = nextcord.Embed(description="## Bot wird gestartet!", color=nextcord.Color.blue())
        embed.set_author(name="Bot startet", icon_url="https://cdn.nextcordapp.com/attachments/955078192966823977/1242863536473112627/CB_2.png")
        embed.set_footer(text=f"Heute um {formatted_time}")
        embed.set_thumbnail(url="https://media.tenor.com/wpSo-8CrXqUAAAAi/loading-loading-forever.gif")
        message = await log_channel.send(embed=embed)
        await asyncio.sleep(5)
        current_time = datetime.datetime.now()
        formatted_time = format_time(current_time)
        embed = nextcord.Embed(description="## Bot ist erfolgreich gestartet!", color=nextcord.Color.green())
        embed.set_author(name="Bot ist ready", icon_url="https://cdn.nextcordapp.com/attachments/955078192966823977/1242863536473112627/CB_2.png")
        embed.set_thumbnail(url="https://media.tenor.com/AWKzZ19awFYAAAAi/checkmark-transparent.gif")
        embed.set_footer(text=f"Heute um {formatted_time}")
        await message.edit(embed=embed)

    async def change_activity():
        activities = [
            nextcord.Activity(type=nextcord.ActivityType.listening, name="/radio"),
            nextcord.Activity(type=nextcord.ActivityType.listening, name="/list"),
            nextcord.Activity(type=nextcord.ActivityType.listening, name="/beta"),
            nextcord.Activity(type=nextcord.ActivityType.listening, name="/server"),
            nextcord.Activity(type=nextcord.ActivityType.listening, name="/top"),
            nextcord.Activity(type=nextcord.ActivityType.listening, name="/serverstats"),
            nextcord.Activity(type=nextcord.ActivityType.listening, name="/help"),
            nextcord.Activity(type=nextcord.ActivityType.listening, name="/globalstats")
        ]
        while True:
            for activity in activities:
                await bot.change_presence(activity=activity, status=nextcord.Status.dnd)
                await asyncio.sleep(5)  

    send_heartbeat.start()
    bot.loop.create_task(change_activity())

@bot.slash_command(name="restart", description="Startet den Bot neu. Nur für den Bot-Besitzer.")
async def restart(interaction: nextcord.Interaction):
    if interaction.user.id != authorized_user_id:
        await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
        return
    
    await interaction.response.send_message("Bot wird neu gestartet...", ephemeral=True)
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.slash_command(name="help", description="Zeigt alle verfügbaren Commands an.")
async def help_command(interaction: nextcord.Interaction):
    embed = nextcord.Embed(
        title="Hilfe - Alle Commands",
        description="Hier sind alle verfügbaren Befehle:",
        color=nextcord.Color.blue()
    )

    embed.add_field(
        name="Allgemeine Befehle", 
        value=(
            "</join:1282442342048993382> - Bot joint in deinen Channel\n"
            "</radio:1283115173200007292> [SENDER] - Spiele einen Radiosender ab\n"
            "</stop:1282442333094285312> - Stoppt das Radio\n"
            "</leave:1283132596242354218> - Bot verlässt den Channel\n"
            "</list:1282442339662565521> - Zeigt alle Server an\n"
            "</server:1283112870711922698> - Zeigt meinen Support Server an\n"
            "</beta:1282479523564224522> [CODE] - Löse deinen Beta-Tester-Code ein\n"
            "</help:1283196081219436636> - Zeigt dir alle öffentlichen Commands an\n"
            " </serverstats:1286309211327828051> - Schaue dir die Server Statistik zu Radio an\n"
            "</globalstats:1286309214637002823> - Schaue dir die Globale Statistik zu Radio an\n"
            "***(Beta Command)*** </like:1283161912288219263> [SENDER] - Gib einem Sender ein Like\n"
            "***(Beta Command)*** </top:1283161915127763197> - Zeigt die Top-Sender an\n"
        ),
        inline=False
    )
    embed.add_field(
        name="Weitere Hilfe",
        value="[Support Server](https://discord.gg/pB2Zwst7qb)",
        inline=False
    )
    embed.set_footer(text="Radio Bot Hilfe")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.slash_command(name="update", description="Hiermit kann MoinMeister3751 die Updates anzeigen lassen")
async def update(
    interaction: Interaction,
    update_description: str = SlashOption(description="Beschreibung des Updates"),
    update_points: str = SlashOption(description="Stichpunkte des Updates, getrennt durch `|`"),
):
    authorized_user_id = 955072460800262164
    if interaction.user.id == authorized_user_id:
        points = update_points.split('|')
        description = f"Heyy Liebes Team,\n\nIch habe von <@955072460800262164> ein Update bekommen.\n\n**Was ist neu?**\n"
        for point in points:
            description += f"* {point.strip()}\n"
        embed = nextcord.Embed(title="Neues Update!", description=description, color=nextcord.Color.orange())
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Du bist nicht berechtigt, diesen Befehl zu verwenden.", ephemeral=True)
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title="Unberechtigter Befehlsversuch", description=f"{interaction.user.mention} hat versucht, den `/update`-Befehl zu verwenden.", color=nextcord.Color.red())
            embed.add_field(name="Benutzer", value=interaction.user.mention)
            embed.add_field(name="Zeitpunkt", value=current_time)
            await log_channel.send(embed=embed)

bot.run('Your Discord Bot Token')