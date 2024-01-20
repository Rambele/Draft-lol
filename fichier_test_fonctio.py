from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import networkx as nx

graphe = nx.read_graphml("./mon_graphe.graphml")
# Une fois le graphe contruit je doit cree des fonction pour repondre a des question apres quoi etablir des heuristique 

# le meilleur champion a pick actuelement instant T


def best_stat_score_champion(graphe) : 
    best_score = 0
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


#calculer le champion qui se fait le moins counter possible 


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
    print("Meilleur champ en terme de counter : ", best_champ)
    print("Le score : ", best_counter_score)

def champion_counters_score(champion,graphe) :
    list = get_champion_cn(champion,graphe)
    sum_score_final = 0
    score_final = 0
    for a in list :
        data = graphe.nodes[a]
        score = float(data.get('Score', 0))
        poid = recupere_poid(champion,a,graphe) * -1 
        score_final = score + poid
        sum_score_final = sum_score_final + score_final
    data = graphe.nodes[champion]
    score = float(data.get('Score', 0))
    score_final = score - sum_score_final/len(list) if len(list) != 0 else score

    return score_final


def champion_matchups_score(champion,graphe) : 
    list = get_champion_mt(champion,graphe)
    sum_score_final = 0
    score_final = 0
    for a in list :
        data = graphe.nodes[a]
        score = float(data.get('Score', 0))
        poid = recupere_poid(champion,a,graphe)  
        score_final = score - poid
        sum_score_final = sum_score_final + score_final
    data = graphe.nodes[champion]
    score = float(data.get('Score', 0))
    score_final = score - sum_score_final/len(list) if len(list) != 0 else score
    return score_final
    
def champion_synrgys_score(champion,graphe) : 
    list = get_champion_sy(champion,graphe)
    sum_score_final = 0
    score_final = 0
    for a in list :
        data = graphe.nodes[a]
        score = float(data.get('Score', 0))
        poid = recupere_poid(champion,a,graphe)  
        score_final = score + poid
        sum_score_final = sum_score_final + score_final
    data = graphe.nodes[champion]
    score = float(data.get('Score', 0))
    score_final = (score + sum_score_final/len(list))/2 if len(list) != 0 else score
    return score_final

def calculer_score_globale_champion(champion,graphe) :
    a = champion_counters_score(champion,graphe)
    b = champion_synrgys_score(champion,graphe)
    c = champion_matchups_score(champion,graphe)
    data = graphe.nodes[champion]
    score = float(data.get('Score', 0))
    w1 = 0.4
    w2 = 0.2
    w3 = 0.2
    w4 = 0.2
    return a * w1 + b * w2 + c * w3 + score * w4

def champion_plus_stable(graphe,blue_pick,red_pick,blue_roles) :
    best = ''
    score = 0 
    for champion in graphe :

        if score < calculer_score_globale_champion(champion,graphe) and champion not in blue_pick and champion not in red_pick and graphe.nodes[champion]['Lane'] not in blue_roles:
            score = calculer_score_globale_champion(champion,graphe)
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
        score = float(data.get('Score', 0))
        graphe.nodes[voisin]['Score'] = str(label_actuel * 5 + score)
    picks_list.append(champion)
    data =data = graphe.nodes[champion]
    roles_list.append(data.get('Lane'))
    






