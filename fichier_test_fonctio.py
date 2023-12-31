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
url = 'https://www.metasrc.com/lol/build/yone/mid'
driver.get(url)

# Attendre que la page se charge complètement
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="page-content"]/div[7]/section/div/div/div/a')))

# Obtenez une liste de tous les champions présents sur la page
champion_elements = driver.find_elements(By.XPATH, '//*[@id="page-content"]/div[7]/section/div/div/div/a')





# Ajouter chaque champion comme un sommet au graphe
for champion_element in champion_elements:
   
    href = champion_element.get_attribute('href')
    
    print(href.split('/')[-1] + " " + champion_element.text )
          
          


# Fermer le navigateur une fois que vous avez terminé
driver.quit()



# best counters  : //*[@id="page-content"]/div[10]/section/div/div/div/a
# best synergies : //*[@id="page-content"]/div[7]/section/div/div/div/a
# best matchups : //*[@id="page-content"]/div[11]/section/div/div/div/a