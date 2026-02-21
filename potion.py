import discord
from discord.ext import commands
from discord import app_commands
import math
import re

# --- CONFIGURATION ---
TOKEN = "MTQ3NDU1MzE2MzE0NjIwMzE1Ng.GsE3fL.7ckMIhGvrXrlBNF42yB5gdUQBx50w4G-fEhO-0"
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

class CraftBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = CraftBot()

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

@bot.tree.command(name="craft", description="Calcule les ressources pour une potion")
@app_commands.describe(
    potion="Nom de la potion",
    quantite="Quantité totale désirée",
    enchantement="Niveau d'enchantement (0-3)"
)
async def craft(interaction: discord.Interaction, potion: str, quantite: int, enchantement: int = 0):
    # Recherche floue (pour éviter de taper le nom exact à la lettre près)
    potion_match = None
    for p in RECETTES.keys():
        if potion.lower() in p.lower():
            potion_match = p
            break
    
    if not potion_match:
        return await interaction.response.send_message(f"❌ Potion '{potion}' non trouvée dans la base.", ephemeral=True)

    # --- LOGIQUE DE CALCUL ---
    popos_x5 = ["gigantisme", "résistance", "collante", "soin", "énergie", "poison", "invisible"]
    unites_par_craft = 5 if any(x in potion_match.lower() for x in popos_x5) else 10
    nb_crafts = math.ceil(quantite / unites_par_craft)
    total_reel = nb_crafts * unites_par_craft

    ingredients = RECETTES[potion_match].copy()
    
    # Gestion des fées
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

    # --- PRÉPARATION DE L'EMBED ---
    embed = discord.Embed(
        title=f"🛠️ Production : {potion_match}",
        color=discord.Color.green(),
        description=f"Cible : **{quantite}** | Produit : **{total_reel}** ({nb_crafts} crafts)"
    )

    total_plots = 0
    besoin_animaux = False
    details_ing = ""

    for ing, qte_recette in ingredients.items():
        besoin_total = qte_recette * nb_crafts
        ing_low = ing.lower()
        
        # Détection du type
        if any(x in ing_low for x in ["lait", "oeuf", "beurre"]):
            rendement, emoji, hdv = RENDEMENT_ANIMAL, "🐄", False
            besoin_animaux = True
        elif any(x in ing_low for x in ["gnôle", "schnaps", "patate", "maïs", "citrouille"]):
            rendement, emoji, hdv = RENDEMENT_GNOLE, "🍺", False
        elif any(x in ing_low for x in ["consoude", "chardon", "cardère", "digital", "molène", "mille-feuille", "agaric"]):
            rendement, emoji, hdv = RENDEMENT_PLANTE, "🌱", False
        else: # Ressources de monstres
            emoji, hdv = "⚔️", True

        if hdv:
            details_ing += f"{emoji} **{ing}** : {besoin_total:,} (Acheter HDV)\n"
        else:
            nb_plots = math.ceil(besoin_total / rendement)
            total_plots += nb_plots
            details_ing += f"{emoji} **{ing}** : {besoin_total:,} ({nb_plots} plots)\n"

    embed.add_field(name="Ingrédients nécessaires", value=details_ing, inline=False)
    
    nb_iles = math.ceil(total_plots / PLOTS_PAR_ILE)
    footer_text = f"🚜 Total Plots : {total_plots} | 🏝️ Îles (16p) : {nb_iles}"
    if besoin_animaux:
        footer_text += "\n💡 Note : Achète des animaux ADULTES pour le lait/oeufs !"
    
    embed.set_footer(text=footer_text)

    await interaction.response.send_message(embed=embed)

# Autocomplétion pour le nom des potions
@craft.autocomplete('potion')
async def potion_autocomplete(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name=p, value=p)
        for p in RECETTES.keys() if current.lower() in p.lower()
    ][:25] # Limite Discord de 25 choix

bot.run(TOKEN)
