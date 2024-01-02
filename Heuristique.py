## Chargement du graphe 
import networkx as nx
import matplotlib.pyplot as plt
graphe = nx.read_graphml("./mon_graphe.graphml") # le graphe contien les données champion + lien


def inspecter_attributs_liens(graphe, champion):
    # Afficher les attributs des liens pour le champion spécifié
    for voisin in graphe.neighbors(champion):
        attributs_lien = graphe[champion][voisin]
        print(f"Attributs du lien entre {champion} et {voisin}: {attributs_lien}")

# Utiliser la fonction pour inspecter les attributs des liens pour un champion donné
champion = 'Bard'  # Remplacez par le champion souhaité
inspecter_attributs_liens(graphe, champion)


