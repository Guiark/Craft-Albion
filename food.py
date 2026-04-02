import discord
from discord import app_commands
import math
import configF  

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

# --- AUTO-COMPLÉTION ---
async def food_autocomplete(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    plats = list(configF.RECETTES_FOOD.keys())
    return [
        app_commands.Choice(name=p, value=p)
        for p in plats if current.lower() in p.lower()
    ][:25] 

# --- COMMANDE SLASH ---
# IMPORTANT : On utilise @app_commands.command au lieu de @bot.tree.command
@app_commands.command(name="food", description="Calcule la répartition des champs pour la cuisine")
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
    
    for ing, qte_u in ingredients.items():
        rend, _, est_animal = get_info_ingredient(ing)
        
        nom_affiche = ing
        if "pain" in ing.lower():
            nom_affiche = "Blé (Pain)"
        if rend:
            poids_total_un_craft += (qte_u / rend)
            if est_animal and nourrir_animaux:
                besoin_miam = (qte_u / rend) * configF.ANIMAUX_PAR_ENCLOS * configF.CONSOMMATION_PAR_BÊTE
                poids_total_un_craft += (besoin_miam / configF.RENDEMENT_PLANTE)

    if poids_total_un_craft == 0:
        nb_crafts = 0
        total_unites = 0
    else:
        nb_crafts = math.floor(plots / poids_total_un_craft)
        multiplicateur = 10 if any(x.lower() in plat.lower() for x in configF.FOOD_X10) else 1
        total_unites = nb_crafts * multiplicateur

    if nb_crafts == 0:
        await interaction.response.send_message(f"❌ Pas assez de plots ({plots}) pour faire un craft de {plat}.", ephemeral=True)
        return

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
