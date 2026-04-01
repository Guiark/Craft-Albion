import discord
from discord import app_commands
from discord.ext import commands
import math
import os
import configF  # Ta base de données Food (doit contenir RECETTES_FOOD, FOOD_X10, etc.)

# --- LOGIQUE DE CALCUL ---
def get_info_ingredient(nom_ingredient):
    low = nom_ingredient.lower()
    if any(x in low for x in configF.KEYWORDS_ANIMAL):
        return configF.RENDEMENT_ANIMAL, "🐄", True
    if any(x in low for x in configF.KEYWORDS_PLANTE):
        return configF.RENDEMENT_PLANTE, "🌱", False
    if any(x in low for x in configF.KEYWORDS_SPECIAL):
        return None, "🎣", False
    return None, "📦", False

# --- CONFIGURATION DU BOT ---
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

# --- AUTO-COMPLÉTION ---
async def food_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    plats = list(configF.RECETTES_FOOD.keys())
    # Filtre les plats selon ce que l'utilisateur tape
    return [
        app_commands.Choice(name=p, value=p)
        for p in plats if current.lower() in p.lower()
    ][:25] # Limite Discord

# --- COMMANDE SLASH ---
@bot.tree.command(name="food", description="Calcule la répartition des champs pour la cuisine")
@app_commands.describe(
    plat="Choisis ton plat dans la liste",
    plots="Nombre total de plots disponibles",
    nourrir_animaux="Calculer la nourriture pour les animaux ?"
)
@app_commands.autocomplete(plat=food_autocomplete)
async def calculer_food(interaction: discord.Interaction, plat: str, plots: int, nourrir_animaux: bool = True):
    if plat not in configF.RECETTES_FOOD:
        await interaction.response.send_message(f"❌ Le plat '{plat}' est introuvable.", ephemeral=True)
        return

    ingredients = configF.RECETTES_FOOD[plat]
    poids_total_un_craft = 0
    
    # 1. Calcul du poids par craft
    for ing, qte_u in ingredients.items():
        rend, _, est_animal = get_info_ingredient(ing)
        if rend:
            poids_total_un_craft += (qte_u / rend)
            if est_animal and nourrir_animaux:
                besoin_miam = (qte_u / rend) * configF.ANIMAUX_PAR_ENCLOS * configF.CONSOMMATION_PAR_BÊTE
                poids_total_un_craft += (besoin_miam / configF.RENDEMENT_PLANTE)

    # 2. Calcul du nombre de crafts possibles
    if poids_total_un_craft == 0:
        nb_crafts = 0
        total_unites = 0
    else:
        nb_crafts = math.floor(plots / poids_total_un_craft)
        # Vérification multiplicateur x10 ou x1
        multiplicateur = 10 if any(x.lower() in plat.lower() for x in configF.FOOD_X10) else 1
        total_unites = nb_crafts * multiplicateur

    if nb_crafts == 0:
        await interaction.response.send_message(f"❌ Pas assez de plots ({plots}) pour faire un craft de {plat}.", ephemeral=True)
        return

    # 3. Construction de l'Embed
    embed = discord.Embed(
        title=f"🍱 Simulation Cuisine : {plat}",
        description=f"Analyse pour **{plots}** plots disponibles",
        color=discord.Color.orange()
    )
    embed.add_field(name="👨‍🍳 Production estimée", value=f"**{total_unites:,}** unités\n({nb_crafts} crafts)", inline=False)
    
    detail_text = ""
    for ing, qte_u in ingredients.items():
        rend, emo, est_animal = get_info_ingredient(ing)
        if rend:
            total_besoin = qte_u * nb_crafts
            plots_necessaires = math.ceil(total_besoin / rend)
            detail_text += f"{emo} **{ing}** : {plots_necessaires} plots\n"
            
            if est_animal and nourrir_animaux:
                total_nourriture = (total_besoin / rend) * configF.ANIMAUX_PAR_ENCLOS * configF.CONSOMMATION_PAR_BÊTE
                plots_nourriture = math.ceil(total_nourriture / configF.RENDEMENT_PLANTE)
                detail_text += f"└─ 🥕 *Nourriture* : {plots_nourriture} plots\n"
        else:
            detail_text += f"{emo} **{ing}** : *Hors-sol / Pêche*\n"

    embed.add_field(name="🌱 Répartition des plots", value=detail_text, inline=False)
    embed.set_footer(text="Calculateur Food Albion Online")

    await interaction.response.send_message(embed=embed)

# --- LANCEMENT ---
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("TOKEN MANQUANT !")
