import discord
from discord import app_commands
from discord.ext import commands
import os
import math

# --- CONFIGURATION ALBION ---
RENDEMENT_PLANTE = 54
RENDEMENT_ANIMAL = 126
RENDEMENT_GNOLE = 54
CONSOMMATION_PAR_BÊTE = 9  
ANIMAUX_PAR_ENCLOS = 9    

RECETTES = {
    "Acide T3": {"Pattes d'esprit (T3)": 1, "Consoude feuille-vive (T3)": 16},
    "Calme T3": {"Griffes de l'ombre (T3)": 1, "Consoude feuille-vive (T3)": 16},
    "Purification T3": {"Racine de sylvain (T5)": 1, "Consoude feuille-vive (T3)": 16},
    "Berserker T4": {"Crocs de loup-garou (T3)": 1, "Chardon crénelé (T4)": 16},
    "Poison T4": {"Chardon crénelé (T4)": 8, "Consoude feuille-vive (T3)": 4},
    "Énergie T4": {"Chardon crénelé (T4)": 24, "Lait de chèvre (T4)": 6},
    "Récolte T4": {"Dent de pierre runique (T3)": 1, "Beurre de chèvre (T4)": 16},
    "Soin T4": {"Chardon crénelé (T4)": 24, "Oeufs de poule (T3)": 6},
    "Infernal T4": {"Crone de diablotin (T3)": 1, "Lait de chèvre (T4)": 16},
    "Tornade T4": {"Plume de l'aube (T3)": 1, "Chardon crénelé (T4)": 16},
    "Acide T5": {"Pattes d'esprit (T5)": 1, "Cardère incendiaire (T5)": 48, "Chardon crénelé (T4)": 24, "Lait de chèvre (T4)": 12},
    "Purification T5": {"Racine de sylvain (T5)": 1, "Cardère incendiaire (T5)": 48, "Consoude feuille-vive (T3)": 24, "Beurre de chèvre (T4)": 12},
    "Calme T5": {"Griffes de l'ombre (T5)": 1, "Cardère incendiaire (T5)": 48, "Chardon crénelé (T4)": 24, "Agaric ésotérique (T2)": 12},
    "Gigantisme T5": {"Cardère incendiaire (T5)": 24, "Chardon crénelé (T4)": 12, "Oeuf d'oie (T5)": 6},
    "Collante T5": {"Cardère incendiaire (T5)": 24, "Chardon crénelé (T4)": 12, "Oeuf d'oie (T5)": 6},
    "Résistance T5": {"Cardère incendiaire (T5)": 24, "Chardon crénelé (T4)": 12, "Lait de chèvre (T4)": 6},
    "Berserker T6": {"Crocs de loup-garou (5)": 1, "Digital furtive (T6)": 48, "Agaric ésotérique (T2)": 24, "Schnaps de patate (T6)": 12},
    "Poison T6": {"Digital furtive (T6)": 24, "Cardère incendiaire (T5)": 12, "Consoude feuille-vive (T3)": 12, "Lait de mouton (T6)": 6},
    "Énergie T6": {"Digital furtive (T6)": 72, "Lait de mouton (T6)": 18, "Schnaps de patate (T6)": 18},
    "Récolte T6": {"Dent de pierre runique (T5)": 1, "Beurre de mouton (T6)": 48, "Digital furtive (T6)": 24, "Cardère incendiaire (T5)": 12},
    "Soin T6": {"Digital furtive (T6)": 72, "Oeuf d'oie (T5)": 18, "Schnaps de patate (T6)": 18},
    "Infernal T6": {"Crone de diablotin (T5)": 1, "Lait de mouton (T6)": 48, "Digital furtive (T6)": 24, "Oeufs de poule (T3)": 12},
    "Tornade T6": {"Plume de l'aube (T5)": 1, "Digital furtive (T6)": 48, "Cardère incendiaire (T5)": 24, "Oeufs de poule (T3)": 12},
    "Acide T7": {"Pattes d'esprit (T7)": 1, "Molène ardente (T7)": 144, "Digital furtive (T6)": 72, "Schnaps de patate (T6)": 72, "Lait de mouton (T6)": 36, "Gnôle de maïs (T7)": 36},
    "Purification T7": {"Racine de sylvain (T7)": 1, "Molène ardente (T7)": 144, "Chardon crénelé (T4)": 72, "Consoude feuille-vive (T3)": 72, "Beurre de mouton (T6)": 36, "Gnôle de maïs (T7)": 36},
    "Calme T7": {"Griffes de l'ombre (T7)": 1, "Molène ardente (T7)": 144, "Digital furtive (T6)": 72, "Consoude feuille-vive (T3)": 72, "Agaric ésotérique (T2)": 36, "Gnôle de maïs (T7)": 36},
    "Gigantisme T7": {"Molène ardente (T7)": 72, "Digital furtive (T6)": 36, "Oeuf d'oie (T5)": 18, "Gnôle de maïs (T7)": 18},
    "Résistance T7": {"Molène ardente (T7)": 72, "Digital furtive (T6)": 36, "Chardon crénelé (T4)": 36, "Lait de mouton (T6)": 18, "Gnôle de maïs (T7)": 18},
    "Berserker T8": {"Crocs de loup-garou (T7)": 1, "Mille-feuille morbide (T8)": 144, "Consoude feuille-vive (T3)": 72, "Schnaps de patate (T6)": 72, "Gnôle de maïs (T7)": 36, "Gnôle de citrouille (T8)": 36},
    "Invisible T8": {"Mille-feuille morbide (T8)": 72, "Molène ardente (T7)": 36, "Cardère incendiaire (T5)": 36, "Lait de vache": 18, "Gnôle de citrouille (T8)": 18},
    "Poison T8": {"Mille-feuille morbide (T8)": 72, "Molène ardente (T7)": 36, "Cardère incendiaire (T5)": 36, "Lait de vache": 18, "Gnôle de citrouille (T8)": 18},
    "Récolte T8": {"Dent de pierre runique (T7)": 1, "Beurre de vache": 144, "Mille-feuille morbide (T8)": 72, "Molène ardente (T7)": 72, "Digital furtive (T6)": 36, "Gnôle de citrouille (T8)": 36},
    "Infernal T8": {"Crone de diablotin (T7)": 1, "Lait de vache": 144, "Mille-feuille morbide (T8)": 72, "Molène ardente (T7)": 72, "Oeuf d'oie (T5)": 36, "Gnôle de citrouille (T8)": 36},
    "Tornade T8": {"Plume de l'aube (T7)": 1, "Mille-feuille morbide (T8)": 144, "Molène ardente (T7)": 72, "Gnôle de maïs (T7)": 72, "Oeuf d'oie (T5)": 36, "Gnôle de citrouille (T8)": 36},
}

def get_info_ingredient(nom_ingredient):
    low = nom_ingredient.lower()
    if any(x in low for x in ["lait", "oeuf", "beurre"]): return RENDEMENT_ANIMAL, "🐄", True
    if any(x in low for x in ["gnôle", "schnaps", "patate", "maïs", "citrouille"]): return RENDEMENT_GNOLE, "🍺", False
    if any(x in low for x in ["consoude", "chardon", "cardère", "digital", "molène", "mille-feuille", "agaric"]): return RENDEMENT_PLANTE, "🌱", False
    return None, "⚔️", False

# --- CONFIG BOT ---
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user} (ID: {bot.user.id})")

@bot.tree.command(name="potion", description="Calcule la production possible selon tes plots")
@app_commands.describe(
    potion="Le nom de la potion (ex: Soin T4)",
    plots="Nombre total de plots disponibles",
    nourrir_animaux="Cultiver soi-même la nourriture des animaux ?"
)
async def calculer(interaction: discord.Interaction, potion: str, plots: int, nourrir_animaux: bool = True):
    potion_match = next((p for p in RECETTES.keys() if potion.lower() in p.lower()), None)
    
    if not potion_match:
        await interaction.response.send_message(f"❌ Potion '{potion}' introuvable.", ephemeral=True)
        return

    ingredients = RECETTES[potion_match]
    poids_terrain_par_craft = 0
    
    # Calcul du poids de terrain par craft
    for ing, qte_unitaire in ingredients.items():
        rend, _, est_animal = get_info_ingredient(ing)
        if rend:
            poids_terrain_par_craft += (qte_unitaire / rend)
            if est_animal and nourrir_animaux:
                besoin_nourriture = (qte_unitaire / rend) * ANIMAUX_PAR_ENCLOS * CONSOMMATION_PAR_BÊTE
                poids_terrain_par_craft += (besoin_nourriture / RENDEMENT_PLANTE)

    if poids_terrain_par_craft == 0:
        await interaction.response.send_message("Cette potion ne nécessite pas de cultures.", ephemeral=True)
        return

    nb_crafts_possibles = math.floor(plots / poids_terrain_par_craft)
    popos_x5 = ["gigantisme", "résistance", "collante", "soin", "énergie", "poison", "invisible"]
    unites_per_craft = 5 if any(x in potion_match.lower() for x in popos_x5) else 10
    total_potions = nb_crafts_possibles * unites_per_craft

    # Construction de l'Embed Discord
    embed = discord.Embed(
        title=f"📊 Simulation : {potion_match}",
        color=discord.Color.green()
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
                nb_betes = (besoin_ressource / rend) * ANIMAUX_PAR_ENCLOS
                total_nourriture = nb_betes * CONSOMMATION_PAR_BÊTE
                plots_nourriture = math.ceil(total_nourriture / RENDEMENT_PLANTE)
                detail_text += f"└─ 🥕 *Nourriture* : {plots_nourriture} plots\n"
    
    embed.add_field(name="🌱 Répartition des champs", value=detail_text or "Aucun champ requis", inline=False)
    embed.set_footer(text=f"Basé sur {plots} plots disponibles")

    await interaction.response.send_message(embed=embed)

token = os.getenv('DISCORD_TOKEN')
if token:
    bot.run(token)
else:
    print("Erreur : Le DISCORD_TOKEN n'est pas configuré dans les Secrets GitHub.")
