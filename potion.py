import discord
from discord import app_commands
from discord.ext import commands
import math
import os
import configP  # Ta base de données potions

# --- LOGIQUE DE CALCUL ---
def get_info_ingredient(nom_ingredient):
    low = nom_ingredient.lower()
    if any(x in low for x in configP.KEYWORDS_ANIMAL): 
        return configP.RENDEMENT_ANIMAL, "🐄", True
    if any(x in low for x in configP.KEYWORDS_GNOLE): 
        return configP.RENDEMENT_GNOLE, "🍺", False
    if any(x in low for x in configP.KEYWORDS_PLANTE): 
        return configP.RENDEMENT_PLANTE, "🌱", False
    return None, "⚔️", False

# --- CONFIGURATION DU BOT ---
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

# --- AUTO-COMPLÉTION ---
async def potion_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    potions = list(configP.RECETTESP.keys())
    return [
        app_commands.Choice(name=p, value=p)
        for p in potions if current.lower() in p.lower()
    ][:25]

# --- COMMANDE SLASH ---
@bot.tree.command(name="potion", description="Calcule la répartition des plots pour les potions")
@app_commands.describe(
    potion="Nom de la potion",
    plots="Nombre de plots disponibles (ex: 18)",
    nourrir_animaux="Faut-il calculer les plots de nourriture pour les animaux ?"
)
@app_commands.autocomplete(potion=potion_autocomplete)
async def calculer(interaction: discord.Interaction, potion: str, plots: int, nourrir_animaux: bool = True):
    if potion not in configP.RECETTESP:
        await interaction.response.send_message(f"❌ Potion '{potion}' non trouvée.", ephemeral=True)
        return

    ingredients = configP.RECETTESP[potion]
    poids_terrain_par_craft = 0
    
    # 1. Calcul du poids par craft
    for ing, qte_unitaire in ingredients.items():
        rend, _, est_animal = get_info_ingredient(ing)
        if rend:
            poids_terrain_par_craft += (qte_unitaire / rend)
            if est_animal and nourrir_animaux:
                besoin_nourriture = (qte_unitaire / rend) * configP.ANIMAUX_PAR_ENCLOS * configP.CONSOMMATION_PAR_BÊTE
                poids_terrain_par_craft += (besoin_nourriture / configP.RENDEMENT_PLANTE)

    # 2. Calcul du nombre de crafts possibles
    nb_crafts_possibles = math.floor(plots / poids_terrain_par_craft)
    
    if nb_crafts_possibles == 0:
        await interaction.response.send_message(f"❌ Tu n'as pas assez de plots ({plots}) pour fabriquer cette potion.", ephemeral=True)
        return

    # 3. Calcul des unités finales
    unites_per_craft = 5 if any(x in potion.lower() for x in configP.POTIONS_X5) else 10
    total_potions = nb_crafts_possibles * unites_per_craft

    # 4. Création de l'Embed
    embed = discord.Embed(
        title=f"📊 Simulation : {potion}",
        description=f"Basé sur **{plots}** plots disponibles",
        color=discord.Color.blue()
    )
    embed.add_field(name="📦 Production", value=f"**{total_potions:,}** potions\n({nb_crafts_possibles} crafts)", inline=False)
    
    detail_text = ""
    for ing, qte_unitaire in ingredients.items():
        rend, emo, est_animal = get_info_ingredient(ing)
        if rend:
            besoin_ressource = qte_unitaire * nb_crafts_possibles
            plots_ingredi = math.ceil(besoin_ressource / rend)
            detail_text += f"{emo} **{ing}** : {plots_ingredi} plots\n"
            
            if est_animal and nourrir_animaux:
                total_nourriture = (besoin_ressource / rend) * configP.ANIMAUX_PAR_ENCLOS * configP.CONSOMMATION_PAR_BÊTE
                plots_nourriture = math.ceil(total_nourriture / configP.RENDEMENT_PLANTE)
                detail_text += f"└─ 🥕 *Nourriture* : {plots_nourriture} plots\n"
    
    embed.add_field(name="🌱 Répartition des champs", value=detail_text or "Aucun champ requis", inline=False)
    embed.set_footer(text="Calculateur Artisanal Albion")

    await interaction.response.send_message(embed=embed)

# --- LANCEMENT ---
TOKEN = os.getenv('DISCORD_TOKEN') # Ou remplace par ton vrai token entre guillemets
if TOKEN:
    bot.run(TOKEN)
else:
    print("ERREUR : Token manquant !")
