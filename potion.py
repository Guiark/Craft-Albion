import discord
from discord.ext import commands
from discord import app_commands
import math
import os

# --- CONFIGURATION ALBION ---
RENDEMENT_PLANTE = 54
RENDEMENT_ANIMAL = 14
RENDEMENT_GNOLE = 54
PLOTS_PAR_ILE = 16

# --- BASE DE DONNÉES ---
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
    "Berserker T6": {"Crocs de loup-garou (T5)": 1, "Digital furtive (T6)": 48, "Agaric ésotérique (T2)": 24, "Schnaps de patate (T6)": 12},
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

# --- CLASSE DU BOT ---
class AlbionBot(commands.Bot):
    def __init__(self):
        # On active les intents nécessaires
        intents = discord.Intents.default()
        intents.message_content = True  # <--- AJOUTE CETTE LIGNE
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"✅ Commandes Slash synchronisées")

bot = AlbionBot()

@bot.event
async def on_ready():
    print(f"🔥 Connecté en tant que {bot.user}")

# --- UTILITAIRES ---
def get_info_ingredient(nom_ingredient):
    low = nom_ingredient.lower()
    if any(x in low for x in ["lait", "oeuf", "beurre"]): return RENDEMENT_ANIMAL, "🐄"
    if any(x in low for x in ["gnôle", "schnaps", "patate", "maïs", "citrouille"]): return RENDEMENT_GNOLE, "🍺"
    if any(x in low for x in ["consoude", "chardon", "cardère", "digital", "molène", "mille-feuille", "agaric"]): return RENDEMENT_PLANTE, "🌱"
    return None, "⚔️"

# --- AUTOCOMPLÉTION ---
async def potion_autocomplete(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name=p, value=p) 
        for p in RECETTES.keys() if current.lower() in p.lower()
    ][:25]

# --- COMMANDE /CRAFT ---
@bot.tree.command(name="craft", description="Calcule les ressources nécessaires pour un nombre de potions")
@app_commands.autocomplete(potion=potion_autocomplete)
@app_commands.describe(potion="Nom de la potion", quantite="Nombre de potions voulues", prix_vente="Prix unitaire HDV")
async def craft(interaction: discord.Interaction, potion: str, quantite: int, prix_vente: int = 0):
    if potion not in RECETTES:
        await interaction.response.send_message("❌ Potion introuvable.", ephemeral=True)
        return

    popos_x5 = ["gigantisme", "résistance", "collante", "soin", "énergie", "poison", "invisible"]
    unites_par_craft = 5 if any(x in potion.lower() for x in popos_x5) else 10
    nb_crafts = math.ceil(quantite / unites_par_craft)
    total_reel = nb_crafts * unites_par_craft

    embed = discord.Embed(title=f"🧪 Craft : {potion}", color=discord.Color.blue())
    
    details = ""
    total_plots = 0
    for ing, qte_recette in RECETTES[potion].items():
        besoin = qte_recette * nb_crafts
        rend, emo = get_info_ingredient(ing)
        if rend:
            plots = math.ceil(besoin / rend)
            total_plots += plots
            details += f"{emo} **{ing}** : {besoin:,} ({plots} plots)\n"
        else:
            details += f"{emo} **{ing}** : {besoin:,} (HDV)\n"

    embed.add_field(name=f"Ingrédients pour {total_reel} potions", value=details, inline=False)
    
    if prix_vente > 0:
        ca_net = int((total_reel * prix_vente) * 0.935)
        embed.add_field(name="💰 Argent", value=f"Estimation Net (taxe 6.5%) : **{ca_net:,}**", inline=False)

    nb_iles = math.ceil(total_plots / PLOTS_PAR_ILE)
    embed.set_footer(text=f"🚜 Plots : {total_plots} | 🏝️ Îles : {nb_iles}")
    await interaction.response.send_message(embed=embed)

# --- COMMANDE /SIMUL ---
@bot.tree.command(name="simul", description="Calcule ce que tu peux produire avec tes terrains")
@app_commands.autocomplete(potion=potion_autocomplete)
@app_commands.describe(potion="Nom de la potion", nb_plots="Nombre de plots disponibles")
async def simul(interaction: discord.Interaction, potion: str, nb_plots: int):
    if potion not in RECETTES:
        await interaction.response.send_message("❌ Potion introuvable.", ephemeral=True)
        return

    ingredients = RECETTES[potion]
    poids_terrain_par_craft = 0
    for ing, qte_unitaire in ingredients.items():
        rend, _ = get_info_ingredient(ing)
        if rend:
            poids_terrain_par_craft += (qte_unitaire / rend)

    if poids_terrain_par_craft == 0:
        await interaction.response.send_message("⚠️ Aucune ressource cultivable pour cette potion.", ephemeral=True)
        return

    nb_crafts_possibles = math.floor(nb_plots / poids_terrain_par_craft)
    popos_x5 = ["gigantisme", "résistance", "collante", "soin", "énergie", "poison", "invisible"]
    unites_par_craft = 5 if any(x in potion.lower() for x in popos_x5) else 10
    total_potions = nb_crafts_possibles * unites_par_craft

    repartition = ""
    for ing, qte_unitaire in ingredients.items():
        rend, emo = get_info_ingredient(ing)
        if rend:
            plots_dedies = math.ceil((qte_unitaire * nb_crafts_possibles) / rend)
            repartition += f"{emo} **{ing}** : {plots_dedies} plots\n"

    embed = discord.Embed(title="📊 Simulation de Production", color=discord.Color.green())
    embed.add_field(name="Capacité", value=f"🧪 {potion}\n📍 {nb_plots} plots\n✨ **{total_potions:,}** unités", inline=False)
    embed.add_field(name="🌱 Répartition des champs", value=repartition, inline=False)
    
    await interaction.response.send_message(embed=embed)
# --- LANCEMENT ---
token = os.getenv("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("❌ Erreur : Le DISCORD_TOKEN est introuvable dans les variables d'environnement.") 
