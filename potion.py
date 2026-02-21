import discord
from discord.ext import commands
from discord import app_commands
import math
import re
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

COUTS_FEES_BASE = {
    "5": ["Résistance T3", "Gigantisme T3", "Collante T3", "Poison T4"],
    "10": ["Calme T3", "Purification T3", "Acide T3", "Berserker T4", "Infernal T4", "Récolte T4", "Tornade T4"],
    "15": ["Soin T4", "Énergie T4", "Gigantisme T5", "Résistance T5", "Collante T5", "Poison T6"],
    "30": ["Calme T5", "Purification T5", "Acide T5", "Berserker T6", "Infernal T6", "Récolte T6", "Tornade T6"],
    "45": ["Soin T6", "Énergie T6", "Gigantisme T7", "Résistance T7", "Collante T7", "Invisible T8", "Poison T8"],
    "90": ["Calme T7", "Purification T7", "Acide T7", "Berserker T8", "Infernal T8", "Récolte T8", "Tornade T8"]
}

# --- CLASSE DU BOT ---
class AlbionBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        # Initialisation sans préfixe car on utilise les Slash Commands
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Synchronise les commandes avec Discord au démarrage
        await self.tree.sync()
        print(f"✅ Commandes Slash synchronisées pour {self.user}")

bot = AlbionBot()

@bot.event
async def on_ready():
    print(f"🔥 Connecté en tant que {bot.user}")

# --- COMMANDE /CRAFT ---
@bot.tree.command(name="craft", description="Calculateur complet de potions Albion")
@app_commands.describe(
    potion="Nom de la potion (ex: Soin T6)",
    quantite="Quantité de potions à produire",
    enchantement="Niveau d'enchantement (0, 1, 2 ou 3)",
    prix_vente="Prix unitaire au marché (pour calcul de profit)"
)
@bot.tree.command(name="simul_plots", description="Calcule combien de potions tu peux craft avec tes terrains")
@app_commands.describe(
    potion="Nom de la potion à crafter",
    nb_plots="Nombre total de plots (emplacements) disponibles",
    enchantement="Niveau d'enchantement (0-3)"
)
async def simul_plots(interaction: discord.Interaction, potion: str, nb_plots: int, enchantement: int = 0):
    # 1. Recherche de la potion
    potion_match = next((p for p in RECETTES.keys() if potion.lower() in p.lower()), None)
async def craft(interaction: discord.Interaction, potion: str, quantite: int, enchantement: int = 0, prix_vente: int = 0):
    # Recherche de la potion
    potion_match = None
    for p in RECETTES.keys():
        if potion.lower() in p.lower():
            potion_match = p
            break
    
    if not potion_match:
        await interaction.response.send_message(f"❌ Potion '{potion}' introuvable.", ephemeral=True)
        return

    # Calculs de base
    popos_x5 = ["gigantisme", "résistance", "collante", "soin", "énergie", "poison", "invisible"]
    unites_par_craft = 5 if any(x in potion_match.lower() for x in popos_x5) else 10
    nb_crafts = math.ceil(quantite / unites_par_craft)
    total_reel = nb_crafts * unites_par_craft

    ingredients = RECETTES[potion_match].copy()
    
    # Gestion des extraits (fées)
    if enchantement > 0:
        fee_unitaire = 0
        for q, liste in COUTS_FEES_BASE.items():
            if potion_match in liste:
                fee_unitaire = int(q)
                break
        if fee_unitaire > 0:
            tier_match = re.search(r'T(\d)', potion_match)
            tier_num = tier_match.group(1) if tier_match else "X"
            nom_fee = f"Extrait (T{tier_num}.{enchantement})"
            ingredients[nom_fee] = fee_unitaire

    # Création de l'Embed
    embed = discord.Embed(
        title=f"🧪 {potion_match} (.{enchantement})",
        color=discord.Color.red(),
        description=f"**{total_reel:,}** potions prévues ({nb_crafts} crafts)"
    )

    details = ""
    total_plots = 0
    for ing, qte_recette in ingredients.items():
        besoin = qte_recette * nb_crafts
        low = ing.lower()
        
        # Attribution icône et rendement
        if any(x in low for x in ["lait", "oeuf", "beurre"]):
            rend, emo = RENDEMENT_ANIMAL, "🐄"
        elif any(x in low for x in ["gnôle", "schnaps", "patate", "maïs", "citrouille"]):
            rend, emo = RENDEMENT_GNOLE, "🍺"
        elif any(x in low for x in ["consoude", "chardon", "cardère", "digital", "molène", "mille-feuille", "agaric"]):
            rend, emo = RENDEMENT_PLANTE, "🌱"
        else:
            rend, emo = None, "⚔️"

        if rend:
            plots = math.ceil(besoin / rend)
            total_plots += plots
            details += f"{emo} **{ing}** : {besoin:,} ({plots} plots)\n"
        else:
            details += f"{emo} **{ing}** : {besoin:,} (HDV)\n"

    embed.add_field(name="Ingrédients nécessaires", value=details, inline=False)

    # Calcul Profit
    if prix_vente and prix_vente > 0:
        ca_brut = total_reel * prix_vente
        ca_net = int(ca_brut * 0.935) # Retrait taxe 6.5%
        profit_unit = int(ca_net / total_reel)
        profit_txt = f"💰 CA Brut : **{ca_brut:,}**\n📉 Net (taxe 6.5%) : **{ca_net:,}**\n📈 Revenu/u : **{profit_unit:,}**"
        embed.add_field(name="Estimation Argent", value=profit_txt, inline=False)
        embed.color = discord.Color.gold()

    nb_iles = math.ceil(total_plots / PLOTS_PAR_ILE)
    embed.set_footer(text=f"🚜 Plots : {total_plots} | 🏝️ Îles : {nb_iles}")

    await interaction.response.send_message(embed=embed)

# Autocomplétion
@craft.autocomplete('potion')
async def potion_autocomplete(interaction: discord.Interaction, current: str):
    return [app_commands.Choice(name=p, value=p) for p in RECETTES.keys() if current.lower() in p.lower()][:25]

# Lancement 
token = os.getenv("DISCORD_TOKEN")
bot.run(token)
