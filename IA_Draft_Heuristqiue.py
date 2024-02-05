import networkx as nx
import matplotlib.pyplot as plt
import time

# Charger le graphe depuis le fichier GraphML
graphe = nx.read_graphml("./mon_graphe.graphml")

def choisir_champion_avec_heuristique(graphe, champions_disponibles, list_role):
    meilleur_champion = None
    meilleur_score = float('-inf')  # Initialiser à une valeur négative infinie

    for champion in champions_disponibles:
        if champion not in graphe:
            continue  # Ignorer les champions qui ne sont pas dans le graphe

        data = graphe.nodes[champion]

        if data.get('Lane') not in list_role :
            continue  # Ignorer les champions avec un role deja pick

        # Ajoutez d'autres critères d'heuristique ici en fonction de vos besoins
        score = float(data.get('Score', 0))  # Par défaut, le score est 0 s'il n'est pas disponible

        # Comparer les scores
        if score > meilleur_score:
            meilleur_score = score
            meilleur_champion = champion

    return meilleur_champion


# Fonction de draft ban les top meta , et pick les meilleurs qui restant 
def Draft(graphe, champions_disponibles):
    list_role  = ['Top ', 'Jungle ','Mid ', 'ADC ', 'Support ']
    list_role_blue  = ['Top ', 'Jungle ','Mid ', 'ADC ', 'Support ']
    list_role_red = ['Top ', 'Jungle ','Mid ', 'ADC ', 'Support ']
    list_champion_selectioner_blue = []
    list_champion_ban_blue = []
    list_champion_selectioner_red = []
    list_champion_ban_red = []
    # Phase ban 1
    for i in range(3):
        Blue_Ban = choisir_champion_avec_heuristique(graphe,champions_disponibles,list_role)
        champions_disponibles.remove(Blue_Ban)
        print('Blue Ban ',i+1,':' + Blue_Ban)
        list_champion_ban_blue.append(Blue_Ban)
        Red_Ban = choisir_champion_avec_heuristique(graphe,champions_disponibles,list_role)
        champions_disponibles.remove(Red_Ban)
        print('Red Ban ',i+1,':' + Red_Ban)
        list_champion_ban_red.append(Red_Ban)
    # Phase pick 1
    Blue_pick1 = choisir_champion_avec_heuristique(graphe,champions_disponibles,list_role_blue)
    champions_disponibles.remove(Blue_pick1)
    lane = graphe.nodes[Blue_pick1]
    list_role_blue.remove(lane.get('Lane'))
    print('Blue Pick 1 :' + Blue_pick1)
    list_champion_selectioner_blue.append(Blue_pick1)
    #time.sleep(2) 
    Red_pick1 = choisir_champion_avec_heuristique(graphe,champions_disponibles,list_role_red)
    champions_disponibles.remove(Red_pick1)
    lane = graphe.nodes[Red_pick1]
    list_role_red.remove(lane.get('Lane'))
    print('Red Pick 1 :' + Red_pick1)
    list_champion_selectioner_red.append(Red_pick1)
    #time.sleep(2) 
    Red_pick2 = choisir_champion_avec_heuristique(graphe,champions_disponibles,list_role_red)
    champions_disponibles.remove(Red_pick2)
    lane = graphe.nodes[Red_pick2]
    list_role_red.remove(lane.get('Lane'))
    print('Red Pick 2 :' + Red_pick2)
    list_champion_selectioner_red.append(Red_pick2)
    #time.sleep(2) 
    Blue_pick2 = choisir_champion_avec_heuristique(graphe,champions_disponibles,list_role_blue)
    champions_disponibles.remove(Blue_pick2)
    lane = graphe.nodes[Blue_pick2]
    list_role_blue.remove(lane.get('Lane'))
    print('Blue Pick 2 :' + Blue_pick2)
    list_champion_selectioner_blue.append(Blue_pick2)
    #time.sleep(2)
    Blue_pick3 = choisir_champion_avec_heuristique(graphe,champions_disponibles,list_role_blue)
    champions_disponibles.remove(Blue_pick3)
    lane = graphe.nodes[Blue_pick3]
    list_role_blue.remove(lane.get('Lane'))
    print('Blue Pick 3 :' + Blue_pick3)
    list_champion_selectioner_blue.append(Blue_pick3)
    #time.sleep(2)
    Red_pick3 = choisir_champion_avec_heuristique(graphe,champions_disponibles,list_role_red)
    champions_disponibles.remove(Red_pick3)
    lane = graphe.nodes[Red_pick3]
    list_role_red.remove(lane.get('Lane'))
    print('Red Pick 3 :' + Red_pick3)
    list_champion_selectioner_red.append(Red_pick3)
    #time.sleep(2) 
    # Phase ban 2
    for i in range(2):
        Red_Ban = choisir_champion_avec_heuristique(graphe,champions_disponibles,list_role)
        champions_disponibles.remove(Red_Ban)
        print('Red Ban ',i+4,':' + Red_Ban)
        list_champion_ban_red.append(Red_Ban)
        Blue_Ban = choisir_champion_avec_heuristique(graphe,champions_disponibles,list_role)
        champions_disponibles.remove(Blue_Ban)
        print('Blue Ban ',i+4,':' + Blue_Ban)
        list_champion_ban_blue.append(Blue_Ban)
    # Phase pick 2
    Red_pick4 = choisir_champion_avec_heuristique(graphe,champions_disponibles,list_role_red)
    champions_disponibles.remove(Red_pick4)
    lane = graphe.nodes[Red_pick4]
    list_role_red.remove(lane.get('Lane'))
    print('Red Pick 4 :' + Red_pick4)
    list_champion_selectioner_red.append(Red_pick4)
    #time.sleep(2)
    Blue_pick4 = choisir_champion_avec_heuristique(graphe,champions_disponibles,list_role_blue)
    champions_disponibles.remove(Blue_pick4)
    lane = graphe.nodes[Blue_pick4]
    list_role_blue.remove(lane.get('Lane'))
    print('Blue Pick 4 :' + Blue_pick4)
    list_champion_selectioner_blue.append(Blue_pick4)
    #time.sleep(2) 
    Blue_pick5 = choisir_champion_avec_heuristique(graphe,champions_disponibles,list_role_blue)
    champions_disponibles.remove(Blue_pick5)
    lane = graphe.nodes[Blue_pick5]
    list_role_blue.remove(lane.get('Lane'))
    print('Blue Pick 5 :' + Blue_pick5)
    list_champion_selectioner_blue.append(Blue_pick5)
    #time.sleep(2) 
    Red_pick5 = choisir_champion_avec_heuristique(graphe,champions_disponibles,list_role_red)
    champions_disponibles.remove(Red_pick5)
    lane = graphe.nodes[Red_pick5]
    list_role_red.remove(lane.get('Lane'))
    print('Red Pick 5 :' + Red_pick5)
    list_champion_selectioner_red.append(Red_pick5)
    #time.sleep(2)

    print(list_champion_ban_blue , '|||||||||' , list_champion_ban_red )
    print(list_champion_selectioner_blue, '||||||||' , list_champion_selectioner_red)


# Exemple d'utilisation pendant la phase de draft
#champions_disponibles = list(graphe.nodes)  # Liste des champions disponibles
champions_disponibles = list(graphe.nodes)
#champion_choisi = choisir_champion_avec_heuristique(graphe,champions_disponibles)
#print(champion_choisi)
Draft(graphe, champions_disponibles)

# Mettez à jour votre graphe ou vos données de draft ici en fonction du champion choisi
# graphe.nodes[champion_choisi] contient les données du champion choisi



# pour le moment j'utilise le score  'Score' presnet dans les donnée du champion ,  je peut ajuster 
# ca en ajoutant le score des matchup : je calcule le score des contre , et le score des matchup pour 
# un meilleur score total 
from scipy.optimize import minimize

# Fonction objectif à maximiser
def objectif(poids):
    # Paramètres à ajuster
    alpha, beta, gamma, delta, epsilon = poids
    
    # Calcul des métriques pour tous les champions
    scores_champions = []
    for champion in graphe:  # Assurez-vous d'avoir la liste complète des champions
        score_champion = calculer_score_globale_champion(champion, graphe, alpha, beta, gamma, delta, epsilon)
        scores_champions.append(score_champion)
    
    # La fonction objectif est l'opposée du score de Varus par rapport aux autres champions
    score_varus = calculer_score_globale_champion("Varus", graphe, alpha, beta, gamma, delta, epsilon)
    return -score_varus

# Supposons que vos poids initiaux soient tous égaux à 1 (vous pouvez ajuster cela)
poids_initiaux = [1, 1, 1, 1, 1]

# Contraintes (par exemple, assurez-vous que les poids sont tous positifs)
contraintes = ({'type': 'ineq', 'fun': lambda x: x})

# Exécution de l'optimisation
resultat_optimisation = minimize(objectif, poids_initiaux, constraints=contraintes)

# Récupération des poids optimisés
poids_optimises = resultat_optimisation.x

# Affichage des poids optimisés
print("Poids optimisés :", poids_optimises)

# Calcul de la métrique composite pour Varus avec les poids optimisés
metrique_composite_varus_optimisee = calculer_score_globale_champion('Varus', graphe, *poids_optimises)
print("Métrique composite optimisée pour Varus :", metrique_composite_varus_optimisee)