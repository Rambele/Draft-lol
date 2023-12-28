import networkx as nx
import matplotlib.pyplot as plt
import random

champion_data = [
    {"name": "Ahri", "note": "A", "style": "Combo", "role": "Mid", "features": [True, False, False, True, True, True, False]},
    {"name": "Darius", "note": "B", "style": "Split", "role": "Jungle", "features": [True, False, True, False, False, False, True]},
    {"name": "Ezreal", "note": "S", "style": "Poke", "role": "ADC", "features": [True, False, False, True, False, True, True]},
    {"name": "Fiora", "note": "A", "style": "Split", "role": "Top", "features": [True, False, True, False, False, False, True]},
    {"name": "Garen", "note": "C", "style": "Tank", "role": "Top", "features": [True, True, False, True, True, False, False]},
    {"name": "Jinx", "note": "S", "style": "Siege", "role": "ADC", "features": [True, False, False, True, False, True, True]},
    {"name": "Katarina", "note": "A", "style": "Assassin", "role": "Mid", "features": [True, True, True, False, True, False, True]},
    {"name": "Lulu", "note": "A", "style": "Protect", "role": "Support", "features": [True, True, False, True, False, False, True]},
    {"name": "Malphite", "note": "B", "style": "Tank", "role": "Top", "features": [True, True, False, True, True, False, False]},
    {"name": "Nami", "note": "A", "style": "Protect", "role": "Support", "features": [True, True, False, True, False, False, True]},
    {"name": "Orianna", "note": "S", "style": "Combo", "role": "Mid", "features": [True, False, False, True, False, True, True]},
    {"name": "Pyke", "note": "A", "style": "Assassin", "role": "Support", "features": [True, True, True, False, True, False, True]},
    {"name": "Quinn", "note": "B", "style": "Split", "role": "Top", "features": [True, False, True, False, False, True, True]},
    {"name": "Riven", "note": "A", "style": "Split", "role": "Top", "features": [True, True, True, False, False, False, True]},
    {"name": "Sivir", "note": "B", "style": "Siege", "role": "ADC", "features": [True, False, False, True, False, True, True]},
    {"name": "Xin Zhao", "note": "B", "style": "Fighter", "role": "Jungle", "features": [True, True, False, False, True, False, False]},
    {"name": "Zed", "note": "A", "style": "Assassin", "role": "Mid", "features": [True, True, True, False, False, True, False]},
    {"name": "Ashe", "note": "A", "style": "ADC", "role": "ADC", "features": [True, False, False, True, False, True, True]},
    {"name": "Thresh", "note": "S", "style": "Support", "role": "Support", "features": [True, True, True, True, False, False, True]},
    {"name": "Rengar", "note": "B", "style": "Assassin", "role": "Jungle", "features": [True, True, False, False, True, False, True]},
    {"name": "Akali", "note": "S", "style": "Assassin", "role": "Mid", "features": [True, True, True, False, True, False, False]},
    {"name": "Vayne", "note": "A", "style": "ADC", "role": "ADC", "features": [True, True, False, True, False, True, True]},
    {"name": "Maokai", "note": "B", "style": "Tank", "role": "Top", "features": [True, True, False, True, True, False, False]},
    {"name": "Janna", "note": "A", "style": "Protect", "role": "Support", "features": [True, True, False, True, False, False, True]},
    {"name": "Lee Sin", "note": "A", "style": "Fighter", "role": "Jungle", "features": [True, True, False, False, True, False, True]},
    {"name": "Lucian", "note": "S", "style": "ADC", "role": "ADC", "features": [True, False, True, True, False, True, True]},
    {"name": "Leona", "note": "B", "style": "Tank", "role": "Support", "features": [True, True, False, True, True, False, True]},
    {"name": "Gragas", "note": "A", "style": "Tank", "role": "Jungle", "features": [True, True, False, True, False, False, False]},
    {"name": "Caitlyn", "note": "A", "style": "Siege", "role": "ADC", "features": [True, False, False, True, False, True, True]},
    {"name": "Yasuo", "note": "S", "style": "Fighter", "role": "Mid", "features": [True, True, True, False, True, False, True]},
]


# Matrices
synergy_matrix_15 = [
    [0, 8, 5, 3, 7, 6, 2, 4, 9, 1, 4, 6, 7, 2, 8, 3, 6, 5, 2, 7, 1, 4, 6, 3, 5, 8, 2, 4, 6, 9],
    [8, 0, 7, 4, 6, 9, 5, 3, 8, 2, 5, 7, 6, 1, 9, 4, 8, 7, 2, 1, 4, 3, 7, 8, 1, 5, 6, 9, 2, 5],
    [5, 7, 0, 6, 8, 4, 9, 2, 5, 7, 3, 1, 9, 6, 4, 6, 9, 2, 4, 6, 8, 5, 3, 7, 2, 1, 5, 8, 9, 7],
    [3, 4, 6, 0, 5, 7, 8, 9, 2, 1, 4, 8, 3, 6, 5, 7, 4, 2, 9, 1, 8, 6, 2, 9, 5, 3, 7, 8, 2, 1],
    [7, 6, 8, 5, 0, 3, 4, 6, 7, 2, 8, 1, 9, 5, 3, 6, 7, 2, 4, 6, 1, 4, 6, 2, 8, 3, 7, 1, 5, 8],
    [6, 9, 4, 7, 3, 0, 6, 8, 9, 5, 7, 2, 1, 3, 7, 5, 9, 1, 3, 7, 2, 6, 1, 3, 8, 4, 2, 3, 6, 5],
    [2, 5, 9, 8, 4, 6, 0, 3, 7, 1, 6, 9, 2, 4, 6, 9, 2, 5, 7, 3, 1, 6, 8, 3, 4, 2, 9, 1, 5, 8],
    [4, 3, 2, 9, 7, 8, 3, 0, 4, 7, 1, 5, 6, 8, 2, 1, 6, 4, 3, 5, 9, 7, 1, 8, 2, 9, 1, 7, 3, 6],
    [9, 8, 5, 2, 7, 9, 7, 4, 0, 6, 3, 1, 5, 6, 9, 2, 8, 1, 4, 6, 3, 7, 1, 4, 6, 9, 5, 3, 7, 8],
    [1, 2, 7, 1, 1, 7, 1, 7, 6, 0, 9, 3, 7, 3, 6, 1, 2, 9, 6, 1, 4, 2, 8, 4, 5, 1, 6, 3, 7, 1],
    [4, 5, 3, 4, 6, 7, 6, 1, 3, 9, 0, 6, 5, 4, 6, 7, 5, 7, 8, 3, 6, 1, 3, 8, 2, 9, 1, 7, 6, 5],
    [6, 7, 1, 8, 1, 2, 9, 5, 1, 3, 6, 0, 7, 3, 1, 8, 9, 3, 5, 4, 6, 2, 9, 1, 7, 6, 5, 8, 4, 2],
    [7, 6, 9, 3, 5, 8, 6, 2, 5, 7, 5, 7, 0, 6, 5, 6, 3, 7, 2, 9, 8, 1, 5, 4, 7, 2, 8, 6, 9, 1],
    [2, 1, 6, 6, 9, 1, 4, 8, 6, 3, 4, 3, 6, 0, 8, 1, 6, 2, 9, 4, 5, 7, 8, 4, 2, 3, 7, 1, 9, 5],
    [8, 9, 4, 5, 3, 3, 6, 2, 9, 6, 6, 1, 5, 8, 0, 7, 5, 8, 2, 1, 7, 6, 1, 4, 6, 9, 3, 7, 2, 8],
    [3, 4, 6, 7, 6, 7, 1, 1, 2, 1, 7, 8, 6, 1, 7, 0, 5, 9, 1, 8, 6, 2, 9, 5, 3, 7, 8, 2, 4, 6],
    [6, 8, 9, 4, 7, 9, 2, 6, 8, 2, 5, 9, 3, 6, 5, 5, 0, 3, 4, 6, 9, 1, 3, 7, 8, 2, 1, 4, 6, 7],
    [5, 7, 2, 2, 2, 1, 5, 4, 1, 9, 7, 3, 7, 2, 8, 9, 3, 0, 6, 5, 1, 4, 6, 7, 8, 1, 2, 9, 6, 3],
    [2, 2, 4, 9, 4, 3, 7, 3, 4, 6, 8, 5, 2, 9, 2, 1, 4, 6, 0, 8, 3, 7, 8, 5, 1, 3, 6, 9, 7, 2],
    [7, 1, 6, 1, 6, 7, 3, 5, 6, 1, 3, 4, 9, 4, 1, 8, 6, 5, 8, 0, 7, 2, 9, 1, 3, 8, 2, 9, 5, 7],
    [1, 4, 8, 8, 1, 2, 1, 9, 1, 4, 6, 6, 8, 5, 7, 6, 9, 1, 3, 7, 0, 6, 3, 5, 4, 6, 2, 9, 1, 8],
    [4, 3, 5, 6, 4, 6, 6, 7, 3, 2, 2, 2, 1, 7, 6, 2, 1, 4, 7, 2, 6, 0, 8, 9, 5, 3, 7, 8, 1, 4],
    [6, 7, 3, 2, 6, 1, 8, 1, 7, 9, 9, 9, 5, 8, 1, 9, 3, 6, 8, 9, 3, 8, 0, 6, 1, 4, 2, 9, 5, 7],
    [3, 8, 7, 9, 2, 3, 3, 4, 4, 5, 1, 5, 4, 4, 3, 5, 7, 1, 5, 1, 5, 9, 6, 0, 8, 9, 2, 7, 6, 1],
    [5, 1, 2, 5, 8, 8, 4, 2, 6, 3, 3, 3, 7, 2, 6, 8, 8, 3, 1, 3, 4, 5, 1, 8, 0, 7, 6, 9, 2, 4],
    [8, 5, 1, 3, 3, 4, 2, 9, 5, 8, 6, 7, 2, 3, 9, 2, 2, 6, 4, 8, 6, 3, 4, 9, 7, 0, 5, 6, 1, 8],
    [2, 6, 5, 7, 7, 2, 9, 1, 3, 1, 9, 1, 8, 7, 1, 1, 1, 9, 6, 2, 2, 7, 2, 2, 6, 5, 7, 8, 3, 4],
    [4, 9, 7, 8, 1, 3, 1, 7, 7, 2, 1, 4, 6, 1, 3, 4, 7, 1, 9, 1, 7, 8, 9, 7, 9, 6, 0, 8, 5, 3],
    [6, 2, 2, 2, 5, 7, 5, 1, 6, 6, 3, 2, 9, 6, 7, 2, 1, 3, 2, 5, 6, 2, 2, 2, 9, 8, 5, 0, 1, 4],
    [9, 5, 4, 3, 6, 3, 7, 4, 3, 1, 7, 9, 1, 9, 2, 9, 4, 6, 9, 1, 1, 9, 7, 7, 2, 6, 6, 1, 0, 8],
]

matchup_matrix_15 = [
    [0, 5, 8, 3, 7, 2, 1, 4, 6, 9, 7, 4, 6, 3, 1, 5, 2, 8, 1, 3, 4, 9, 7, 2, 6, 8, 3, 5, 1, 4],
    [5, 0, 7, 4, 6, 9, 8, 3, 1, 2, 8, 5, 7, 1, 4, 6, 9, 2, 5, 7, 3, 1, 6, 5, 7, 1, 4, 6, 3, 2],
    [8, 7, 0, 6, 8, 4, 9, 2, 5, 7, 3, 1, 6, 4, 5, 1, 3, 7, 6, 4, 9, 2, 5, 7, 3, 2, 6, 4, 1, 8],
    [3, 4, 6, 0, 5, 7, 2, 9, 1, 8, 4, 6, 9, 5, 7, 8, 2, 1, 3, 6, 5, 7, 1, 4, 3, 6, 9, 2, 8, 1],
    [7, 6, 8, 5, 0, 3, 6, 7, 2, 4, 6, 1, 5, 8, 2, 3, 4, 6, 7, 5, 2, 8, 1, 9, 5, 7, 3, 1, 6, 4],
    [2, 9, 4, 7, 3, 0, 6, 8, 9, 5, 7, 2, 8, 1, 3, 6, 5, 1, 2, 9, 8, 9, 5, 7, 4, 6, 1, 3, 2, 7],
    [1, 8, 9, 2, 6, 6, 0, 3, 7, 1, 6, 9, 4, 2, 6, 1, 7, 3, 6, 2, 9, 5, 1, 3, 8, 9, 7, 4, 6, 5],
    [4, 3, 2, 9, 7, 8, 3, 0, 4, 7, 1, 5, 2, 9, 1, 4, 6, 5, 8, 3, 7, 1, 8, 9, 2, 3, 4, 7, 6, 1],
    [6, 1, 5, 1, 2, 9, 7, 4, 0, 6, 3, 1, 3, 7, 9, 2, 6, 8, 9, 7, 4, 1, 5, 8, 3, 4, 6, 2, 9, 1],
    [9, 2, 7, 8, 4, 5, 1, 7, 6, 0, 9, 3, 1, 8, 2, 7, 1, 3, 5, 8, 4, 6, 9, 7, 2, 5, 1, 4, 3, 6],
    [7, 8, 3, 4, 6, 7, 6, 1, 3, 9, 0, 6, 5, 4, 6, 5, 3, 7, 9, 2, 1, 4, 3, 6, 2, 8, 1, 5, 7, 9],
    [4, 5, 1, 6, 1, 2, 9, 5, 1, 3, 6, 0, 7, 3, 1, 9, 5, 8, 4, 2, 6, 1, 3, 2, 6, 9, 7, 4, 5, 8],
    [6, 7, 6, 9, 5, 8, 4, 2, 9, 1, 5, 7, 0, 6, 5, 8, 9, 7, 3, 1, 2, 3, 4, 1, 5, 6, 0, 8, 2, 9],
    [3, 1, 4, 5, 8, 1, 2, 9, 1, 8, 4, 3, 6, 0, 8, 1, 4, 6, 5, 9, 7, 5, 8, 2, 7, 1, 3, 6, 4, 9],
    [1, 4, 5, 7, 2, 3, 6, 1, 3, 2, 6, 1, 5, 8, 0, 4, 5, 7, 1, 9, 2, 6, 1, 3, 9, 2, 8, 7, 4, 5],
    [5, 6, 1, 8, 3, 6, 1, 4, 6, 7, 4, 6, 8, 1, 4, 0, 9, 2, 3, 1, 5, 2, 8, 3, 1, 6, 7, 9, 5, 2],
    [2, 9, 3, 2, 4, 5, 7, 6, 5, 1, 6, 5, 9, 4, 5, 9, 0, 3, 6, 1, 8, 7, 2, 8, 1, 7, 4, 2, 3, 6],
    [8, 2, 7, 1, 6, 1, 3, 5, 8, 3, 7, 8, 7, 6, 7, 2, 3, 0, 6, 5, 1, 9, 4, 6, 9, 4, 5, 1, 3, 2],
    [1, 5, 6, 3, 7, 2, 6, 8, 9, 5, 9, 4, 3, 5, 1, 3, 6, 6, 0, 8, 7, 1, 4, 2, 5, 7, 1, 4, 6, 9],
    [4, 7, 4, 6, 5, 9, 2, 3, 7, 8, 2, 2, 6, 9, 9, 1, 1, 5, 8, 0, 3, 6, 5, 8, 3, 6, 1, 9, 7, 4],
    [9, 3, 9, 5, 2, 8, 9, 7, 4, 4, 1, 6, 1, 7, 2, 5, 8, 1, 7, 3, 0, 6, 1, 4, 6, 2, 3, 9, 5, 8],
    [6, 1, 2, 7, 8, 9, 5, 1, 6, 1, 4, 1, 3, 5, 6, 2, 7, 9, 1, 6, 6, 0, 8, 3, 4, 5, 7, 2, 9, 1],
    [7, 6, 5, 1, 1, 5, 1, 8, 9, 3, 3, 4, 4, 8, 1, 8, 2, 4, 4, 5, 1, 8, 0, 9, 5, 2, 7, 6, 1, 3],
    [2, 5, 7, 4, 9, 7, 3, 2, 7, 6, 6, 1, 5, 2, 3, 3, 8, 6, 2, 8, 4, 3, 9, 0, 6, 7, 1, 4, 5, 8],
    [8, 7, 3, 3, 5, 4, 8, 7, 1, 9, 9, 5, 7, 5, 6, 1, 1, 9, 5, 3, 6, 4, 4, 6, 0, 2, 8, 7, 1, 3],
    [1, 1, 2, 6, 7, 6, 9, 1, 3, 4, 4, 6, 1, 7, 2, 7, 7, 4, 7, 6, 2, 5, 5, 7, 2, 0, 8, 1, 9, 4],
    [9, 4, 6, 9, 3, 1, 7, 3, 4, 5, 5, 2, 3, 4, 3, 4, 6, 5, 1, 2, 3, 7, 7, 1, 8, 2, 0, 9, 6, 5],
    [5, 6, 1, 2, 7, 3, 4, 4, 6, 1, 1, 3, 6, 6, 6, 2, 1, 8, 4, 3, 9, 2, 6, 4, 7, 8, 9, 0, 5, 1],
    [7, 3, 8, 8, 3, 2, 6, 7, 2, 4, 9, 9, 4, 1, 1, 6, 3, 3, 6, 7, 5, 9, 1, 5, 1, 7, 6, 5, 0, 2],
    [3, 2, 1, 1, 1, 7, 5, 6, 9, 6, 2, 1, 2, 8, 9, 9, 6, 6, 9, 8, 8, 1, 3, 8, 3, 1, 1, 1, 2, 0],
]

import random



def select_champions(champion_data, synergy_matrix, selected_champions=None):
    selected_champions = selected_champions or [random.choice([champ for champ in champion_data if champ["note"] == "S"])]

    while len(selected_champions) < 5:
        last_selected = selected_champions[-1]
        synergy_row = synergy_matrix[champion_data.index(last_selected)]
        remaining_champions = [champ for champ in champion_data if champ not in selected_champions and champ["role"] not in [selected["role"] for selected in selected_champions]]

        if not remaining_champions:
            print("Aucun champion disponible respectant les règles. Arrêt de la sélection.")
            break

        next_champion = max(remaining_champions, key=lambda champ: synergy_row[champion_data.index(champ)])
        selected_champions.append(next_champion)

    return selected_champions


def visualize_graph(matrix, labels, selected_champions=None):
    G = nx.Graph()

    for i in range(len(labels)):
        G.add_node(labels[i])

    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            G.add_edge(labels[i], labels[j], weight=matrix[i][j])

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, font_size=8)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Ajout de la couleur verte pour les champions sélectionnés
    if selected_champions:
        node_colors = ['green' if champ["name"] in selected_champions else 'skyblue' for champ in champion_data]
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, font_size=8, node_color=node_colors)

    plt.show()

# Exemple d'utilisation

result = select_champions(champion_data, synergy_matrix_15)
for champ in result:
    print(f"{champ['name']} - Note: {champ['note']}")

# Visualiser le graphe de synergie avec les champions sélectionnés en vert
visualize_graph(synergy_matrix_15, [champ["name"] for champ in champion_data], selected_champions=[champ["name"] for champ in result])


#afficher que les champion selectioné 

def visualize_selected_champions(champion_data, synergy_matrix, selected_champions):
    num_selected = len(selected_champions)

    fig, axes = plt.subplots(1, num_selected, figsize=(5*num_selected, 5))

    for i, champion in enumerate(selected_champions):
        G = nx.Graph()
        champion_name = champion["name"]

        for champ in selected_champions:
            if champ != champion:
                G.add_edge(champion_name, champ["name"], weight=synergy_matrix[champion_data.index(champion)][champion_data.index(champ)])

        pos = nx.spring_layout(G)

        # Nodes
        nx.draw_networkx_nodes(G, pos, ax=axes[i], node_size=700, node_color='skyblue')

        # Edges
        nx.draw_networkx_edges(G, pos, ax=axes[i], width=2)

        # Labels
        nx.draw_networkx_labels(G, pos, ax=axes[i], font_size=10, font_color='black')

        # Edge labels
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=axes[i])

        # Set title for the subplot
        axes[i].set_title(f'{champion_name}\nRole: {champion["role"]}\nStyle: {champion["style"]}', fontsize=12)

    plt.show()

# Exemple d'utilisation
#result = select_champions(champion_data, synergy_matrix_15)
visualize_selected_champions(champion_data, synergy_matrix_15, result)

# chemin de picks 
def visualize_selected_path(champion_data, synergy_matrix, selected_champions):
    G = nx.Graph()

    for i, champion in enumerate(selected_champions):
        G.add_node(champion["name"])
        if i > 0:
            # Ajouter une arête entre les champions successifs avec le poids de synergie correspondant
            G.add_edge(selected_champions[i-1]["name"], champion["name"], weight=synergy_matrix[champion_data.index(selected_champions[i-1])][champion_data.index(champion)])

    pos = nx.spring_layout(G)

    # Nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')

    # Edges
    nx.draw_networkx_edges(G, pos, width=2)

    # Labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

    # Edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Chemin des champions sélectionnés avec synergie")
    plt.show()

# Exemple d'utilisation
#result = select_champions(champion_data, synergy_matrix_15)
visualize_selected_path(champion_data, synergy_matrix_15, result)