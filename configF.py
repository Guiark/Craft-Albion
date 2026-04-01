# --- CONFIGURATION ALBION FOOD ---
RENDEMENT_PLANTE = 54
RENDEMENT_ANIMAL = 126
RENDEMENT_BEURRE = 126
RENDEMENT_FARINE = 54  # Souvent lié au Blé
CONSOMMATION_PAR_BÊTE = 9
ANIMAUX_PAR_ENCLOS = 9

# --- DETECTION DES TYPES D'INGRÉDIENTS ---
# Priorité aux produits animaux (Lait, Oeufs, Viande)
KEYWORDS_ANIMAL = ["lait", "oeuf", "cru", "beurre"]

# Produits issus de la transformation ou de la culture
KEYWORDS_PLANTE = [
    "carrote", "haricot", "blé", "navet", "choux", "patate", "maïs", "citrouille", 
    "consoude", "chardon", "cardère", "digitale", "molène", "mille-feuille", "agaric", "pain", "farine"
]

# Cas particuliers (souvent achetés ou pêchés, ne consomment pas de plots de terre classiques)
KEYWORDS_SPECIAL = ["poisson", "algue", "clovisse", "calamar", "palourde", "crabe", "sar ", "lutjan", "pieuvre", "anguille", "loche", "kraken", "cavernicole", "energie"]

# Listes pour le calcul du nombre d'unités par craft
FOOD_X10 = ["Soupe Carrotes",
             "Salade de haricots",
             "Soupe de blé",
             "Omelette au poulet",
             "Tourte au poulet",
             "Omelette au poulet avalonienne",
             "Poulet rôti",
             "Salade de navets",
             "Ragoût de chèvre",
             "Ragoût de chèvre avalonien",
             "Sandwich à la chèvre",
             "Sandwich à la chèvre avalonien",
             "Soupe aux choux",
             "Omelette à l'oie",
             "Omelette d'oie avalonienne",
             "Tourte à l'oie",
             "Oie rôti",
             "Salade de patates",
             "Ragoût de mouton",
             "Ragoût de mouton avalonien",
             "Sandwich au mouton",
             "Sandwich au mouton avalonien",
             "Omelette au porc",
             "Omelette au porc avalonien",
             "Tourte au porc",
             "Porc rôti",
             "Ragoût de boeuf",
             "Ragoût de boeuf avalonien",
             "Sandwich au boeuf",
             "Sandwich au boeuf avalonien"
]


# --- BASE DE DONNÉES DES RECETTES ---
RECETTES_FOOD = {
    # T1
    "Poisson grillé T1": {"morceaux de poisson (T1)": 10},
    "Salade d'algues": {"algues (T1)": 10},
    "Soupe Carrotes T1": {"Carrotes (T1)": 16},
    "Soupe de clovisse blanches T1": {"Clovisse blanche (T3)": 1, "Carrotes (T1)": 2},

    # T2
    "Salade de haricots T2": {"Haricots (T2)": 8, "Carrotes (T1)": 8},
    "Salade de calamars des récifs T2": {"Calamar des récifs (T3)": 1, "Haricot (T2)": 1, "Agaric ésotérique (T2)": 1},

    # T3
    "Soupe de blé T3": {"Blé (T3)": 48},
    "Soupe de palourdes vaseuses T3": {"Palourde vaseuse (T5)": 1, "Blé (T3)": 2, "Consoude feuille-vive (T3)": 2, "Poulet cru (T3)": 2},
    "Omelette au poulet T3": {"Blé (T3)": 4, "Poulet cru (T3)": 8, "Oeufs de poule (T3)": 2},
    "Omelette au crabe fouisseur T3": {"Crabe fouisseur (T3)": 1, "Consoude feuille-vive (T3)": 1, "Oeufs de poule (T3)": 1},
    "Omelette au poulet avalonienne T3": {"Lait de chèvre (T4)": 4, "Poulet cru (T3)": 8, "Oeufs de poule (T3)": 2, "Energie avalonienne (T6)": 10},
    "Tourte au poulet T3": {"Blé (T3)": 2, "Farine (T3)": 4, "Poulet cru (T3)": 8},
    "Tourte au sar noirtête T3": {"Sar noirtête (T3)": 1, "Farine (T3)": 1, "Oeufs de poule (T3)": 1},
    "Poulet rôti T3": {"Poulet cru": 8, "Haricots (T2)": 4, "Lait de chèvre (T4)": 4},
    "Lutjan albruine rôti T3": {"Lutjan albruine (T3)": 1, "Consoude feuille-vive (T3)": 1, "Lait de chèvre (T4)": 1},

    # T4
    "Salade de navets T4": {"Navets (T4)": 24, "Blé": 24},
    "Salade de petites pieuvres T4": {"Petite pieuvre (T5)": 1, "Navets (T4)": 2, "Chardon crénelé (T4)": 2, "Chèvre crue (T4)": 2},
    "Ragoût de chèvre T4": {"Navets (T4)": 4, "Pain (T4)": 4, "Chèvre crue (T4)": 8},
    "Ragoût d'anguille verte T4": {"Anguille verte (T3)": 1, "Navets (T4)": 1, "Chardon crénelé (T4)": 1},
    "Ragoût de chèvre avalonien T4": {"Carrotes (T1)": 4, "Navets (T4)": 4, "Energie avalonienne (T6)": 10},
    "Sandwich à la chèvre T4": {"Pain (T4)": 4, "Chèvre cru (T4)": 8, "Beurre de chèvre (T4)": 2},
    "Sandwich à la loche pétrée T4": {"Loche pétrée (T3)": 1, "Navets (T4)": 1, "Beurre de chèvre (T4)": 1},
    "Sandwich à la chèvre avalonien T4": {"Pain (T4)": 4, "Chèvre cru (T4)": 8, "Beurre de chèvre (T4)": 2, "Energie avalonienne (T6)": 10},

    # T5
    "Soupe aux choux T5": {"Choux (T5)": 144},
    "Soupe de palourdes noirebières T5": {"Palourde noirebière (T7)": 1, "Choux (T5)": 6, "Cardère incendiaire (T5)": 6, "Oie crue (T5)": 6},
    "Omelette à l'oie T5": {"Choux (T5)": 12, "Oie crue (T5)": 24, "Oeuf d'oie (T5)": 6},
    "Omelette au crabe de rivière T5": {"Crabe de rivière (T5)": 1, "Choux (T5)": 2, "Cardère incendiaire (T5)": 2, "Oeuf d'oie (T5)": 2},
    "Omelette d'oie avalonienne T5": {"lait de chèvre (T6)": 12, "Oie cru (T5)": 24, "Oeuf d'oie (T5)": 6, "Energie avalonienne (T6)": 30},
    "Tourte à l'oie T5": {"Choux (T5)": 6, "Farine (T3)": 12, "Oie cru (T5)": 24, "Lait de chèvre (T4)": 6},
    "Tourte au cavernicole montagneux T5": {"Cavernicole montagneux (T5)": 1, "Choux (T5)": 2, "Cardère incendiaire (T5)": 2, "Oeuf d'oie": 2},
    "Oie rôti T5": {"Oie cru (T5)": 24, "Choux (T5)": 12, "Lait de mouton (T6)": 12},
    "Lutjan clairebrumasse rôti T5": {"Lutjan clairebrumasse (T5)": 1, "Choux (T5)": 2, "Cardère incendiaire (T5)": 2, "Lait de mouton (T6)": 2},

    # T6
    "Salade de patates T6": {"Patates (T6)": 72, "Choux (T5)": 72},
    "Salade de krakens des profondeurs T6": {"Kraken des profondeurs (T6)": 1, "Patates (T6)": 6, "Digitale furtive (T6)": 6, "Mouton cru (T6)": 6},
    "Ragoût de mouton T6": {"Patates (T6)": 12, "Pain (T4)": 12, "Mouton cru (T6)": 24},
    "Ragoût d'anguille rosée T6": {"Anguille rosée (T5)": 1, "Patates (T6)": 2, "Digitale furtive (T6)": 2, "lait de mouton (T6)": 2},
    "Ragoût de mouton avalonien T6": {"Choux (T5)": 12, "Patates (T6)": 12, "Mouton cru (T6)": 24, "Energie avalonienne (T6)": 30},
    "Sandwich au mouton T6": {"Pain (T4)": 12, "Mouton cru (T6)": 24, "Beurre de mouton (T6)": 6},
    "Sandwich à la loche franche T6": {"Loche franche (T6)": 1, "Patates (T6)": 2, "Digitale furtive (T6)": 2, "Beurre de mouton (T6)": 2},
    "Sandwich au mouton avalonien T6": {"Pain (T4)": 12, "Mouton cru (T6)": 24, "Beurre de mouton (T6)": 6, "Energie avalonienne (T6)": 30},

    # T7
    "Omelette au porc T7": {"Maïs (T7)": 36, "Porc cru (T7)": 72, "Oeuf d'oie (T5)": 18},
    "Omelette au crabe mantou T7": {"Crabe mantou (T7)": 1, "Maïs (T7)": 6, "Molène ardente (T7)": 6, "Porc cru (T7)": 6},
    "Omelette au porc avalonienne T7": {"Lait de vache (T8)": 36, "Porc cru (T7)": 72, "Oeuf d'oie (T5)": 18, "Energie avalonienne (T6)": 90},
    "Tourte au porc T7": {"Maïs (T7)": 18, "Farine (T3)": 36, "Porc cru (T7)": 72, "Lait de mouton (T6)": 18},
    "Tourte au sar boréal T7": {"Sar boréal (T7)": 1, "Maïs (T7)": 6, "Molène ardente (T7)": 6, "Porc cru (T7)": 6},
    "Porc rôti T7": {"Porc cru (T7)": 72, "Maïs (T7)": 36, "Lait de vache (T8)": 36},
    "Lutjan purebrume rôti T7": {"Lutjan purebrume (T7)": 1, "Maïs (T7)": 6, "Molène ardente (T7)": 6, "Lait de vache (T8)": 6},

    # T8
    "Ragoût de boeuf T8": {"Citrouille (T8)": 36, "Pain (T4)": 36, "Boeuf cru (T8)": 72},
    "Ragoût d'anguille morteaux T8": {"Anguille morteau (T8)": 1, "Citrouille (T8)": 8, "Mille-feuille morbide (T8)": 6, "Lait de vache (T8)": 6},
    "Ragoût de boeuf avalonien T8": {"Maïs (T7)": 36, "Citrouille (T8)": 36, "Boeuf cru (T8)": 72, "Energie avalonienne (T6)": 90},
    "Sandwich au boeuf T8": {"Pain (T4)": 36, "Boeuf cru (T8)": 72, "Beurre de vache (T8)": 18},
    "Sandwich à la loche léopard T8": {"Loche léopard (T7)": 1, "Citrouille (T8)": 6, "Mille-feuille morbide (T8)": 6, "Beurre de vache (T8)": 6},
    "Sandwich au boeuf avalonien T8": {"Pain (T4)": 36, "Boeuf cru (T8)": 72, "Beurre de vache (T8)": 18, "Energie avalonienne (T6)": 90},
}
