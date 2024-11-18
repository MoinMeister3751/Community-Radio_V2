import nextcord
from nextcord.ext import commands
from nextcord.ui import View, Button
import time
import json

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

RADIO_STATIONS = {
    1: "104.6 RTL",
    2: "1LIVE",
    3: "3FM",
    4: "88.6 ö",
    5: "Ö3",
    6: "Antenne Bayern",
    7: "Antenne Brandenburg",
    8: "--- Offline :(",
    9: "BB Radio",
    10: "BigFM",
    11: "Deutschlandfunk",
    12: "Energy Basel",
    13: "Energy Berlin",
    14: "Energy Sachsen",
    15: "Energy Schweiz",
    16: "Energy Österreich",
    17: "FFN",
    18: "Fritz RBB",
    19: "I Love 2 Dance",
    20: "I Love Radio",
    21: "KISS FM",
    22: "--- Offline :(",
    23: "MDR Sputnik",
    24: "Metal FM",
    25: "N-JOY",
    26: "PSR Sachsen",
    27: "PSR Sachsensongs",
    28: "Radio 21",
    29: "Radio BOB",
    30: "Radio FFH",
    31: "Radio Hamburg",
    32: "Radio Wien",
    33: "Rock Antenne",
    34: "RTL Luxemburg",
    35: "RTL Sachsen",
    36: "RTL PartyMix",
    37: "Superfly",
    38: "Sunshine Live",
    39: "YOU FM",
    40: "---",
    66: "Energy Disneyhits",
    9000: "9000 Radio",
    9001: "MoinMeister3751"
}

RADIO_URLS = {
    "104.6 RTL": "http://stream.104.6rtl.com/rtl-live/mp3-192",
    "N-JOY": "http://icecast.ndr.de/ndr/njoy/live/mp3/128/stream.mp3",
    "Antenne Bayern": "http://stream.antenne.de/antenne",
    "Radio BOB": "https://streams.radiobob.de/2000er/mp3-128/streams.radiobob.de/play.m3u",
    "Energy Berlin": "http://energyradio.de/berlin",
    "Radio FFH": "http://mp3.ffh.de/radioffh/hqlivestream.aac",
    "1LIVE": "http://wdr-1live-live.icecastssl.wdr.de/wdr/1live/live/mp3/128/stream.mp3",
    "Fritz RBB": "https://dispatcher.rndfnk.com/rbb/fritz/live/mp3/mid",
    "Deutschlandfunk": "http://st01.dlf.de/dlf/01/128/mp3/stream.mp3",
    "Sunshine Live": "http://stream.sunshine-live.de/live/mp3-128/stream.sunshine-live.de/play.m3u",
    "Rock Antenne": "https://s4-webradio.rockantenne.bayern/rockantenne-bayern/stream/mp3",
    "KISS FM": "http://stream.kissfm.de/kissfm/mp3-192",
    "MDR Sputnik": "http://mdr-284350-0.cast.mdr.de/mdr/284350/0/mp3/high/stream.mp3",
    "BigFM": "http://streams.bigfm.de/bigfm-deutschland-128-mp3",
    "BB Radio": "https://streambbr.ir-media-tec.com/live/mp3-128/dmhubweb/play.mp3",
    "I Love Radio": "https://play.ilovemusic.de/ilm_iloveradio/",
    "I Love 2 Dance": "https://streams.ilovemusic.de/iloveradio2.mp3",
    "Radio Hamburg": "http://stream.radiohamburg.de/live/mp3-192/stream.radiohamburg.de",
    "FFN": "http://stream.ffn.de/ffn/mp3-192/stream.ffn.de",
    "YOU FM": "https://dispatcher.rndfnk.com/hr/youfm/live/mp3/high",
    "3FM": "http://icecast.omroep.nl/3fm-bb-mp3",
    "Energy Österreich": "https://scdn.nrjaudio.fm/adwz1/at/36001/mp3_128.mp3",
    "Energy Schweiz": "http://energyzuerich.ice.infomaniak.ch/energyzuerich-high.mp3",
    "88.6 ö": "https://radio886.at/streams/88.6_On_Air/ubuntu_users_de/mp3",
    "RTL Luxemburg": "http://sc-rtllive.newmedia.lu:80/",
    "Superfly": "http://stream01.superfly.fm:8080/live128",
    "Ö3": "http://orf-live.ors-shoutcast.at/oe3-q2a",
    "Radio Wien": "https://orf-live.ors-shoutcast.at/wie-q1a.m3u",
    "PSR Sachsen": "http://streams.radiopsr.de/psr-live/mp3-192/mediaplayer",
    "RTL Sachsen": "https://web.radio.hitradio-rtl.de/hrrtl-sachsen/stream/mp3?aggregator=direktlink",
    "RTL PartyMix": "https://web.radio.hitradio-rtl.de/hrrtl-maxis/stream/mp3?aggregator=direktlink",
    "Energy Basel": "https://energybern.ice.infomaniak.ch/energybern-high.mp3",
    "Radio 21": "https://radio21.streamabc.net/radio21-hannover-mp3-192-3735655",
    "Metal FM": "https://metal.stream.laut.fm/metal?t302=2024-08-26_19-28-42&uuid=2a88171b-3c35-4d9e-a350-d019ea5fd519",
    "Energy Sachsen": "https://scdn.nrjaudio.fm/de/33013/mp3_128.mp3?origine=wlan&cdn_path=adswizz_lbs9&adws_out_1&access_token=d38452afc3b94eb8b615dc485d4523ac",
    "Antenne Brandenburg": "http://www.antennebrandenburg.de/prenzlau/livemp3",
    "PSR Sachsensongs": "https://streams.radiopsr.de/sachsensongs/mp3-192/onlineradiobox/",
    "---": "---",
    "---": "---",
    "---": "---",
    "Energy Disneyhits": "https://edge18.streamonkey.net/energy-disneyhits?aggregator=shorty",
    "9000 Radio": "https://super-elk-stable.ngrok-free.app/stream",
    "MoinMeister3751": "https://9000-radio.netlify.app/mm3751.mp3"
}
# Load statistics from JSON file
def load_stats(guild_id):
    try:
        with open("radio_stats.json", "r") as f:
            all_stats = json.load(f)
            return all_stats.get(str(guild_id), {})
    except FileNotFoundError:
        return {}

# Save statistics to JSON file
def save_stats(guild_id, stats):
    try:
        with open("radio_stats.json", "r") as f:
            all_stats = json.load(f)
    except FileNotFoundError:
        all_stats = {}

    all_stats[str(guild_id)] = stats
    with open("radio_stats.json", "w") as f:
        json.dump(all_stats, f)

# Update statistics for radio stations
def update_stats(guild_id, station, duration):
    stats = load_stats(guild_id)
    if station not in stats:
        stats[station] = {"count": 0, "total_duration": 0}
    stats[station]["count"] += 1
    stats[station]["total_duration"] += duration
    save_stats(guild_id, stats)

# Current radio station and start time
current_station = None
start_time = None

# Bot Setup
def setup(bot):
    default_activity = nextcord.Activity(type=nextcord.ActivityType.listening, name="/radio")
    bot.loop.create_task(bot.change_presence(activity=default_activity))

    @bot.slash_command(name="radio", description="Spiele einen Radiosender ab oder zeige den aktuell gespielten Sender an.")
    async def radio(interaction: nextcord.Interaction, station: int = None):
        global current_station, start_time

        voice_client = interaction.guild.voice_client

        if station is None:
            # Show the current station
            if voice_client and voice_client.is_playing() and current_station:
                await interaction.response.send_message(f"Derzeit höre ich: **{current_station}**", ephemeral=True)
            else:
                await interaction.response.send_message("Aktuell läuft kein Radiosender.", ephemeral=True)
            return

        # Play a new station
        if station not in RADIO_STATIONS:
            await interaction.response.send_message("Ungültige Sendernummer. Bitte wähle eine gültige Nummer.", ephemeral=True)
            return

        selected_station = RADIO_STATIONS[station]

        if selected_station not in RADIO_URLS:
            await interaction.response.send_message("Dieser Radiosender ist aktuell nicht verfügbar.", ephemeral=True)
            return

        url = RADIO_URLS[selected_station]

        if not voice_client:
            if not interaction.user.voice or not interaction.user.voice.channel:
                await interaction.response.send_message("Du musst in einem Voice-Channel sein, damit ich beitreten und Musik abspielen kann.", ephemeral=True)
                return

            channel = interaction.user.voice.channel
            voice_client = await channel.connect()

        voice_client.stop()
        voice_client.play(nextcord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))
        current_station = selected_station
        start_time = time.time()

        await interaction.response.send_message(f"Ich spiele jetzt: **{current_station}**", ephemeral=True)

    @bot.slash_command(name="leave", description="Lass den Bot den Voice-Channel verlassen.")
    async def leave(interaction: nextcord.Interaction):
        global current_station, start_time

        voice_client = interaction.guild.voice_client

        if voice_client:
            # Update stats when leaving
            if voice_client.is_playing():
                end_time = time.time()
                duration = end_time - start_time
                update_stats(interaction.guild.id, current_station, duration)  # Use the global update_stats

            await bot.change_presence(activity=default_activity)
            await voice_client.disconnect()

            await interaction.response.send_message("Ich habe den Voice-Channel verlassen.", ephemeral=True)
        else:
            await interaction.response.send_message("Ich bin in keinem Voice-Channel.", ephemeral=True)

    @bot.slash_command(name="globalstats", description="Zeige die globalen Radio-Statistiken an.")
    async def globalstats(interaction: nextcord.Interaction):
        try:
            with open("radio_stats.json", "r") as f:
                all_stats = json.load(f)
        except FileNotFoundError:
            await interaction.response.send_message("Es wurden noch keine Statistiken gesammelt.", ephemeral=True)
            return

        global_stats = {}

        # Aggregate stats from all servers
        for guild_id, stats in all_stats.items():
            for station, data in stats.items():
                if station not in global_stats:
                    global_stats[station] = {"count": 0, "total_duration": 0}
                global_stats[station]["count"] += data["count"]
                global_stats[station]["total_duration"] += data["total_duration"]

        if not global_stats:
            await interaction.response.send_message("Es wurden noch keine globalen Statistiken gesammelt.", ephemeral=True)
            return

        description = "\n".join([f"{station}: {data['count']} Mal gespielt, {round(data['total_duration'] / 60, 2)} Minuten gehört" for station, data in global_stats.items()])
        embed = nextcord.Embed(title="Globale Radio-Statistiken", description=description, color=0x00ff00)
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @bot.slash_command(name="serverstats", description="Zeige die Radio-Statistiken für diesen Server an.")
    async def serverstats(interaction: nextcord.Interaction):
        stats = load_stats(interaction.guild.id)  # Load stats for the current server
        if not stats:
            await interaction.response.send_message("Es wurden noch keine Statistiken für diesen Server gesammelt.", ephemeral=True)
            return

        description = "\n".join([f"{station}: {data['count']} Mal gespielt, {round(data['total_duration'] / 60, 2)} Minuten gehört" for station, data in stats.items()])
        embed = nextcord.Embed(title=f"Radio-Statistiken für {interaction.guild.name}", description=description, color=0x00ff00)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.slash_command(name="list", description="Liste der verfügbaren Radiosender anzeigen.")
    async def list_stations(interaction: nextcord.Interaction):
        page1_button = Button(label="Seite 1", style=nextcord.ButtonStyle.primary)
        page2_button = Button(label="Seite 2", style=nextcord.ButtonStyle.primary)

        async def page1_callback(interaction):
            stations_page1 = list(RADIO_STATIONS.items())[:20]
            description_page1 = "\n".join([f"{num}: {name}" for num, name in stations_page1])
            embed_page1 = nextcord.Embed(title="Verfügbare Radiosender (Seite 1)", description=description_page1, color=0x00ff00)
            await interaction.response.edit_message(embed=embed_page1, view=view)

        async def page2_callback(interaction):
            stations_page2 = list(RADIO_STATIONS.items())[20:40]
            description_page2 = "\n".join([f"{num}: {name}" for num, name in stations_page2])
            embed_page2 = nextcord.Embed(title="Verfügbare Radiosender (Seite 2)", description=description_page2, color=0x00ff00)
            await interaction.response.edit_message(embed=embed_page2, view=view)

        page1_button.callback = page1_callback
        page2_button.callback = page2_callback

        view = View()
        view.add_item(page1_button)
        view.add_item(page2_button)

        # Start with page 1
        stations_page1 = list(RADIO_STATIONS.items())[:20]
        description_page1 = "\n".join([f"{num}: {name}" for num, name in stations_page1])
        embed_page1 = nextcord.Embed(title="Verfügbare Radiosender (Seite 1)", description=description_page1, color=0x00ff00)

        await interaction.response.send_message(embed=embed_page1, view=view, ephemeral=True)
