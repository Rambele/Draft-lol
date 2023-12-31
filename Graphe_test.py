import networkx as nx
import matplotlib.pyplot as plt

# Créer un multigraphe
multigraphe = nx.MultiGraph()

# Ajouter des sommets
multigraphe.add_node('A')
multigraphe.add_node('B')

# Ajouter plusieurs arêtes entre les mêmes sommets
multigraphe.add_edge('A', 'B', weight=1)
multigraphe.add_edge('A', 'B', weight=2)

# Dessiner le multigraphe
pos = nx.spring_layout(multigraphe)
nx.draw(multigraphe, pos, with_labels=True, font_size=8, font_color='black', font_weight='bold', node_size=500, node_color='skyblue', edge_color='gray', linewidths=0.5)
plt.show()
