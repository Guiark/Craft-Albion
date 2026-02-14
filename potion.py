import math
import re

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
    "schnaps T6": {"Patates (T6)": 1},
    "Acide T7": {"Pattes d'esprit (T7)": 1, "Molène ardente (T7)": 144, "Digital furtive (T6)": 72, "Schnaps de patate (T6)": 72, "Lait de mouton (T6)": 36, "Gnôle de maïs (T7)": 36},
    "Purification T7": {"Racine de sylvain (T7)": 1, "Molène ardente (T7)": 144, "Chardon crénelé (T4)": 72, "Consoude feuille-vive (T3)": 72, "Beurre de mouton (T6)": 36, "Gnôle de maïs (T7)": 36},
    "Calme T7": {"Griffes de l'ombre (T7)": 1, "Molène ardente (T7)": 144, "Digital furtive (T6)": 72, "Consoude feuille-vive (T3)": 72, "Agaric ésotérique (T2)": 36, "Gnôle de maïs (T7)": 36},
    "Gigantisme T7": {"Molène ardente (T7)": 72, "Digital furtive (T6)": 36, "Oeuf d'oie (T5)": 18, "Gnôle de maïs (T7)": 18},
    "Résistance T7": {"Molène ardente (T7)": 72, "Digital furtive (T6)": 36, "Chardon crénelé (T4)": 36, "Lait de mouton (T6)": 18, "Gnôle de maïs (T7)": 18},
    "Gnôle T7": {"Maïs": 1},
    "Berserker T8": {"Crocs de loup-garou (T7)": 1, "Mille-feuille morbide (T8)": 144, "Consoude feuille-vive (T3)": 72, "Schnaps de patate (T6)": 72, "Gnôle de maïs (T7)": 36, "Gnôle de citrouille (T8)": 36},
    "Invisible T8": {"Mille-feuille morbide (T8)": 72, "Molène ardente (T7)": 36, "Cardère incendiaire (T5)": 36, "Lait de vache": 18, "Gnôle de citrouille (T8)": 18},
    "Poison T8": {"Mille-feuille morbide (T8)": 72, "Molène ardente (T7)": 36, "Cardère incendiaire (T5)": 36, "Lait de vache": 18, "Gnôle de citrouille (T8)": 18},
    "Récolte T8": {"Dent de pierre runique (T7)": 1, "Beurre de vache": 144, "Mille-feuille morbide (T8)": 72, "Molène ardente (T7)": 72, "Digital furtive (T6)": 36, "Gnôle de citrouille (T8)": 36},
    "Infernal T8": {"Crone de diablotin (T7)": 1, "Lait de vache": 144, "Mille-feuille morbide (T8)": 72, "Molène ardente (T7)": 72, "Oeuf d'oie (T5)": 36, "Gnôle de citrouille (T8)": 36},
    "Tornade T8": {"Plume de l'aube (T7)": 1, "Mille-feuille morbide (T8)": 144, "Molène ardente (T7)": 72, "Gnôle de maïs (T7)": 72, "Oeuf d'oie (T5)": 36, "Gnôle de citrouille (T8)": 36},
    "Gnôle T8": {"Citrouille (T8)": 1}
}

# --- CONFIGURATION (SÉCURITÉ MAX) ---
rendement_plante = 54
rendement_animal = 14  # Valeur basse pour être sûr
rendement_gnole = 54
plots_par_ile = 16

def alchimie():
    print("\n" + "="*65)
    print("           ALBION PRODUCTION POTIONS - MENU")
    print("="*65)

    popos_liste = list(RECETTES.keys())
    tiers = ["T3", "T4", "T5", "T6", "T7", "T8"]
    
    for t in tiers:
        print(f"\n-----------------------{t}-----------------------")
        potions_du_tier = [(i+1, nom) for i, nom in enumerate(popos_liste) if t in nom]
        for j in range(0, len(potions_du_tier), 2):
            p1 = potions_du_tier[j]
            p2 = potions_du_tier[j+1] if j+1 < len(potions_du_tier) else None
            txt1 = f"{p1[0]:>2}. {p1[1]:<20}"
            txt2 = f"{p2[0]:>2}. {p2[1]:<20}" if p2 else ""
            print(f"{txt1} | {txt2}")
    
    print("\n" + "="*65)
    
    try:
        choix = int(input("\nChoisis le numéro de la potion : "))
        nom_selectionne = popos_liste[choix - 1]
        qte_visee = int(input(f"Quantité de [{nom_selectionne}] à produire : "))
        enchant = int(input(f"Enchantement (0, 1, 2 ou 3) : "))
        
        # Mapping des coûts des fées
        COUTS_FEES_BASE = {
            "5": ["Résistance T3", "Gigantisme T3", "Collante T3", "Poison T4"],
            "10": ["Calme T3", "Purification T3", "Acide T3", "Berserker T4", "Infernal T4", "Récolte T4", "Tornade T4"],
            "15": ["Soin T4", "Énergie T4", "Gigantisme T5", "Résistance T5", "Collante T5", "Poison T6"],
            "30": ["Calme T5", "Purification T5", "Acide T5", "Berserker T6", "Infernal T6", "Récolte T6", "Tornade T6"],
            "45": ["Soin T6", "Énergie T6", "Gigantisme T7", "Résistance T7", "Collante T7", "Invisible T8", "Poison T8"],
            "90": ["Calme T7", "Purification T7", "Acide T7", "Berserker T8", "Infernal T8", "Récolte T8", "Tornade T8"]
        }
    except (ValueError, IndexError):
        print("Erreur : Entrée invalide !")
        return

    # --- CALCULS ---
    popos_x5 = ["gigantisme", "résistance", "collante", "soin", "énergie", "poison", "invisible"]
    unites_par_craft = 5 if any(x in nom_selectionne.lower() for x in popos_x5) else 10
    nb_crafts = math.ceil(qte_visee / unites_par_craft)

    ingredients = RECETTES[nom_selectionne].copy()
    if enchant > 0:
        fee_unitaire = 0
        for qte, liste in COUTS_FEES_BASE.items():
            if nom_selectionne in liste:
                fee_unitaire = int(qte)
                break
        if fee_unitaire > 0:
            tier_match = re.search(r'T(\d)', nom_selectionne)
            tier_num = tier_match.group(1) if tier_match else "X"
            nom_fee = f"Extrait arcanique (T{tier_num}.{enchant})"
            ingredients[nom_fee] = fee_unitaire

    print(f"\n{'-' * 20} RÉSULTATS {'-' * 20}")
    print(f"📦 Type : {unites_par_craft} par craft | 🔨 Nombre de crafts : {nb_crafts}")
    print(f"🎯 Total produit : {nb_crafts * unites_par_craft} potions\n")

    total_plots = 0
    besoin_animaux = False

    for ing, qte_recette in ingredients.items():
        besoin_total = qte_recette * nb_crafts
        ing_low = ing.lower()
        
        # Détection du type
        if any(x in ing_low for x in ["lait", "oeuf", "beurre"]):
            rendement, emoji, hdv, animal = rendement_animal, "🐄 ", False, True
            besoin_animaux = True
        elif any(x in ing_low for x in ["gnôle", "schnaps", "patate", "maïs", "citrouille"]):
            rendement, emoji, hdv, animal = rendement_gnole, "🍺 ", False, False
        elif any(x in ing_low for x in ["consoude", "chardon", "cardère", "digital", "molène", "mille-feuille", "agaric"]):
            rendement, emoji, hdv, animal = rendement_plante, "🌱 ", False, False
        elif any(x in ing_low for x in ["griffes", "pattes", "corne", "crocs", "plume", "dent", "racine", "extrait"]):
            emoji, hdv, animal = "⚔️ ", True, False
        else:
            rendement, emoji, hdv, animal = rendement_plante, "🌱 ", False, False

        if hdv:
            print(f"{emoji}{ing:.<30} Besoins : {besoin_total:>6} | [ACHETER HDV]")
        else:
            nb_plots = math.ceil(besoin_total / rendement)
            total_plots += nb_plots
            print(f"{emoji}{ing:.<30} Besoins : {besoin_total:>6} | Plots : {nb_plots}")

    # --- FINAL ---
    nb_iles = math.ceil(total_plots / plots_par_ile)
    print("-" * 65)
    print(f"🚜 Total de plots nécessaires : {total_plots}")
    print(f"🏝️  Estimation d'îles (16 plots) : {nb_iles}")
    if besoin_animaux:
        print("\n💡 NOTE : Achète des ANIMAUX ADULTES, c'est plus rentable !")
        print("   Nourris-les avec la plante la moins chère (Carottes).")
    print("-" * 65)

if __name__ == "__main__":
    alchimie()