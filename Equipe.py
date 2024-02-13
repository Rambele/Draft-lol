import random
import math
class Equipe:
    def __init__(self, graphe,poids_opti):
        self.score_to_metrique(graphe) # changé le score donnée par metasrc
        self.graphe_base = graphe
        self.tours = [0,0,0,1,1,1,0,0,1,1] #0 pour ban , 1 pour pick 
        self.picks = []
        self.bans = []
        self.roles = []
        self.type = [] # pour le type de draft plus tard 
        self.picks_adverse = []
        self.bans_advers = []
        self.roles_advers = []
        self.type_advers = []
        self.graphe = graphe.copy()
        self.graphe_adverse = graphe.copy()
        self.total_picks_bans = []
        self.poids_opti = poids_opti

    def reset_equipe(self) :
        self.picks = []
        self.bans = []
        self.roles = []
        self.type = [] # pour le type de draft plus tard 
        self.picks_adverse = []
        self.bans_advers = []
        self.roles_advers = []
        self.type_advers = []
        self.graphe = self.graphe_base.copy()
        self.graphe_adverse = self.graphe_base.copy()
        self.total_picks_bans = []

    def pick(self,champion) : 
        self.picks.append(champion)
        self.roles.append(self.graphe.nodes[champion]["Lane"])
        self.total_picks_bans.append(champion)
        # augmenté les poids des sy et supp les mt,cn
        sy = self.get_champion_sy(champion,self.graphe)
        cn = self.get_champion_cn(champion,self.graphe)
        mt = self.get_champion_mt(champion,self.graphe)
        for voisin in sy:
            label_actuel = self.graphe[champion][voisin]['label']
            self.graphe[champion][voisin]['label'] = label_actuel*2
        for voisin in cn:
            self.graphe.remove_edge(champion, voisin)
        for voisin in mt:
            self.graphe.remove_edge(champion, voisin)
        # cest l'inverse de coté adverse du graphe 
        sy = self.get_champion_sy(champion,self.graphe_adverse)
        cn = self.get_champion_cn(champion,self.graphe_adverse)
        mt = self.get_champion_mt(champion,self.graphe_adverse)
        for voisin in cn:
            label_actuel = self.graphe_adverse[champion][voisin]['label']
            self.graphe_adverse[champion][voisin]['label'] = label_actuel*2
        for voisin in mt:
            label_actuel = self.graphe_adverse[champion][voisin]['label']
            self.graphe_adverse[champion][voisin]['label'] = label_actuel*2
        for voisin in sy:
            self.graphe_adverse.remove_edge(champion, voisin)

        
    def ban(self,champion) : 
        self.bans.append(champion)
        self.total_picks_bans.append(champion)
        self.graphe.remove_node(champion)
        self.graphe_adverse.remove_node(champion)
    
    def action(self,champion,pick_ban) : 
        self.pick(champion) if pick_ban else self.ban(champion)

    def pick_adverse(self,champion) : 

        self.picks_adverse.append(champion)
        self.roles_advers.append(self.graphe.nodes[champion]["Lane"])
        self.total_picks_bans.append(champion)
        # augmenté les poids des sy et supp les mt,cn
        sy = self.get_champion_sy(champion,self.graphe_adverse)
        cn = self.get_champion_cn(champion,self.graphe_adverse)
        mt = self.get_champion_mt(champion,self.graphe_adverse)
        for voisin in sy:
            label_actuel = self.graphe_adverse[champion][voisin]['label']
            self.graphe_adverse[champion][voisin]['label'] = label_actuel*2
        for voisin in cn:
            self.graphe_adverse.remove_edge(champion, voisin)
        for voisin in mt:
            self.graphe_adverse.remove_edge(champion, voisin)
        # cest l'inverse de coté adverse du graphe 
        sy = self.get_champion_sy(champion,self.graphe)
        cn = self.get_champion_cn(champion,self.graphe)
        mt = self.get_champion_mt(champion,self.graphe)
        for voisin in cn:
            label_actuel = self.graphe[champion][voisin]['label']
            self.graphe[champion][voisin]['label'] = label_actuel*2
        for voisin in mt:
            label_actuel = self.graphe[champion][voisin]['label']
            self.graphe[champion][voisin]['label'] = label_actuel*2
        for voisin in sy:
            self.graphe.remove_edge(champion, voisin)
    
    def ban_adverse(self,champion)  :

        self.bans_advers.append(champion)
        self.total_picks_bans.append(champion)
        self.graphe.remove_node(champion)
        self.graphe_adverse.remove_node(champion)
    
    def action_adverse(self,champion,pick_ban) : 
        self.pick_adverse(champion) if pick_ban else self.ban_adverse(champion)

    def choisir_pick(self) : 
        champion_choisi = self.champion_plus_stable(self.graphe,self.roles)
        return champion_choisi
    
    def choisir_ban(self) :
        champion_choisi = self.champion_plus_stable(self.graphe_adverse,self.roles_advers)
        return champion_choisi
    
    def choix_pick_ban(self,pick_ban) :
        choix = self.choisir_pick() if pick_ban else self.choisir_ban()
        return choix
    
    def calculer_metrique_composite_champion(self,champion,graphe, alpha=1, beta=1, gamma=1, delta=1, epsilon=1):
        # Normaliser les valeurs (par exemple, convertir le win_rate de pourcentage à décimal)
        win_rate = graphe.nodes[champion]["Win"]
        pick_rate = graphe.nodes[champion]["Pick"]
        ban_rate = graphe.nodes[champion]["Ban"]
        kda = graphe.nodes[champion]["KDA"]
        nombre_de_games = graphe.nodes[champion]["Games"]
    
        # Calculer le logarithme du nombre de games
        log_nombre_de_games = math.log(nombre_de_games ) 
        log_base_1 = math.log(1.3) #1.27
        log_nombre_de_games = log_nombre_de_games/log_base_1
        kda = kda 
        # Appliquer les poids pour chaque paramètre
        #metrique_composite = alpha * win_rate + beta * (100 - ban_rate) + gamma * pick_rate + delta * kda + epsilon * log_nombre_de_games
        metrique_composite = (alpha * win_rate) / (gamma * pick_rate) + (beta * ban_rate) + (delta * kda) + (epsilon * log_nombre_de_games)
        metrique_composite = (win_rate / log_nombre_de_games ) + ban_rate*0.075 + kda*0.01 + pick_rate*0.0001
        return metrique_composite*self.classe_score(champion,graphe)

    def classe_score(self,champion,graph) :
        score = 0
        for classe in graph.nodes[champion]["Classe"] :
            if  classe=="Marksman" :
                score +=1
            elif classe=="Support" : 
                score +=1
            elif classe=="Tank" : 
                score +=0.8 
            elif classe=="Fighter" : 
                score +=0.9
            elif classe=="Mage" : 
                score +=1.1
            else : #assassin
                score+=0.7
        return score/len(graph.nodes[champion]["Classe"])

    def poid_arret(self,championA,championB,graphe) :
        if graphe.has_edge(championA, championB):
            edge_attributes = graphe.get_edge_data(championA, championB)
            label = edge_attributes['label']  
            return label
        else:
            return 0
    def get_champion_sy(slef,champion,graphe) :
        synergy_champion = [neighbor for neighbor in graphe.successors(champion) if graphe[champion][neighbor]['type'] == 'Synergy']
        return  synergy_champion
    def get_champion_cn(slef,champion,graphe) :
        counter_champion = [neighbor for neighbor in graphe.successors(champion) if graphe[champion][neighbor]['type'] == 'Counter']
        return counter_champion
    def get_champion_mt(self,champion,graphe) :
        matchup_champion = [neighbor for neighbor in graphe.successors(champion) if graphe[champion][neighbor]['type'] == 'Matchup']
        return matchup_champion
    
    def champion_counters_score(self,championA,graphe) :
        list = self.get_champion_cn(championA,graphe)
        sum_score_final = 0
        score_final = 0
        for championB in list :
            score = graphe.nodes[championB]["Score"]
            win = graphe.nodes[championB]["Win"]
            poid = self.poid_arret(championA,championB,graphe) * -1 
            graphe.nodes[championB]["Win"] = graphe.nodes[championB]["Win"]  + poid 
            graphe.nodes[championB]["Score"] = self.calculer_metrique_composite_champion(championB,graphe)
            sum_score_final = sum_score_final + self.calculer_metrique_composite_champion(championB,graphe)
            graphe.nodes[championB]["Win"] =  win
            graphe.nodes[championB]["Score"] = score
        score_final = sum_score_final/len(list) if len(list) != 0 else 1
        return score_final
    
    def champion_matchups_score(self,championA,graphe) :
        list = self.get_champion_mt(championA,graphe)
        sum_score_final = 0
        score_final = 0
        for championB in list :
            score = graphe.nodes[championB]["Score"]
            win = graphe.nodes[championB]["Win"]
            poid = self.poid_arret(championA,championB,graphe) 
            graphe.nodes[championB]["Win"] = graphe.nodes[championB]["Win"]  - poid 
            graphe.nodes[championB]["Score"] = self.calculer_metrique_composite_champion(championB,graphe)
            sum_score_final = sum_score_final + self.calculer_metrique_composite_champion(championB,graphe)
            graphe.nodes[championB]["Win"] =  win
            graphe.nodes[championB]["Score"] = score
        score_final = sum_score_final/len(list) if len(list) != 0 else 1
        return score_final
    
    def champion_synrgys_score(self,championA,graphe) :
        list = self.get_champion_mt(championA,graphe)
        sum_score_final = 0
        score_final = 0
        for championB in list :
            score = graphe.nodes[championB]["Score"]
            win = graphe.nodes[championB]["Win"]
            poid = self.poid_arret(championA,championB,graphe) 
            graphe.nodes[championB]["Win"] = graphe.nodes[championB]["Win"]  + poid 
            graphe.nodes[championB]["Score"] = self.calculer_metrique_composite_champion(championB,graphe)
            sum_score_final = sum_score_final + self.calculer_metrique_composite_champion(championB,graphe)
            graphe.nodes[championB]["Win"] =  win
            graphe.nodes[championB]["Score"] = score
        score_final = sum_score_final/len(list) if len(list) != 0 else 1
        return score_final
    
    def score_to_metrique(self,graphe):
        for champion in graphe :
             graphe.nodes[champion]["Score"] = self.calculer_metrique_composite_champion(champion,graphe)
    
    def champion_cn_mt_sy_score(self,champion,graphe, alpha=1, beta=1, gamma=1, delta=1, epsilon=1) :
        a = self.champion_counters_score(champion,graphe)
        b = self.champion_synrgys_score(champion,graphe)
        c = self.champion_matchups_score(champion,graphe)
        return  alpha*graphe.nodes[champion]["Score"]/((beta*c+gamma*b)/2-(delta*a)) + epsilon
    
    def champion_plus_stable(self,graphe,list_roles) :
        best = ''
        score = -10000
        for champion in graphe :

            if score < self.champion_cn_mt_sy_score(champion,graphe,*self.poids_opti) and champion not in self.total_picks_bans and graphe.nodes[champion]['Lane'] not in list_roles:
                score = self.champion_cn_mt_sy_score(champion,graphe,*self.poids_opti)
                best = champion
        return best
    
    def score_draft(self) :
        score = 0
        for champion in self.picks :
            score+=self.calculer_metrique_composite_champion(champion,self.graphe)
        return score/len(self.picks)
    
    #Partie pour l'envirenement IA 

    def stablite_champion_picks(self) : 
        reward = 0
        for champion in self.picks :
            reward = reward + self.champion_cn_mt_sy_score(champion,self.graphe,*self.poids_opti)
        return reward