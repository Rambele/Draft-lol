import networkx as nx
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



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
wait = WebDriverWait(driver, 60)
wait.until(EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/main[1]/article[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/section[1]/div[1]/a[1]')))

# Obtenez une liste de tous les champions présents sur la page
champion_elements = driver.find_elements(By.XPATH, '/html[1]/body[1]/div[2]/main[1]/article[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/section[1]/div[1]/a')

# Créer un graphe pour stocker les champions leurs données et leurs relations avec les autre champion
graphe = nx.Graph()
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
    graphe.add_node(champion_name)
    links.append(champion_element.get_attribute('href'))
    print(champion_name)

   
i = 0 # le i pour acceder au lien numero i champion i pendant la boucle
for champion in list_champ_name:

    driver.get(links[i])

    # Attendre que la page du champion se charge complètement
    wait.until(EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/main[1]/article[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[6]/section[1]/div[1]/div[1]/div[1]/a[1]/div[1]/img[1]')))
    # Obtenez les éléments des meilleurs bans
    meilleurs_bans_elements = driver.find_elements(By.XPATH, '/html[1]/body[1]/div[2]/main[1]/article[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[6]/section[1]/div[1]/div[1]/div[1]/a')
    # Ajouter chaque meilleur ban comme un sommet au graphe
    j=1

    # Récuperer les donnée de champion i 
    wait.until(EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/main[1]/article[1]/div[1]/div[1]/div[1]/header[1]/div[1]/div[1]/div[1]/div[2]/span[1]/div[1]/span')))
    donnees = []
    donnee_champ_elements = driver.find_elements(By.XPATH, '/html/body/div[2]/main/article/div/div[1]/div/header/div/div/div[1]/div[2]/span/div/span')
    for donnee_champ_element in donnee_champ_elements :
        info_text = donnee_champ_element.text.split("\n")
        info = info_text[1].strip()
        donnees.append(info)
    # Clés fixes
    cles_fixes = ['Tier', 'Win', 'Role', 'Pick', 'Ban', 'Games', 'KDA', 'Score']
    # Créer un dictionnaire en utilisant les clés fixes
    donnees_champion = dict(zip(cles_fixes, donnees))
    print(donnees_champion)
    graphe.nodes[champion].update(donnees_champion)
    print("Donnée mise a jour \2" + champion)
    #=============FIN RECUPERATION============

    for meilleur_ban_element in meilleurs_bans_elements:
        #meilleur_ban_name = meilleur_ban_element.get_attribute('title')
        href = meilleur_ban_element.get_attribute('href')
        if href.split('/')[-1].replace("-", " ").capitalize() in graphe :
          
          meilleur_ban_name = href.split('/')[-1].replace("-", " ").capitalize()
        else :
            meilleur_ban_name = href.split('/')[-2].replace("-", " ").capitalize()
    
        if meilleur_ban_name == 'Build' :
            print('erreur build name apeare' + champion + '/' + meilleur_ban_name )
            print(j)

        #graphe.add_node(meilleur_ban_name)
        graphe.add_edge(champion, meilleur_ban_name)
        j=j+1
    i = i+1

# Afficher le graphe avec une mise en page améliorée
plt.figure(figsize=(15, 15))
pos = nx.spring_layout(graphe, seed=42)
nx.draw(graphe, pos, with_labels=True, font_size=8, font_color='black', font_weight='bold', node_size=500, node_color='skyblue', edge_color='gray', linewidths=0.5)
edge_labels = nx.get_edge_attributes(graphe, 'weight')
nx.draw_networkx_edge_labels(graphe, pos, edge_labels=edge_labels)
plt.show()

# Fermer le navigateur une fois que vous avez terminé
driver.quit()
