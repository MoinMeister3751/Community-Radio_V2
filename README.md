# Community Radio Bot  

## Beschreibung German
Der Community Radio Bot ist ein vielseitiger Discord-Bot, der es Nutzern ermöglicht, aus einer Auswahl von über 40 Radiosendern ihre Lieblingsstation direkt in einem Voice-Channel zu hören. Der Bot bietet eine Vielzahl von Befehlen für die Interaktion, Statistiken, Verwaltung und spezielle Funktionen für Beta-Nutzer.  

---

## Features und Befehle  

### 🎵 Radio- und Voice-Befehle  
- **`/radio [Sendername]`**  
  Startet den gewünschten Radiosender im aktuellen Voice-Channel.  
- **`/leave`**  
  Verlässt den Voice-Channel, in dem der Bot gerade spielt.  

### 📊 Statistiken  
- **`/globalstats`**  
  Zeigt globale Statistiken, wie z. B. die meistgehörten Sender.  
- **`/serverstats`**  
  Zeigt Statistiken des aktuellen Servers, z. B. die Anzahl der Zuhörer.  

### ℹ️ Informationen und Hilfe  
- **`/help`**  
  Zeigt eine interaktive Liste aller Befehle mit Erklärungen.  
- **`/server`**  
  Zeigt Informationen über den aktuellen Server und seine Radioaktivität.  

### 🛠️ Verwaltung und Updates  
- **`/update`**  
  Aktualisiert die Liste der Radiosender, falls neue hinzugefügt wurden.  
- **`/restart`**  
  Startet den Bot neu, um z. B. Streaming-Probleme zu beheben.  

### 🧪 Beta-Funktionen  
- **`/beta`**  
  Zeigt Informationen zu Beta-Funktionen und wie man Zugang erhält.  
- **`/beta_user`**  
  Listet alle Beta-Nutzer und deren Zugangsstatus.  
- **`/beta_send`**  
  Sendet Beta-Einladungen an berechtigte Nutzer.  

### 📜 Sonstige Befehle  
- **`/list`**  
  Zeigt die vollständige Liste der verfügbaren Radiosender.  

---

## Einrichtung  

1. **Konfiguration in `main.py`, `premium.py` and `serverinfo.py`:**  
   Öffne die Datei `main.py` und ersetze die folgenden Platzhalter mit deinen Informationen:  
   ```python
   authorized_user_id = "Your Owner ID"  # Deine Discord User ID
   GUILD_ID = "Your Discord Server ID"  # Die ID deines Discord Servers
   LOG_CHANNEL_ID = "Your Log Channel ID"  # Die ID des Log-Channels auf deinem Server

**Konfiguration in `main.py`, `premium.py` and `serverinfo.py`:**
   Öffne die Datei `premium.py` und ersetze die folgenden Platzhalter mit deinen Informationen:  
   ```python
   BOT_OWNER_ID = "Your Owner ID" # Deine Discord User ID
   GUILD_IDS = "Your Discord Server ID" # Die ID deines Discord Servers
```
**Konfiguration in `main.py`, `premium.py` und `serverinfo.py`:**  
   Öffne die Datei `serverinfo.py` und ersetze die folgenden Platzhalter mit deinen Informationen:  
   ```python
   BOT_OWNER_ID = "Your Owner ID"  # Deine Discord User ID

```
   # Better Stack Heartbeat URL
   HEARTBEAT_URL = "Your Heartbeat URL from Better Stack"  # URL für die Überwachung des Bots
2. **Bot-Token:**
    Stelle sicher, dass du den Bot-Token in deiner ".env-Datei" oder direkt im Code eingibst, falls du keine Umgebungsvariablen verwendest.

4. **Bot starten:**
    Starte den Bot, lade ihn in deinen Server ein und stelle sicher, dass er die notwendigen Berechtigungen hat.

5. **Befehle nutzen:**
    Nutze /help, um eine Übersicht der Befehle und Funktionen zu erhalten.

---

# Community Radio Bot  

## Description English
The Community Radio Bot is a versatile Discord bot that allows users to listen to their favorite station from a selection of over 40 radio stations directly in a voice channel. The bot offers a variety of commands for interaction, statistics, management and special functions for beta users.  

---

## Features and commands  

### 🎵 Radio and voice commands  
- **`/radio [station name]`**  
  Starts the desired radio station in the current voice channel.  
- **`/leave`**  
  Leaves the voice channel in which the bot is currently playing.  

### 📊 Statistics  
- **`/globalstats`**  
  Shows global statistics such as: B. the most listened to stations.  
- **`/serverstats`**  
  Shows statistics of the current server, e.g. B. the number of listeners.

### ℹ️ Information and help  
- **`/help`**  
  Shows an interactive list of all commands with explanations.  
- **`/server`**  
  Shows information about the current server and its radioactivity.  

### 🛠️ Management and updates  
- **`/update`**  
  Updates the list of radio stations if new ones are added.  
- **`/restart`**  
  Restarts the bot, e.g. B. Troubleshoot streaming issues.  

### 🧪 Beta features  
- **`/beta`**  
  Shows information about beta features and how to get access.  
- **`/beta_user`**  
  Lists all beta users and their access status.  
- **`/beta_send`**  
  Sends beta invitations to eligible users.  

### 📜 Other commands  
- **`/list`**  
  Shows the full list of available radio stations.  

---

## Furnishings  

1. **Configuration in `main.py`, `premium.py` and `serverinfo.py`:**  
   Open the `main.py` file and replace the following placeholders with your information:  
   ```python
   authorized_user_id = "Your Owner ID" # Your Discord User ID
   GUILD_ID = "Your Discord Server ID" # The ID of your Discord server
   LOG_CHANNEL_ID = "Your Log Channel ID" # The ID of the log channel on your server

**Configuration in `main.py`, `premium.py` and `serverinfo.py`:**
   Open the `premium.py` file and replace the following placeholders with your information:  
   ```python
   BOT_OWNER_ID = "Your Owner ID" # Your Discord User ID
   GUILD_IDS = "Your Discord Server ID" # The ID of your Discord server
```
**Configuration in `main.py`, `premium.py` and `serverinfo.py`:**  
   Open the `serverinfo.py` file and replace the following placeholders with your information:  
   ```python
   BOT_OWNER_ID = "Your Owner ID" # Your Discord User ID

```
   # Better Stack Heartbeat URL
   HEARTBEAT_URL = "Your Heartbeat URL from Better Stack" # URL for monitoring the bot
2. **Bot Token:**
    Make sure to enter the bot token in your .env file or directly in the code if you don't use environment variables.

4. **Start bot:**
    Start the bot, invite it to your server and make sure it has the necessary permissions.

5. **Use commands:**
    Use /help to get an overview of the commands and functions.