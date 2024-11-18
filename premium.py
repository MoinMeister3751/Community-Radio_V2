import nextcord
from nextcord.ext import commands
import random
import string
import json
import os

BOT_OWNER_ID = "Your Owner ID"
GUILD_IDS = ["Your Discord Server ID"] 
JSON_DIR = "all json"
PREMIUM_USERS_FILE = os.path.join(JSON_DIR, "premium_users.json")
PREMIUM_CODES_FILE = os.path.join(JSON_DIR, "premium_codes.json")

premium_users = set()
premium_codes = {}

def ensure_file_exists(file_name, default_data):
    os.makedirs(JSON_DIR, exist_ok=True)  
    if not os.path.exists(file_name):
        with open(file_name, "w") as f:
            json.dump(default_data, f)

def load_premium_data():
    global premium_users, premium_codes

    ensure_file_exists(PREMIUM_USERS_FILE, [])
    ensure_file_exists(PREMIUM_CODES_FILE, {})

    with open(PREMIUM_USERS_FILE, "r") as f:
        try:
            premium_users = set(json.load(f))
        except json.JSONDecodeError:
            premium_users = set()

    with open(PREMIUM_CODES_FILE, "r") as f:
        try:
            premium_codes = json.load(f)
        except json.JSONDecodeError:
            premium_codes = {}

def save_premium_data():
    with open(PREMIUM_USERS_FILE, "w") as f:
        json.dump(list(premium_users), f)

    with open(PREMIUM_CODES_FILE, "w") as f:
        json.dump(premium_codes, f)

load_premium_data()

class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def generate_premium_code(self, length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    @nextcord.slash_command(name="beta_send", description="Sende einem Benutzer einen Beta-Code.")
    async def beta_send(self, interaction: nextcord.Interaction, user: nextcord.Member):
        if interaction.user.id != BOT_OWNER_ID:
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
            return

        code = self.generate_premium_code()
        premium_codes[code] = user.id
        save_premium_data()

        try:
            await user.send(f"Du hast einen Beta-Code erhalten: **{code}**\nVerwende den Befehl `/beta code: {code}`, um Beta-Zugriff zu aktivieren.")
            await interaction.response.send_message(f"Beta-Code wurde an {user.mention} gesendet.", ephemeral=True)
        except nextcord.Forbidden:
            await interaction.response.send_message("Konnte die Direktnachricht nicht senden. Stelle sicher, dass der Benutzer Direktnachrichten aktiviert hat.", ephemeral=True)

    @nextcord.slash_command(name="beta", description="Löse einen Beta-Code ein oder zeige verfügbare Beta-Befehle an.")
    async def premium(self, interaction: nextcord.Interaction, code: str = None):
        if code:
            if code in premium_codes:
                if premium_codes[code] == interaction.user.id:
                    premium_users.add(interaction.user.id)
                    save_premium_data()

                    del premium_codes[code]
                    save_premium_data()

                    await interaction.response.send_message("Glückwunsch! Du hast Beta-Zugriff aktiviert.", ephemeral=True)
                else:
                    await interaction.response.send_message("Dieser Code gehört nicht dir.", ephemeral=True)
            else:
                await interaction.response.send_message("Ungültiger oder abgelaufener Beta-Code.", ephemeral=True)
        else:
            if interaction.user.id in premium_users:
                embed = nextcord.Embed(
                    title="Beta-Commands",
                    description="***Hier ist eine Liste der Befehle, die nur für Beta-Benutzer verfügbar sind:***",
                    color=nextcord.Color.gold()
                )

                embed.add_field(name="/stats", value="*Mit /stats kannst du dir die Radio-Stats anzeigen lassen.*", inline=False)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message("Dieser Befehl ist nur für Beta-Benutzer verfügbar.", ephemeral=True)

    @nextcord.slash_command(name="beta_remove", description="Entziehe einem Benutzer den Beta-Status.")
    async def beta_remove(self, interaction: nextcord.Interaction, user: nextcord.Member):
        if interaction.user.id != BOT_OWNER_ID:
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
            return

        if user.id in premium_users:
            premium_users.remove(user.id)
            save_premium_data()
            await interaction.response.send_message(f"Beta-Status wurde von {user.mention} entfernt.", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.mention} hat keinen Beta-Status.", ephemeral=True)

        codes_to_remove = [code for code, uid in premium_codes.items() if uid == user.id]
        for code in codes_to_remove:
            del premium_codes[code]
        save_premium_data()

    @nextcord.slash_command(name="beta_user", description="Zeige alle Beta-Nutzer.")
    async def beta_user(self, interaction: nextcord.Interaction):
        if interaction.user.id != BOT_OWNER_ID:
            await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl zu verwenden.", ephemeral=True)
            return
        
        if not premium_users:
            await interaction.response.send_message("Es gibt derzeit keine Beta-Nutzer.", ephemeral=True)
            return
        
        user_list = []
        for user_id in premium_users:
            user = self.bot.get_user(user_id)
            if user:
                user_list.append(f"Benutzer: {user.mention}")
        
        if not user_list:
            await interaction.response.send_message("Es gibt keine Beta-Nutzer.", ephemeral=True)
        else:
            description = "\n".join(user_list)
            embed = nextcord.Embed(title="Beta-Nutzer", description=description, color=0x00ff00)
            await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Premium(bot))
