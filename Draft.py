# Fichier de la draft contien les fonction pour faire marché une draft , les test vont se faire ici meme 

# Definir les données , entrée et sortie 
## Chargement du graphe 
import networkx as nx
import matplotlib.pyplot as plt
graphe = nx.read_graphml("./mon_graphe.graphml") # le graphe contien les données champion + lien

## Les lists dont j'aurai besoin pour les heuristique 

list_ban_blue = []
list_ban_red = []

list_role_blue = []
list_role_red = []

list_champion_selectioner_blue = []
list_champion_selectioner_red = []

list_champion_disponible = []

# Initialisation
list_champion_disponible = list(graphe.nodes)

# Fonction de draft chaque pick ou ban est une fonction , elle mis a jours les list et renvois le champion 

## Fonction ban 
def ban_champion(graphe,champion,list_ban):
    graphe.remove_node(champion)
    list_ban.append(champion)
    return 0

## Fonction pick 
def pick_champion(champion,list_champion_selectioner):
    list_champion_selectioner.append(champion)
    return 0
