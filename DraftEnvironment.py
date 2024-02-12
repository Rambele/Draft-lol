import gym
from gym import spaces
import networkx as nx
import Equipe
from ClasseDraft import ClasseDraft
import random
import time
class DraftEnvironment(gym.Env):
    def __init__(self, graphe):
        super(DraftEnvironment, self).__init__()
        
        self.draft = ClasseDraft(graphe)
        self.action_space = spaces.Discrete(len(self.draft.champion_disponible()))
    
    def step(self, action):
        
        #Lancer un tour de draft 
        self.draft.lancer_un_tour_draft_step(action)

        # Vérifiez si la draft est terminée
        done = self.check_done()

        # Calculez la récompense (à adapter en fonction de votre logique)
        reward = self.calculate_reward()

        # Avancer d'un tour 
        self.draft.letour+=1

        # Définissez l'observation comme l'état actuel
        observation = self.draft.get_observation()

        # Définissez les informations supplémentaires si nécessaire
        info = {}

        return observation, reward, done, info

    def render(self, mode='human'):
        # Fonction de rendu (à définir en fonction des besoins)
        pass

    def close(self):
        # Nettoyer les ressources si nécessaire
        pass

    def calculate_reward(self):
        return self.draft.reward_action()

    def check_done(self):
        return True if self.draft.letour==20 else False



# Exemple d'utilisation
graphe = nx.read_gml('mon_graphe.gml')
env = DraftEnvironment(graphe)

# Boucle d'épisode
for _ in range(20):  # ou jusqu'à ce que done soit True
    action = random.choice(env.draft.champion_disponible())  # Remplacez ceci par l'action de votre agent
    observation, reward, done, info = env.step(action)
    print(observation)
    print("Action : ",action)
    print("Reward : ",reward)
    time.sleep(2)
    # Ajoutez d'autres étapes nécessaires en fonction de votre logique
    if done:
        break

env.close()
