from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time

# Utilisation du navigateur Chrome. Assurez-vous d'avoir le driver correspondant installé.
driver = webdriver.Chrome()

# Ouvrir la page web
driver.get("https://draftlol.dawe.gg/f2XoiNhx/SCNHdeli")

# Fonction pour attendre que le joueur Red soit prêt et cliquer sur "Ready"
def wait_for_red_turn(driver):
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.roomReadyBackgroundred.active"))
    )
    print("C'est le tour de Red.")
    
    # Ajouter le clic sur "Ready" pour le joueur Red
    room_ready_red = driver.find_element(By.CSS_SELECTOR, "div.roomReadyBackgroundred.active")
    room_ready_red.click()
    print("Le joueur Red a cliqué sur Ready.")

# Fonction pour attendre que le joueur Blue soit prêt et cliquer sur "Ready"
def wait_for_blue_turn(driver):
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.roomReadyBackgroundblue.active"))
    )
    print("C'est le tour de Blue.")
    
    # Ajouter le clic sur "Ready" pour le joueur Blue
    room_ready_blue = driver.find_element(By.CSS_SELECTOR, "div.roomReadyBackgroundblue.active")
    room_ready_blue.click()
    print("Le joueur Blue a cliqué sur Ready.")

def click_sur_champion_random(driver):
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[6]/div[2]/img'))
    )
    list_champion_element = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[6]/div[2]/img')
    elements_non_desactives = [element for element in list_champion_element if not element.get_attribute('disabled')]
    element_aleatoire = random.choice(elements_non_desactives)
    element_aleatoire.click()
    element_select = driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[7]')
    element_select[0].click()
    valeur_alt = element_aleatoire.get_attribute('alt')
    print("champion choisi : " + valeur_alt)


# Attendre que la page soit chargée (timeout de 10 secondes)
try:
    # click ready
    wait_for_blue_turn(driver)
    wait_for_red_turn(driver)

    # phase de ban 1

    # clicker sur un ban 1
    click_sur_champion_random(driver)
    # attendre le tour blue 
    wait_for_blue_turn(driver)
    wait_for_red_turn(driver)
    # click pour ban 2
    click_sur_champion_random(driver)
    # attendre le tour blue
    wait_for_blue_turn(driver)
    wait_for_red_turn(driver)
    # click pour ban3
    click_sur_champion_random(driver)
    # attndre le tour blue 
    wait_for_blue_turn(driver)
    wait_for_red_turn(driver)
    print("FIN phase de ban 1")  

    #phase de pick 1
    click_sur_champion_random(driver)
    click_sur_champion_random(driver)
    wait_for_blue_turn(driver)
    wait_for_red_turn(driver)
    click_sur_champion_random(driver)
    
    print("FIN phase de pick 1")   

    # phase de ban 2
    click_sur_champion_random(driver) 
    wait_for_blue_turn(driver)
    wait_for_red_turn(driver)
    click_sur_champion_random(driver)
    print("FIN phase de ban 2") 

    # phase de pick 2
    click_sur_champion_random(driver) 
    wait_for_blue_turn(driver)
    wait_for_red_turn(driver)
    click_sur_champion_random(driver)
    
    wait_for_blue_turn(driver)
    wait_for_red_turn(driver)
    EC.text_to_be_present_in_element((By.XPATH, '//*[@id="root"]/div/div[7]'), "Finished")
    


    print("FIN de la draft") 
finally:
    # Fermer le navigateur
    driver.quit()
