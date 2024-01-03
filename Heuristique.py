## Chargement du graphe 
import networkx as nx
import matplotlib.pyplot as plt
graphe = nx.read_graphml("./mon_graphe.graphml") # le graphe contien les données champion + lien


def calculer_moyenne_ponderee(graphe, champion):
    types_liens = ['Counter', 'Synergy', 'Matchup']
    moyennes_ponderees = {}

    for type_lien in types_liens:
        somme_produit_score_poids = 0
        somme_poids = 0

        # Parcourir tous les voisins du champion avec le type de lien spécifié
        for voisin in graphe.neighbors(champion):
            if 'type' in graphe[champion][voisin] and graphe[champion][voisin]['type'] == type_lien:
                poids_lien = float(graphe[champion][voisin]['label'])
                score_voisin = float(graphe.nodes[voisin]['Score'])
                
                somme_produit_score_poids += score_voisin + abs(poids_lien)
                somme_poids += 1

        # Calculer la moyenne pondérée pour ce type de lien
        if somme_poids != 0:
            moyenne_ponderee_lien = somme_produit_score_poids / somme_poids
            moyennes_ponderees[type_lien] = moyenne_ponderee_lien

    return moyennes_ponderees

# Utiliser la fonction pour calculer les moyennes pondérées des scores pour un champion donné
graphe.remove_node('Hwei')
champion = 'Varus'  # Remplacez par le champion souhaité
moyennes_ponderees = calculer_moyenne_ponderee(graphe, champion)

# Afficher les moyennes pondérées des scores
print(f"Moyennes pondérées des scores pour {champion}:")
for type_lien, moyenne_ponderee in moyennes_ponderees.items():
    print(f"{type_lien}: {moyenne_ponderee}")
print(moyennes_ponderees['Counter'])
norme_counter = moyennes_ponderees['Counter']/100
norme_matchup = moyennes_ponderees['Matchup']/100
norme_synergy = moyennes_ponderees['Synergy']/100
data = graphe.nodes['Varus']
score_champ = float(data.get('Score',0))/100
score = 0.2*(norme_matchup-norme_counter) + 0.4*norme_synergy + 0.2*score_champ
print(score)