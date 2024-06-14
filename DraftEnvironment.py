import gym
from gym import spaces
import networkx as nx
import Equipe
from ClasseDraft import ClasseDraft
import random
import time
import DraftAgentDqn
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random
import numpy as np
from collections import deque

class DraftEnvironment(gym.Env):
    def __init__(self, graphe):
        super(DraftEnvironment, self).__init__()
        
        self.draft = ClasseDraft(graphe)
        self.action_space = spaces.Discrete(len(self.draft.champion_disponible()))
    
    def reset(self) : 
        return np.array(self.draft.reset_draft()).flatten()
    
    def step(self, action, agent=True):
        
        #convertir l'action en un nom de champion
        if agent :
            action = self.draft.indice_to_champion(self.draft.champion_indice_list[action])
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
        return self.draft.reward_action_only_blue()

    def check_done(self):
        return True if self.draft.letour==19 else False #0--->19 = 20 tours 


# Initialisation de l'environnement et de l'agent
    

graphe = nx.read_gml('mon_graphe.gml')
env = DraftEnvironment(graphe.copy())
state_size = 21 + len(env.draft.champion_indice_list)
action_size =  len(env.draft.champion_indice_list)
agent = DraftAgentDqn.DQNAgent(state_size, action_size)
#agent.model.load_state_dict(torch.load('dqn_model.pth4.1'))
display_interval = 10
# Paramètres d'entraînement
num_episodes = 100
batch_size = 32

# Boucle d'entraînement
for episode in range(num_episodes):
    state = env.reset()  # Réinitialiser l'environnement pour un nouvel épisode
    initial_state = env.draft.get_observation()
    #print("Taille de l'état initial:", initial_state)
    state =  torch.tensor(state, dtype=torch.float32)
    action = 0
    for step in range(20):
        if env.draft.tours[step] == "b" :
            agent.update_action_size(len(env.draft.champion_indice_list))
            action = agent.act(state)  # L'agent choisit une action
            try :
                next_state, reward, done, _ = env.step(action)  # Exécutez l'action dans l'environnement
            except :
                print("Action agent  = ",action)
                print("Champion corespondance : ",env.draft.indice_to_champion(action))
                print("Etat de la draft  =======> :")
                print("Blue bans : ", env.draft.blue.bans)
                print("Blue picks : ", env.draft.blue.picks)
                print("Red bans : ", env.draft.red.bans)
                print("Red picks : ", env.draft.red.picks)
                reward = -1000
                print("REWARD  : ", reward)
                
                break

            
        else : 
            actionHeuristique = env.draft.red.choix_pick_ban(env.draft.red.tours[int(step/2)])
            rewardX = 0
            if reward == -1000 : rewardX = -1000
            next_state, reward, done, _ = env.step(actionHeuristique,False)
            if rewardX == -1000 : reward = -1000
            # Stockez l'expérience dans la mémoire de relecture
            agent.remember(state, action, reward, next_state, done)
            # Mettez à jour les poids du réseau neuronal en utilisant la mémoire de relecture
            agent.replay(batch_size)
            #state = np.reshape(next_state, [1, state_size])

        if done:
            #env.draft.afficher_resultat()
            break

    # Affichez et évaluez la performance de l'agent périodiquement
    if episode % display_interval == 0:
        print("Épisode:", episode)
        print("evaluation draft :" ,env.draft.blue.score_draft()-env.draft.red.score_draft())
        try :
            env.draft.afficher_resultat()
        except :
                print("Action agent  = ",action)
                print("Champion corespondance : ",env.draft.indice_to_champion(action))
                print("Etat de la draft  =======> :")
                print("Blue bans : ", env.draft.blue.bans)
                print("Blue picks : ", env.draft.blue.picks)
                print("Red bans : ", env.draft.red.bans)
                print("Red picks : ", env.draft.red.picks)
                print("REWARD  : ", reward)
#jouer cntre mon model 
# Apres l'entrainement je rend epsilon a zero et je le lance contre le model heuristique 
if num_episodes != 0 :
    torch.save(agent.model.state_dict(), 'dqn_model.pth5')
print("Lancer le test  : ...")
time.sleep(5)
state = env.reset()  # Réinitialiser l'environnement pour un nouvel épisode
initial_state = env.draft.get_observation()
print("Taille de l'état initial:", initial_state)
state =  torch.tensor(state, dtype=torch.float32)
dernier_reward = 0
for step in range(20):
    if env.draft.tours[step] == "b" :
        agent.update_action_size(len(env.draft.champion_disponible()))
        action = agent.act(state,True)  # L'agent choisit une action
        try :
            next_state, reward, done, _ = env.step(action)  # Exécutez l'action dans l'environnement
        except :
            print("Parite test Choix cahmpion out pf range ")
            break
    else : 
        action = env.draft.red.choix_pick_ban(env.draft.red.tours[int(step/2)])
        next_state, reward, done, _ = env.step(action,False)

    if done:
        break     

print("evaluation draft :" ,env.draft.blue.score_draft()-env.draft.red.score_draft())
env.draft.afficher_resultat()        
# Sauvegarde du modèle (si nécessaire)

'''
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
'''