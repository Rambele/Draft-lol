from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import networkx as nx
from scipy.optimize import minimize

graphe = nx.read_gml('mon_graphe.gml')
pd = [-4.44089210e-15,1.58671718e+00,1.87418490e+00,1.02144791e+00,-4.86160690e-15]
pd = [3.05311332e-15,1.93712176e+00,1.61943703e+00,1.03381622e+00,4.19154530e-15]
pd = [-4.44089210e-16,3.68251342e+00,2.12309074e+00,0.00000000e+00,0.00000000e+00]#udyr
pd = [9.15933995e-16,3.48769222e+00,3.72504135e+00,1.29504376e+00,1.48420521e-15]
pd = [2.22044605e-16,1.63475423e+00,1.67052905e+00,1.02661625e+00,0.00000000e+00]
pd = [-1.88737914e-15,4.52493244e+00,4.72834057e+00,9.99555218e-01,-3.87792318e-15]
#pd = [-2.22044605e-16,1.27904409e+00,1.15715135e+00,1.00750185e+00,0.00000000e+00]
# Une fois le graphe contruit je doit cree des fonction pour repondre a des question apres quoi etablir des heuristique 

# le meilleur champion a pick actuelement instant T


def best_stat_score_champion(graphe) : 
    best_score = -1000
    championN = ''
    for champion in graphe:
        
        data = graphe.nodes[champion]
        score = float(data.get('Score', 0))
        if best_score < score :
            best_score = score
            championN = champion
    return championN


def recupere_poid(championA,championB,graphe) :
    # Supposons que 'champion_source' et 'champion_target' soient les noms de vos champions connectés

    # Vérifiez si l'arête existe entre ces deux champions
    if graphe.has_edge(championA, championB):
     # Obtenez le dictionnaire des attributs de cette arête
        edge_attributes = graphe.get_edge_data(championA, championB)
    
        # Obtenez le label ou le poids (selon la structure de votre graphe)
        label = edge_attributes['label']  # Remplacez 'label' par le nom de votre attribut
        
        label = float(label)
        return label
        
    else:
        return 0


def calcule_stabilite_champion(champion,graphe) : 
    return graphe + champion 

def get_champion_sy(champion,graphe) :
    synergy_champion = [neighbor for neighbor in graphe.successors(champion) if graphe[champion][neighbor]['type'] == 'Synergy']
    return  synergy_champion
def get_champion_cn(champion,graphe) :
    counter_champion = [neighbor for neighbor in graphe.successors(champion) if graphe[champion][neighbor]['type'] == 'Counter']
    return counter_champion
def get_champion_mt(champion,graphe) :
    matchup_champion = [neighbor for neighbor in graphe.successors(champion) if graphe[champion][neighbor]['type'] == 'Matchup']
    return matchup_champion



def champion_moins_counter(graphe) :
    best_counter_score = 0
    best_champ = ''
    for c in graphe:
        list = get_champion_cn(c,graphe)
        sum_score_final = 0
        score_final = 0
        for a in list :
            data = graphe.nodes[a]
            score = float(data.get('Score', 0))
            poid = recupere_poid(c,a,graphe) * -1 
            score_final = score + poid
            sum_score_final = sum_score_final + score_final
        data = graphe.nodes[c]
        score = float(data.get('Score', 0))
        score_final = score - sum_score_final/len(list) if len(list)!= 0 else score
        if best_counter_score < score_final : 
            best_counter_score = score_final
            best_champ = c
    return best_champ

def champion_counters_score(champion,graphe) :
    list = get_champion_cn(champion,graphe)
    sum_score_final = 0
    score_final = 0
    for a in list :
        score = graphe.nodes[a]["Score"]
        win = graphe.nodes[a]["Win"]
        poid = recupere_poid(champion,a,graphe) * -1 
        graphe.nodes[a]["Win"] = str(float(graphe.nodes[a]["Win"].rstrip('%'))  + poid ) + "%"
        graphe.nodes[a]["Score"] = str(calculer_metrique_composite(a,graphe))
        sum_score_final = sum_score_final + calculer_metrique_composite(a,graphe)
        graphe.nodes[a]["Win"] =  win
        graphe.nodes[a]["Score"] = score

    score_final = sum_score_final/len(list) if len(list) != 0 else 1

    return score_final


def champion_matchups_score(champion,graphe) : 
    list = get_champion_mt(champion,graphe)
    sum_score_final = 0
    score_final = 0
    for a in list :
        score = graphe.nodes[a]["Score"]
        win = graphe.nodes[a]["Win"]
        poid = recupere_poid(champion,a,graphe)
        graphe.nodes[a]["Win"] = str(float(graphe.nodes[a]["Win"].rstrip('%'))  - poid ) + "%"
        graphe.nodes[a]["Score"] = str(calculer_metrique_composite(a,graphe))  
        sum_score_final = sum_score_final + recupere_poid(champion,a,graphe)
        graphe.nodes[a]["Win"] =  win
        graphe.nodes[a]["Score"] = score
    score_final = sum_score_final/len(list) if len(list) != 0 else 1
    return score_final
    
def champion_synrgys_score(champion,graphe) : 
    list = get_champion_sy(champion,graphe)
    sum_score_final = 0
    score_final = 0
    for a in list :
        score = graphe.nodes[a]["Score"]
        win = graphe.nodes[a]["Win"]
        poid = recupere_poid(champion,a,graphe)  
        graphe.nodes[a]["Win"] = str(float(graphe.nodes[a]["Win"].rstrip('%'))  + poid ) + "%"
        graphe.nodes[a]["Score"] = str(calculer_metrique_composite(a,graphe))
        sum_score_final = sum_score_final + calculer_metrique_composite(a,graphe)
        graphe.nodes[a]["Win"] =  win
        graphe.nodes[a]["Score"] = score
    score_final =  sum_score_final/len(list) if len(list) != 0 else 1
    return score_final

def calculer_score_globale_champion(champion,graphe, alpha=1, beta=1, gamma=1, delta=1, epsilon=1) :
    a = champion_counters_score(champion,graphe)
    b = champion_synrgys_score(champion,graphe)
    c = champion_matchups_score(champion,graphe)
    return  alpha*float(graphe.nodes[champion]["Score"])/((beta*c+gamma*b)/2-(delta*a)) + epsilon
    #return float(graphe.nodes[champion]["Score"])/(a*c/b)

def champion_plus_stable(graphe,blue_pick,red_pick,blue_roles,*pd) :
    best = ''
    score = -10000
    for champion in graphe :

        if score < calculer_score_globale_champion(champion,graphe,*pd) and champion not in blue_pick and champion not in red_pick and graphe.nodes[champion]['Lane'] not in blue_roles:
            score = calculer_score_globale_champion(champion,graphe,*pd)
            best = champion
    return best



# Quand je ban un champion je le supprime du graph , donc 
# automatiquement les calcule seront mise a jour 
# mais que faire pour les picks ????? 
# ===> sol : une fois les champion selectioné j'utilise plus le calcule stabilité de tout les voison 
# ====> mais uniquement pour les champions deja pick 


# pour le moment je ban les champion les plus stable 
def ban_champion(champion,graphe) : 
    graphe.remove_node(champion)

# pour le pick ca devenir compliqué un peu 
# je commance par un truc simple : si liste vide je pick le plus stable sinon  : 
#                                               je je fais le croisement entre les synrgy counter ...
def pick_champion(blue_picks,red_picks,graphe) : 
    if not blue_picks and not red_picks : 
        return champion_plus_stable(graphe)
    else :
        # trouvé le champion le plus table , sy , cn , mt 
        return 0
        
    # ici je test et cree la fonction pour me renvoiyé me meilleur champion par rapport a ce que j'ai pick

# vagues de changement 
def pick_champion(champion,graphe,picks_list,roles_list) : 
    sy = get_champion_sy(champion,graphe)
    cn = get_champion_cn(champion,graphe)
    mt = get_champion_mt(champion,graphe)
    for voisin in sy:
    # Vérifiez si l'arête a un attribut 'label' et si c'est une valeur numérique
        label_actuel = float(graphe[champion][voisin]['label'])
        
        data = graphe.nodes[voisin]
        win = float(data.get('Win').rstrip('%'))
        graphe.nodes[voisin]['Win'] = str(label_actuel  + win) + "%"
    picks_list.append(champion)
    data = graphe.nodes[champion]
    roles_list.append(data.get('Lane'))
    #supprimer les lien counter et match up  faudra dapater cette section pour les ban plus tard 
    for voisin in cn:
        graphe.remove_edge(champion, voisin)
    for voisin in mt:
        graphe.remove_edge(champion, voisin)

def pick_en_face(champion,graphe,list_picks) :
    sy = get_champion_sy(champion,graphe)
    cn = get_champion_cn(champion,graphe)
    mt = get_champion_mt(champion,graphe)
    for voisin in cn:
    # Vérifiez si l'arête a un attribut 'label' et si c'est une valeur numérique
        label_actuel = float(graphe[champion][voisin]['label'])*(-1)
        data = graphe.nodes[voisin]
        win = float(data.get('Win').rstrip('%'))
        graphe.nodes[voisin]['Win'] = str(label_actuel  + win) + "%"
    for voisin in mt:
    # Vérifiez si l'arête a un attribut 'label' et si c'est une valeur numérique
        label_actuel = float(graphe[champion][voisin]['label'])
        data = graphe.nodes[voisin]
        win = float(data.get('Win').rstrip('%'))
        graphe.nodes[voisin]['Win'] = str(win - label_actuel  ) + "%"
    list_picks.append(champion)
    for voisin in sy:
        graphe.remove_edge(champion, voisin)

def convertir_donnees_noeud(graphe) : 
    for noeud in graphe.nodes:
    # Parcourez toutes les données dans le nœud
        for cle, valeur in graphe.nodes[noeud].items():
            try:
                # Essayez de convertir la valeur en nombre
                valeur_numerique = float(valeur.rstrip('%'))
            
                # Remplacez la valeur dans le nœud par la version numérique
                graphe.nodes[noeud][cle] = valeur_numerique
            except ValueError:
                # En cas d'erreur de conversion, laissez la valeur inchangée
                pass


#convertir_donnees_noeud(graphe)

import math

def calculer_metrique_composite(champion,graphe, alpha=1, beta=1, gamma=1, delta=1, epsilon=1):
    # Normaliser les valeurs (par exemple, convertir le win_rate de pourcentage à décimal)
    win_rate = float(graphe.nodes[champion].get('Win').rstrip('%'))
    pick_rate = float(graphe.nodes[champion].get('Pick').rstrip('%'))
    ban_rate = float(graphe.nodes[champion].get('Ban').rstrip('%'))
    kda = float(graphe.nodes[champion].get('KDA'))
    nombre_de_games = float(graphe.nodes[champion].get('Games'))
    
    # Calculer le logarithme du nombre de games
    log_nombre_de_games = math.log(nombre_de_games ) 
    log_base_1 = math.log(1.3) #1.27
    log_nombre_de_games = log_nombre_de_games/log_base_1
    kda = kda 
    # Appliquer les poids pour chaque paramètre
    #metrique_composite = alpha * win_rate + beta * (100 - ban_rate) + gamma * pick_rate + delta * kda + epsilon * log_nombre_de_games
    metrique_composite = (alpha * win_rate) / (gamma * pick_rate) + (beta * ban_rate) + (delta * kda) + (epsilon * log_nombre_de_games)
    metrique_composite = (win_rate / log_nombre_de_games ) + ban_rate*0.075 + kda*0.01 + pick_rate*0.0001 
    return metrique_composite*classe_score(champion,graphe)

#je donne un score au classe de champion 
def classe_score(champion,graph) :
        score = 0
        for classe in graph.nodes[champion]["Classe"] :
            if  classe=="Marksman" :
                score +=0.90
            elif classe=="Support" : 
                score +=0.7
            elif classe=="Tank" : 
                score +=0.9
            elif classe=="Fighter" : 
                score +=1
            elif classe=="Mage" : 
                score +=1.1
            else : #assassin
                score+=0.80
        return score/len(graph.nodes[champion]["Classe"])
        

def score_to_metrique(graphe):
    for champion in graphe :
         graphe.nodes[champion]["Score"] = str(calculer_metrique_composite(champion,graphe))
    

# Calculer la métrique composite
score_to_metrique(graphe)
#print(graphe.nodes["Miss fortune"]["Score"])

blue_picks = []
red_picks = []
blue_roles = []
red_roles = []
#ban_champion("Teemo",graphe)
def afficher_meilleur_score_champ() : 
    print("score : ",best_stat_score_champion(graphe)," : ",graphe.nodes[best_stat_score_champion(graphe)]["Score"])

def afficher_meilleur_stable_champion() : 
    champ = champion_plus_stable(graphe,[],[],[],*pd)
    print("stable : ",champ," : ",calculer_score_globale_champion(champ,graphe))

def alpha_beta(graphe) : 
    grapheTest = graphe
    b_test_picks = []
    r_test_picks = []
    b_test_roles = []
    score = - 10000
    pick = ""
    for champion in graphe :
        grapheTest = graphe
        pick_champion(champion,grapheTest,b_test_picks,b_test_roles) 
        for champred1 in graphe :
            if champred1 != champion :
                for champred2 in graphe :
                    if champred2 != champred1 and champred2 != champion :
                        graphetest = grapheTest
                        pick_en_face(champred1,graphetest,r_test_picks)
                        pick_en_face(champred2,graphetest,r_test_picks)
                        a = calculer_score_globale_champion(champion,graphetest)
                        if score < a :
                            score = a
                            pick = champion
                        print(champion,"->",champred1,"->",champred2)
                            
    return pick




# Fonction-objectif pour maximiser le score de Varus
objective_function = lambda weights: calculer_score_globale_champion("Xin zhao", graphe, *weights)

# Contrainte pour s'assurer que les poids restent positifs
constraints = ({'type': 'ineq', 'fun': lambda weights: weights})

# Définition des poids initiaux
initial_weights = [1, 1, 1, 1, 1]

# Optimisation des poids
result = minimize(objective_function, initial_weights, constraints=constraints)

# Récupération des poids optimisés
optimized_weights = result.x

# Affichage des poids optimisés
print("Poids optimisés:", optimized_weights)
print("Champion stable : ",champion_plus_stable(graphe,[],[],[],*optimized_weights))
afficher_meilleur_stable_champion()
afficher_meilleur_score_champ()



