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
wait = WebDriverWait(driver, 20)
wait.until(EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/main[1]/article[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/section[1]/div[1]/a[1]')))

# Obtenez une liste de tous les champions présents sur la page
champion_element = driver.find_elements(By.XPATH, '/html[1]/body[1]/div[2]/main[1]/article[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/section[1]/div[1]/a[1]')

# Créer un graphe pour stocker les champions leurs données et leurs relations avec les autre champion
graphe = nx.Graph()
# Dictionnaire pour stocker des données supplémentaires sur les sommets
champion_data = {}


driver.get('https://www.metasrc.com/lol/build/aatrox')
#attednre que les données de champion ce chargant
wait.until(EC.presence_of_element_located((By.XPATH, '/html[1]/body[1]/div[2]/main[1]/article[1]/div[1]/div[1]/div[1]/header[1]/div[1]/div[1]/div[1]/div[2]/span[1]/div[1]/span')))
valeurs_champion = []
donnee_champ_elements = driver.find_elements(By.XPATH, '/html/body/div[2]/main/article/div/div[1]/div/header/div/div/div[1]/div[2]/span/div/span')
for donnee_champ_element in donnee_champ_elements :
    info_text = donnee_champ_element.text.split("\n")
    info = info_text[1].strip()
    print(info)
    valeurs_champion.append(info)

print(valeurs_champion)
# Clés fixes
cles_fixes = ['Tier', 'Win', 'Role', 'Pick', 'Ban', 'Games', 'KDA', 'Score']

# Créer un dictionnaire en utilisant les clés fixes
donnees_champion = dict(zip(cles_fixes, valeurs_champion))

print(donnees_champion)
driver.quit()
