import discord
from discord.ext import commands
import os

# Importation de TES fichiers de commandes
import food
import potion

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # On ajoute les commandes slash venant de food.py et potion.py
        self.tree.add_command(food.calculer_food)
        self.tree.add_command(potion.calculer)
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

# Lancement avec ton secret GitHub
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ ERREUR : Le TOKEN est introuvable dans les secrets GitHub.")
