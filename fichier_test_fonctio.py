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
wait = WebDriverWait(driver, 360)
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
    links.append(champion_element.get_attribute('href')) 

   
i = 0 # le i pour acceder au lien numero i champion i pendant la boucle
perdu = 0
for champion in list_champ_name:
    driver.get(links[i])
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
    if donnees_champion :
        print("Donnée mise a jour \2" + champion)
    else :
        perdu = perdu + 1
        print("Donnée perdu :" , perdu)
    #=============FIN RECUPERATION============
    i = i+1



# Fermer le navigateur une fois que vous avez terminé
driver.quit()


