import networkx as nx
import Equipe
import matplotlib.pyplot as plt


class ClasseDraft:
    def __init__(self,graph):
        self.graphe = graph
        self.convertir_donnees_graphe_str_to_float()
        self.poids_blue = [-1.88737914e-15,4.52493244e+00,4.72834057e+00,9.99555218e-01,-3.87792318e-15]
        self.poids_red = [9.15933995e-16,3.48769222e+00,3.72504135e+00,1.29504376e+00,1.48420521e-15]
        self.blue = Equipe.Equipe(graph,self.poids_blue)
        self.red = Equipe.Equipe(graph,self.poids_red)
        self.tours = ["b","r","b","r","b","r","b","r","r","b","b","r","r","b","r","b","r","b","b","r"]
        self.letour = 0


    def lancer_draft(self) : 
        for i in range(len(self.tours)) : 
            if self.tours[i] == "b" :
                champion = self.blue.choix_pick_ban(self.blue.tours[int(i/2)])
                self.blue.action(champion,self.blue.tours[int(i/2)])
                self.red.action_adverse(champion,self.blue.tours[int(i/2)])
            else : 
                champion = self.red.choix_pick_ban(self.red.tours[int(i/2)])
                self.red.action(champion,self.red.tours[int(i/2)])
                self.blue.action_adverse(champion,self.red.tours[int(i/2)])
    
    def lancer_un_tour_draft(self) :
        if self.tours[self.letour] == "b" :
            champion = self.blue.choix_pick_ban(self.blue.tours[int(i/2)])
            self.blue.action(champion,self.blue.tours[int(self.letour/2)])
            self.red.action_adverse(champion,self.blue.tours[int(self.letour/2)])
        else : 
            champion = self.red.choix_pick_ban(self.red.tours[int(i/2)])
            self.red.action(champion,self.red.tours[int(self.letour/2)])
            self.blue.action_adverse(champion,self.red.tours[int(self.letour/2)])
        self.letour = self.letour + 1

    #Partie de fonction pour l'envirenement IA 
    def lancer_un_tour_draft_step(self,champion) :
        if self.tours[self.letour] == "b" :
            self.blue.action(champion,self.blue.tours[int(self.letour/2)])
            self.red.action_adverse(champion,self.blue.tours[int(self.letour/2)])
        else : 
            self.red.action(champion,self.red.tours[int(self.letour/2)])
            self.blue.action_adverse(champion,self.red.tours[int(self.letour/2)])
        
    def reward_action(self) : 
        if self.tours[self.letour] == "b" :
            return self.blue.stablite_champion_picks()
        else : 
            return self.red.stablite_champion_picks()
    def get_observation(self) : 
        return self.blue.bans,self.blue.picks,self.red.bans, self.red.picks
    

    def afficher_resultat(self) : 
        print(self.blue.bans,"\t",self.red.bans)
        print("\t\t -> : ",self.blue.picks[0],"\t",self.red.picks[0])
        print("\t\t -> : ",self.blue.picks[1],"\t",self.red.picks[1])
        print("\t\t -> : ",self.blue.picks[2],"\t",self.red.picks[2])
        print("\n")
        print("\t\t -> : ",self.blue.picks[3],"\t",self.red.picks[3])
        print("\t\t -> : ",self.blue.picks[4],"\t",self.red.picks[4])
        print("=====================")
        print("Score blue : ",self.blue.score_draft())
        print("Score red : ",self.red.score_draft())

    def convertir_donnees_graphe_str_to_float(self) : 
        for noeud in self.graphe.nodes:
            for cle, valeur in self.graphe.nodes[noeud].items():
                try:    
                    if cle != "Lane" and cle != "Classe" :
                        valeur_numerique = float(valeur.rstrip('%'))
                        self.graphe.nodes[noeud][cle] = valeur_numerique
                except ValueError:
                    pass
        for arrete in self.graphe.edges:
            for cle, valeur in self.graphe.edges[arrete].items():
                try:
                    valeur_numerique = float(valeur)
                    self.graphe.edges[arrete][cle] = valeur_numerique
                except ValueError:
                    pass
    
    def afficher_noeuds_selectionnes(self):
        pos = nx.spring_layout(self.graphe)
        # Filtrer les nœuds et les arêtes
        subgraph_nodes = set(self.blue.picks + self.red.picks)
        subgraph_edges = [(u, v) for u, v in self.graphe.edges() if u in subgraph_nodes and v in subgraph_nodes]
        # Créer un sous-graphe avec les nœuds et les arêtes filtrés
        subgraph = graphe.subgraph(subgraph_nodes).copy()
        subgraph.add_edges_from(subgraph_edges)
        # Afficher les nœuds du côté bleu en bleu
        nx.draw_networkx_nodes(subgraph, pos, nodelist=self.blue.picks, node_color='blue', label="Blue Team")
        # Afficher les nœuds du côté rouge en rouge
        nx.draw_networkx_nodes(subgraph, pos, nodelist=self.red.picks, node_color='red', label="Red Team")
        # Afficher les arêtes
        nx.draw_networkx_edges(subgraph, pos)
        # Ajouter les labels
        nx.draw_networkx_labels(subgraph, pos)
        # Afficher la légende
        plt.legend()
        # Afficher le graphe
        plt.show()

    def champion_disponible(self) : 
        champion_dispo = []
        for champion in self.graphe : 
            if champion not in self.blue.total_picks_bans : 
                champion_dispo.append(champion)
        return champion_dispo


#afficher le score de la draft 


    