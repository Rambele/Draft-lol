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
champion = 'Diana'  # Remplacez par le champion souhaité
moyennes_ponderees = calculer_moyenne_ponderee(graphe, champion)

# Afficher les moyennes pondérées des scores
print(f"Moyennes pondérées des scores pour {champion}:")
for type_lien, moyenne_ponderee in moyennes_ponderees.items():
    print(f"{type_lien}: {moyenne_ponderee}")
print(moyennes_ponderees['Counter'])
norme_counter = moyennes_ponderees['Counter']/100
norme_matchup = moyennes_ponderees['Matchup']/100
norme_synergy = moyennes_ponderees['Synergy']/100
data = graphe.nodes['Diana']
score_champ = float(data.get('Score',0))/100
score = 0.2*(norme_matchup-norme_counter) + 0.4*norme_synergy + 0.2*score_champ
print(score)
#Définissez l'environnement : Identifiez clairement l'environnement dans lequel votre agent évoluera. Dans votre cas, cela pourrait être le processus de sélection des champions dans le jeu League of Legends.

#Définissez les états, les actions et les récompenses : Identifiez les différents états dans lesquels votre agent peut se trouver, les actions qu'il peut entreprendre et les récompenses qu'il peut recevoir pour chaque action. Par exemple, un état pourrait être la composition actuelle de l'équipe, les actions pourraient être les choix de champions, et les récompenses pourraient être basées sur les performances de l'équipe.

#Créez un modèle d'apprentissage : Choisissez ou créez un algorithme d'apprentissage par renforcement, comme Q-learning, Deep Q Networks (DQN) ou Proximal Policy Optimization (PPO). Ces algorithmes vous aideront à entraîner votre agent à prendre des décisions optimales dans l'environnement défini.

#Définissez la fonction de récompense : Élaborez une fonction de récompense qui fournit à l'agent des informations sur la qualité de ses actions. Assurez-vous que la fonction de récompense encourage les comportements souhaités.

#Entraînez votre agent : Faites passer votre agent par des itérations d'entraînement, où il explore l'environnement, apprend à partir de ses actions et ajuste ses stratégies en fonction des récompenses reçues.

#Évaluez les performances : Évaluez régulièrement les performances de votre agent dans l'environnement pour vous assurer qu'il s'améliore au fil du temps. Cela peut nécessiter des ajustements dans les paramètres de l'algorithme ou dans la fonction de récompense.

#Itération et amélioration : Continuez à itérer sur votre modèle, à ajuster les paramètres et à améliorer la fonction de récompense en fonction des performances de l'agent.

#Visualisation et analyse : Utilisez des outils de visualisation pour comprendre le comportement de votre agent. Vous pouvez visualiser les choix de champions au fil du temps et comment ils évoluent à mesure que l'agent apprend.

#Optimisation : Si nécessaire, recherchez des moyens d'optimiser votre modèle pour des performances plus rapides ou de meilleures performances.