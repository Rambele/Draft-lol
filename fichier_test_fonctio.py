import networkx as nx
import matplotlib.pyplot as plt

def visualiser_champion_et_liens(graphe, champion):
    # Créer un sous-graphe contenant le champion et ses liens
    sous_graphe = nx.DiGraph()

    # Ajouter le champion au sous-graphe
    sous_graphe.add_node(champion, label=champion, color='red')

    # Ajouter les liens du champion au sous-graphe
    for voisin in graphe.neighbors(champion):
        poids = graphe[champion][voisin].get('label', '')
        type_lien = graphe[champion][voisin].get('type', '')

        sous_graphe.add_node(voisin, label=f"{voisin}\nType: {type_lien}\nPoids: {poids}", color='blue')
        sous_graphe.add_edge(champion, voisin, label=f"Type: {type_lien}\nPoids: {poids}")

    # Afficher le sous-graphe avec les étiquettes des arêtes
    pos = nx.spring_layout(sous_graphe)
    labels = nx.get_edge_attributes(sous_graphe, 'label')
    nx.draw(sous_graphe, pos, with_labels=True, font_size=8, font_color='black', font_weight='bold', node_size=500, node_color='skyblue', edge_color='gray', linewidths=0.5)
    nx.draw_networkx_edge_labels(sous_graphe, pos, edge_labels=labels)
    plt.show()

# Exemple d'utilisation avec votre graphe
# Supposons que vous avez un graphe appelé "graphe" et un champion appelé "champion_exemple"
champion_exemple = 'Lee sin'
graphe = nx.read_graphml("./mon_graphe.graphml") # le graphe contien les données champion + lien
print(graphe.nodes[champion_exemple]['Lane'])
visualiser_champion_et_liens(graphe, champion_exemple)

# //*[@id="page-content"]/div[7]/section/div/div/div/a[1]/div
# //*[@id="page-content"]/div[7]/section/div/div/div/a[1]/div

#//*[@id="page-content"]/div[10]/section/div/div/div/a[1]/div
#//*[@id="page-content"]/div[13]/section/div/div/div/a[1]/div