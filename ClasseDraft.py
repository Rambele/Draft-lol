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
        #pour l'agent 
        self.champion_indice_list = self.noeud_to_list_indice()

    def reset_draft(self): 
        self.letour = 0
        self.blue.reset_equipe()
        self.red.reset_equipe()
        self.champion_indice_list = self.noeud_to_list_indice()
        return self.get_observation()
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
        i = self.letour
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
        
    def noeud_to_list_indice(self):
        champion_indice_list = []
        indice = 0
        for chamion in self.graphe : 
            champion_indice_list.append(indice)
            indice+=1
        return champion_indice_list
    def champion_to_indice(self,champion):
        indice = 0
        for champ in self.graphe : 
            if champ == champion :
                return indice
            indice+=1
    def indice_to_champion(self,indice):
        i = 0
        for champ in self.graphe : 
            if i == indice :
                return champ
            i+=1
    def lancer_un_tour_draft_step(self,champion) :
        if self.tours[self.letour] == "b" :
            self.blue.action(champion,self.blue.tours[int(self.letour/2)])
            self.red.action_adverse(champion,self.blue.tours[int(self.letour/2)])
        else : 
            self.red.action(champion,self.red.tours[int(self.letour/2)])
            self.blue.action_adverse(champion,self.red.tours[int(self.letour/2)])
        #une fois le champion choisi que ca soit pick ou ban j'enleve l'indice de ce champion
        self.champion_indice_list.remove(self.champion_to_indice(champion))
        
    def reward_action(self) : 
        if self.tours[self.letour] == "b" :
            return self.blue.stablite_champion_picks() #- self.red.stablite_champion_picks()
        else : 
            return self.red.stablite_champion_picks() #- self.red.stablite_champion_picks()
    #recompense apres le tour de l'advecaire
    def reward_action_only_blue(self) :
        return self.blue.stablite_champion_picks()
    def get_observation(self) :
        bb = ["VIDE","VIDE","VIDE","VIDE","VIDE"] if len(self.blue.bans) == 0 else self.blue.bans.copy()
        bp = ["VIDE","VIDE","VIDE","VIDE","VIDE"] if len(self.blue.picks) == 0 else self.blue.picks.copy()
        rb = ["VIDE","VIDE","VIDE","VIDE","VIDE"] if len(self.red.bans) == 0 else self.red.bans.copy()
        rp = ["VIDE","VIDE","VIDE","VIDE","VIDE"] if len(self.red.picks) == 0 else self.red.picks.copy()
        for i in range(6) :
            if i > len(bb) :
                bb.append("VIDE")
            if i > len(bp) :
                bp.append("VIDE")
            if i > len(rb) :
                rb.append("VIDE")
            if i > len(rp) :
                rp.append("VIDE")
        all = bb+bp+rb+rp
        stat = []
        for i in all :
            if i == "VIDE" :
                stat.append(0)
            else :
                stat.append(self.trouve_champ_num(i))
        return stat
    def trouve_champ_num(self,champion):
        i=1
        for champ in self.graphe :
            if champ == champion :
                return i
            i+=1
    def cherche_champion_par_num(self,num) : 
        i=0
        for champion in self.champion_disponible() :
            if i == num :
                return champion
            i+=1

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
        subgraph = self.graphe.subgraph(subgraph_nodes).copy()
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

'''
graphe = nx.read_gml('mon_graphe.gml')
draft = ClasseDraft(graphe)
draft.blue.ban("Azir")
draft.red.ban("Draven")
stat = draft.get_observation()
print(stat)
print(len(stat))

'''