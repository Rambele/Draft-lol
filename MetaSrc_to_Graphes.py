import networkx as nx
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



# Spécifiez le chemin du pilote Chrome
chrome_driver_path = './webdriv/chromedriver'

# Configurez les options du navigateur pour un chargement sans interface graphique (headless)
chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument(f"webdriver.chrome.driver: {chrome_driver_path}")



# Initialisez le webdriver avec les options
driver = webdriver.Chrome(options=chrome_options)

# Remplacez l'URL par celui du site web que vous souhaitez scraper
url = 'https://www.metasrc.com/lol'
driver.get(url)

# Attendre que la page se charge complètement
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH ,'//*[@id="page-content"]/div/section/div')))

# Obtenez une liste de tous les champions présents sur la page
champion_elements = driver.find_elements(By.XPATH, '//*[@id="page-content"]/div/section/div/a')

# Créer un graphe pour stocker les champions leurs données et leurs relations avec les autre champion
graphe = nx.DiGraph()
# Dictionnaire pour stocker des données supplémentaires sur les sommets
champion_data = {}

links = []
list_champ_name = []
# Ajouter chaque champion comme un sommet au graphe
for champion_element in champion_elements:
    champion_name = champion_element.text.replace("'", "").capitalize()
    champion_name = champion_name.replace(".", "")
    if  champion_name == 'Jarvan iv' :
        champion_name = 'Jarvan'
    list_champ_name.append(champion_name)
    # hewi pose probleme je le supp du graph  
    graphe.add_node(champion_name)
    links.append(champion_element.get_attribute('href'))
    print(champion_name)

   
i = 0 # le i pour acceder au lien numero i champion i pendant la boucle
for champion in list_champ_name:

    driver.get(links[i])
    j=1

    # Récuperer les donnée de champion i 
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="splash-content"]/div[2]/span/div')))
    donnees = []
    donnee_champ_elements = driver.find_elements(By.XPATH, '//*[@id="splash-content"]/div[2]/span/div/span')
    for donnee_champ_element in donnee_champ_elements :
        info_text = donnee_champ_element.text.split("\n")
        info = info_text[1].strip()
        donnees.append(info)
    # A jouter le role de champion 
        
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="splash-content"]/div[1]/div/div/div/div[2]/div/h1/span[2]/span[1]')))
    role_champion_elements = driver.find_elements(By.XPATH, '//*[@id="splash-content"]/div[1]/div/div/div/div[2]/div/h1/span[2]/span[1]')
    for role_champion_element in role_champion_elements :
        info = role_champion_element.text
        donnees.append(info)
    # Clés fixes
    cles_fixes = ['Tier', 'Win', 'Role', 'Pick', 'Ban', 'Games', 'KDA', 'Score', 'Lane']
    # Créer un dictionnaire en utilisant les clés fixes
    donnees_champion = dict(zip(cles_fixes, donnees))
    print(donnees_champion)
    graphe.nodes[champion].update(donnees_champion)
    print("Donnée mise a jour \2" + champion)
    #=============FIN RECUPERATION============

    # ============== Récupiration des lien entre les champion ============================================

    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="page-content"]/div[6]/section/div/div/div')))
    # Obtenez les éléments des meilleurs bans
    meilleurs_bans_elements = driver.find_elements(By.XPATH, '//*[@id="page-content"]/div[6]/section/div/div/div/a')
    
    # best counters  : //*[@id="page-content"]/div[10]/section/div/div/div/a
    xpath = '//*[@id="page-content"]/div[10]/section/div/div/div/a' if graphe.nodes[champion]['Lane'] != 'Jungle ' else '//*[@id="page-content"]/div[13]/section/div/div/div/a'
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        # Si l'élément n'est pas présent, effectuez ici les actions que vous souhaitez en cas d'absence d'élément
        print("L'élément n'est pas présent. Passez à l'étape suivante.")
    else:  # ou break, selon votre logique
        best_counters_elements = driver.find_elements(By.XPATH, xpath)
    
        for best_counters_element in best_counters_elements:
            href = best_counters_element.get_attribute('href')
            if href.split('/')[-1].replace("-", " ").capitalize() in graphe :
          
                best_counters_name = href.split('/')[-1].replace("-", " ").capitalize()
            else :
                best_counters_name = href.split('/')[-2].replace("-", " ").capitalize()
    
            if best_counters_name == 'Build' :
                print('erreur build name apeare' + champion + '/' + best_counters_name )

            #graphe.add_node(meilleur_ban_name)
            graphe.add_edge(champion, best_counters_name, type='Counter', label=best_counters_element.text)
            j=j+1
    #==========================================================================================================
    # best synergies : //*[@id="page-content"]/div[7]/section/div/div/div/a
    try:
        if graphe.nodes[champion]['Lane'] != 'Jungle ' :
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="page-content"]/div[7]/section/div/div/div/a')))
        else :
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="page-content"]/div[7]/section/div/div/div/a | //*[@id="page-content"]/div[10]/section/div/div/div/a')))
    except TimeoutException:
        # Si l'élément n'est pas présent, effectuez ici les actions que vous souhaitez en cas d'absence d'élément
        print("L'élément n'est pas présent. Passez à l'étape suivante.")
    else:
        if graphe.nodes[champion]['Lane'] != 'Jungle ' : 
            best_synergy_elements = driver.find_elements(By.XPATH, '//*[@id="page-content"]/div[7]/section/div/div/div/a')
        else :
            best_synergy_elements = driver.find_elements(By.XPATH, '//*[@id="page-content"]/div[7]/section/div/div/div/a | //*[@id="page-content"]/div[10]/section/div/div/div/a')
        for best_synergy_element in best_synergy_elements:
            href = best_synergy_element.get_attribute('href')
            if href.split('/')[-1].replace("-", " ").capitalize() in graphe :
          
                best_synergy_name = href.split('/')[-1].replace("-", " ").capitalize()
            else :
                best_synergy_name = href.split('/')[-2].replace("-", " ").capitalize()
    
            if best_synergy_name == 'Build' :
                print('erreur build name apeare' + champion + '/' + best_synergy_name )

            #graphe.add_node(meilleur_ban_name)
            graphe.add_edge(champion, best_synergy_name, type='Synergy', label=best_synergy_element.text)
            graphe.add_edge(best_synergy_name, champion, type='Synergy', label=best_synergy_element.text)
            j=j+1
    #===========================================================================================================
    # best matchups : //*[@id="page-content"]/div[11]/section/div/div/div/a
    
    xpath = '//*[@id="page-content"]/div[11]/section/div/div/div/a' if graphe.nodes[champion]['Lane'] != 'Jungle ' else '//*[@id="page-content"]/div[14]/section/div/div/div/a'
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        # Si l'élément n'est pas présent, effectuez ici les actions que vous souhaitez en cas d'absence d'élément
        print("L'élément n'est pas présent. Passez à l'étape suivante.")
    else:
        best_matchup_elements = driver.find_elements(By.XPATH, xpath)
    
        for best_matchup_element in best_matchup_elements:
            href = best_matchup_element.get_attribute('href')
            if href.split('/')[-1].replace("-", " ").capitalize() in graphe :
          
                best_matchup_name = href.split('/')[-1].replace("-", " ").capitalize()
            else :
                best_matchup_name = href.split('/')[-2].replace("-", " ").capitalize()
    
            if best_matchup_name == 'Build' :
                print('erreur build name apeare' + champion + '/' + best_matchup_name )

            #graphe.add_node(meilleur_ban_name)
            graphe.add_edge(champion, best_matchup_name, type='Matchup', label=best_matchup_element.text)
            print(best_matchup_name,':',graphe.nodes[champion]['Lane'],':',best_matchup_element.text)
            j=j+1
    #==========================================================================================================
    i = i+1


# Sauvgarder le graphe 
chemin_du_fichier = "./mon_graphe.graphml"
nx.write_graphml(graphe, chemin_du_fichier)

#===========================================Graphe partie ===========================================
# Afficher le graphe avec une mise en page améliorée
plt.figure(figsize=(15, 15))
pos = nx.spring_layout(graphe, seed=42)
nx.draw(graphe, pos, with_labels=True, font_size=8, font_weight='bold', node_size=500, node_color='skyblue', edge_color='gray', linewidths=0.5)
edge_labels = nx.get_edge_attributes(graphe, 'label')
nx.draw_networkx_edge_labels(graphe, pos, edge_labels=edge_labels)
plt.show()
driver.quit()

#========================================================================================

# Sauvgarder le graphe 

# Charger le graphe depuis le fichier GraphML
#graphe_charge = nx.read_graphml(chemin_du_fichier)
