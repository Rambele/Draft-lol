import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_mobalytics():
    url = 'https://mobalytics.gg/lol/profile/euw/ssh%20fox/champion-pool'

    # Configurer les options pour un navigateur sans tête
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Nécessaire pour certains systèmes

    # Instancier le navigateur Chrome avec les options configurées
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        # Attendre que la page se charge complètement (ajuster le délai si nécessaire)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "m-s5xdrg")))

        # Cibler les balises et les classes spécifiques pour extraire les données
        champion_elements = driver.find_elements(By.CLASS_NAME, 'm-s5xdrg')

        # Créer un fichier CSV et écrire les en-têtes
        with open('champions_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Champion', 'Image URL'])

            for champion_element in champion_elements:
                image_url = champion_element.find_element(By.TAG_NAME, 'img').get_attribute('src')
                champion_name = champion_element.find_element(By.CLASS_NAME, 'm-arwevg').text

                # Écrire les données dans le fichier CSV
                csv_writer.writerow([champion_name, image_url])

    finally:
        driver.quit()

# Utilisation de la fonction sans paramètre spécifique
scrape_mobalytics()
