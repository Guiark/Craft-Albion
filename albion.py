vert= "\033[92m"
rouge= "\033[91m"
reset= "\033[0m"
jaune= "\033[93m"

print(f"{jaune}-" * 50)
print ("  Bienvenue sur l'outil de craft  ")
print("-" * 50 + reset)
nouveau_craft= "o"

while nouveau_craft.lower() == "o" :
    # Les ressouces 
    total_achat_brut = 0
    ajouter_ressources = "o"

    while ajouter_ressources.lower() == "o":
        nom = input("\nNom de la ressource : ")
        prix = int(input(f"Prix unitaire de {nom} :"))
        qte = int(input(f"Quantité de {nom} pour 1 craft : "))

        total_achat_brut += (prix * qte)

        ajouter_ressources = input("Ajouter une autre ressouces ? (o/n) : ")

    # Le Retour 
    print("-" * 50)
    taux_saisi = float(input("Ton taux de retour en % (ex: 15 ou 32.5) : "))
    taux_reel = taux_saisi /100

    # Coût réel
    cout_fabrication_reel = total_achat_brut * (1 - taux_reel)

    # Vente & Taxes
    print("-" * 50)
    prix_vente = int(input("Prix de vente visé à l'HDV : "))
    prenium = input ("As-tu le Prenium ? (o/n) : ").lower()

    # Précisions Taxes
    frais_placement = 0.025 #Taxes Fixes
    taxes_vente = 0.04 if prenium == 'o' else 0.08

    total_taxes = prix_vente * (frais_placement + taxes_vente)
    revenu_net_apres_vente = prix_vente - total_taxes

    # Verdict
    profit_final = revenu_net_apres_vente - cout_fabrication_reel

    print("\n" + "-" * 50)
    print(f"Revenu Net : {revenu_net_apres_vente:,.0f} Silver")
    print(f"Coût Réel : {cout_fabrication_reel:,.0f} Silver")
    print("-" * 50)

    if profit_final > 0 : 
        print(f"{vert}Bénéfice : +{profit_final:,.0f} Silver")
        print(f"Tu peux lancer la prod !{reset}")
    else:
        print(f"{rouge}Perte : {profit_final:,.0f} Silver")
        print(f"Arrete tes pas rentable !{reset}")
    print("-" * 50)

    nouveau_craft = input("Tu veux faire un autre Craft ? (o/n) : ")