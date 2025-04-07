# THIS WAS MADE BY XPKI DEFINETELY NOT AI

import nextcord
from nextcord.ext import commands
import random
import time
import requests

# Create a bot instance
intents = nextcord.Intents.default()
bot = commands.Bot(intents=intents)

# Function to fetch links from a Pastebin
def fetch_links_from_pastebin(pastebin_url):
    try:
        response = requests.get(pastebin_url)
        response.raise_for_status()  # Raise an error for bad responses
        # Split the response text into lines and filter out empty lines
        links = [line.strip() for line in response.text.splitlines() if line.strip()]
        return links
    except requests.RequestException as e:
        print(f"Error fetching links: {e}")
        return []

# Dictionary to store cooldowns
cooldowns = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')

@bot.slash_command(name="linkget", description="Get a random link via DM with a 24-hour cooldown.")
async def linkget(interaction: nextcord.Interaction):
    """Send a random link via DM with a 24-hour cooldown."""
    user_id = interaction.user.id
    current_time = time.time()

    # Check if the user is on cooldown
    if user_id in cooldowns:
        last_used = cooldowns[user_id]
        if current_time - last_used < 1:  # 86400 seconds = 24 hours
            await interaction.response.send_message("Hey! You're on cooldown :(. Boost the server for no cooldowns.", ephemeral=True)
            return

    # Fetch links from the Pastebin
    pastebin_url = "https://raw.githubusercontent.com/xpki/links/refs/heads/main/links"  # Replace with your actual Pastebin raw URL
    links = fetch_links_from_pastebin(pastebin_url)  # Fetch links from the Pastebin

    if links:
        # If not on cooldown, send a random link
        link = random.choice(links)
        await interaction.user.send(f"Here is your link: {link}")

        # Update the cooldown timestamp
        cooldowns[user_id] = current_time

        # Acknowledge the command
        await interaction.response.send_message("I've sent you a link in DM!", ephemeral=True)
    else:
        await interaction.response.send_message("Sorry, I couldn't fetch any links.", ephemeral=True)

# Run the bot with the token
if __name__ == '__main__':
    bot.run('MTM1NTk1NTE1MjgwODMxNzA1OQ.GBdS0M.aeOVyibjFe25IoaxcOvXFDiYqSc6znNiOHNvk0')