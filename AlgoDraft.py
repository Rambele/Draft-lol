import networkx as nx
import matplotlib.pyplot as plt
import random
import random

champion_data = [
    {"name": "Ahri", "note": "A", "style": "Combo", "role": "Mid", "features": [True, False, False, True, True, True, False]},
    {"name": "Darius", "note": "B", "style": "Split", "role": "Jungle", "features": [True, False, True, False, False, False, True]},
    {"name": "Ezreal", "note": "S", "style": "Poke", "role": "ADC", "features": [True, False, False, True, False, True, True]},
    {"name": "Fiora", "note": "A", "style": "Split", "role": "Top", "features": [True, False, True, False, False, False, True]},
    {"name": "Garen", "note": "C", "style": "Tank", "role": "Top", "features": [True, True, False, True, True, False, False]},
    {"name": "Jinx", "note": "S", "style": "Siege", "role": "ADC", "features": [True, False, False, True, False, True, True]},
    {"name": "Katarina", "note": "A", "style": "Assassin", "role": "Mid", "features": [True, True, True, False, True, False, True]},
    {"name": "Lulu", "note": "A", "style": "Protect", "role": "Support", "features": [True, True, False, True, False, False, True]},
    {"name": "Malphite", "note": "B", "style": "Tank", "role": "Top", "features": [True, True, False, True, True, False, False]},
    {"name": "Nami", "note": "A", "style": "Protect", "role": "Support", "features": [True, True, False, True, False, False, True]},
    {"name": "Orianna", "note": "S", "style": "Combo", "role": "Mid", "features": [True, False, False, True, False, True, True]},
    {"name": "Pyke", "note": "A", "style": "Assassin", "role": "Support", "features": [True, True, True, False, True, False, True]},
    {"name": "Quinn", "note": "B", "style": "Split", "role": "Top", "features": [True, False, True, False, False, True, True]},
    {"name": "Riven", "note": "A", "style": "Split", "role": "Top", "features": [True, True, True, False, False, False, True]},
    {"name": "Sivir", "note": "B", "style": "Siege", "role": "ADC", "features": [True, False, False, True, False, True, True]},
    {"name": "Xin Zhao", "note": "B", "style": "Fighter", "role": "Jungle", "features": [True, True, False, False, True, False, False]},
    {"name": "Zed", "note": "A", "style": "Assassin", "role": "Mid", "features": [True, True, True, False, False, True, False]},
    {"name": "Ashe", "note": "A", "style": "ADC", "role": "ADC", "features": [True, False, False, True, False, True, True]},
    {"name": "Thresh", "note": "S", "style": "Support", "role": "Support", "features": [True, True, True, True, False, False, True]},
    {"name": "Rengar", "note": "B", "style": "Assassin", "role": "Jungle", "features": [True, True, False, False, True, False, True]},
    {"name": "Akali", "note": "S", "style": "Assassin", "role": "Mid", "features": [True, True, True, False, True, False, False]},
    {"name": "Vayne", "note": "A", "style": "ADC", "role": "ADC", "features": [True, True, False, True, False, True, True]},
    {"name": "Maokai", "note": "B", "style": "Tank", "role": "Top", "features": [True, True, False, True, True, False, False]},
    {"name": "Janna", "note": "A", "style": "Protect", "role": "Support", "features": [True, True, False, True, False, False, True]},
    {"name": "Lee Sin", "note": "A", "style": "Fighter", "role": "Jungle", "features": [True, True, False, False, True, False, True]},
    {"name": "Lucian", "note": "S", "style": "ADC", "role": "ADC", "features": [True, False, True, True, False, True, True]},
    {"name": "Leona", "note": "B", "style": "Tank", "role": "Support", "features": [True, True, False, True, True, False, True]},
    {"name": "Gragas", "note": "A", "style": "Tank", "role": "Jungle", "features": [True, True, False, True, False, False, False]},
    {"name": "Caitlyn", "note": "A", "style": "Siege", "role": "ADC", "features": [True, False, False, True, False, True, True]},
    {"name": "Yasuo", "note": "S", "style": "Fighter", "role": "Mid", "features": [True, True, True, False, True, False, True]},
]


# Matrices
synergy_matrix = [
    [0, 8, 5, 3, 7, 6, 2, 4, 9, 1, 4, 6, 7, 2, 8, 3, 6, 5, 2, 7, 1, 4, 6, 3, 5, 8, 2, 4, 6, 9],
    [8, 0, 7, 4, 6, 9, 5, 3, 8, 2, 5, 7, 6, 1, 9, 4, 8, 7, 2, 1, 4, 3, 7, 8, 1, 5, 6, 9, 2, 5],
    [5, 7, 0, 6, 8, 4, 9, 2, 5, 7, 3, 1, 9, 6, 4, 6, 9, 2, 4, 6, 8, 5, 3, 7, 2, 1, 5, 8, 9, 7],
    [3, 4, 6, 0, 5, 7, 8, 9, 2, 1, 4, 8, 3, 6, 5, 7, 4, 2, 9, 1, 8, 6, 2, 9, 5, 3, 7, 8, 2, 1],
    [7, 6, 8, 5, 0, 3, 4, 6, 7, 2, 8, 1, 9, 5, 3, 6, 7, 2, 4, 6, 1, 4, 6, 2, 8, 3, 7, 1, 5, 8],
    [6, 9, 4, 7, 3, 0, 6, 8, 9, 5, 7, 2, 1, 3, 7, 5, 9, 1, 3, 7, 2, 6, 1, 3, 8, 4, 2, 3, 6, 5],
    [2, 5, 9, 8, 4, 6, 0, 3, 7, 1, 6, 9, 2, 4, 6, 9, 2, 5, 7, 3, 1, 6, 8, 3, 4, 2, 9, 1, 5, 8],
    [4, 3, 2, 9, 7, 8, 3, 0, 4, 7, 1, 5, 6, 8, 2, 1, 6, 4, 3, 5, 9, 7, 1, 8, 2, 9, 1, 7, 3, 6],
    [9, 8, 5, 2, 7, 9, 7, 4, 0, 6, 3, 1, 5, 6, 9, 2, 8, 1, 4, 6, 3, 7, 1, 4, 6, 9, 5, 3, 7, 8],
    [1, 2, 7, 1, 1, 7, 1, 7, 6, 0, 9, 3, 7, 3, 6, 1, 2, 9, 6, 1, 4, 2, 8, 4, 5, 1, 6, 3, 7, 1],
    [4, 5, 3, 4, 6, 7, 6, 1, 3, 9, 0, 6, 5, 4, 6, 7, 5, 7, 8, 3, 6, 1, 3, 8, 2, 9, 1, 7, 6, 5],
    [6, 7, 1, 8, 1, 2, 9, 5, 1, 3, 6, 0, 7, 3, 1, 8, 9, 3, 5, 4, 6, 2, 9, 1, 7, 6, 5, 8, 4, 2],
    [7, 6, 9, 3, 5, 8, 6, 2, 5, 7, 5, 7, 0, 6, 5, 6, 3, 7, 2, 9, 8, 1, 5, 4, 7, 2, 8, 6, 9, 1],
    [2, 1, 6, 6, 9, 1, 4, 8, 6, 3, 4, 3, 6, 0, 8, 1, 6, 2, 9, 4, 5, 7, 8, 4, 2, 3, 7, 1, 9, 5],
    [8, 9, 4, 5, 3, 3, 6, 2, 9, 6, 6, 1, 5, 8, 0, 7, 5, 8, 2, 1, 7, 6, 1, 4, 6, 9, 3, 7, 2, 8],
    [3, 4, 6, 7, 6, 7, 1, 1, 2, 1, 7, 8, 6, 1, 7, 0, 5, 9, 1, 8, 6, 2, 9, 5, 3, 7, 8, 2, 4, 6],
    [6, 8, 9, 4, 7, 9, 2, 6, 8, 2, 5, 9, 3, 6, 5, 5, 0, 3, 4, 6, 9, 1, 3, 7, 8, 2, 1, 4, 6, 7],
    [5, 7, 2, 2, 2, 1, 5, 4, 1, 9, 7, 3, 7, 2, 8, 9, 3, 0, 6, 5, 1, 4, 6, 7, 8, 1, 2, 9, 6, 3],
    [2, 2, 4, 9, 4, 3, 7, 3, 4, 6, 8, 5, 2, 9, 2, 1, 4, 6, 0, 8, 3, 7, 8, 5, 1, 3, 6, 9, 7, 2],
    [7, 1, 6, 1, 6, 7, 3, 5, 6, 1, 3, 4, 9, 4, 1, 8, 6, 5, 8, 0, 7, 2, 9, 1, 3, 8, 2, 9, 5, 7],
    [1, 4, 8, 8, 1, 2, 1, 9, 1, 4, 6, 6, 8, 5, 7, 6, 9, 1, 3, 7, 0, 6, 3, 5, 4, 6, 2, 9, 1, 8],
    [4, 3, 5, 6, 4, 6, 6, 7, 3, 2, 2, 2, 1, 7, 6, 2, 1, 4, 7, 2, 6, 0, 8, 9, 5, 3, 7, 8, 1, 4],
    [6, 7, 3, 2, 6, 1, 8, 1, 7, 9, 9, 9, 5, 8, 1, 9, 3, 6, 8, 9, 3, 8, 0, 6, 1, 4, 2, 9, 5, 7],
    [3, 8, 7, 9, 2, 3, 3, 4, 4, 5, 1, 5, 4, 4, 3, 5, 7, 1, 5, 1, 5, 9, 6, 0, 8, 9, 2, 7, 6, 1],
    [5, 1, 2, 5, 8, 8, 4, 2, 6, 3, 3, 3, 7, 2, 6, 8, 8, 3, 1, 3, 4, 5, 1, 8, 0, 7, 6, 9, 2, 4],
    [8, 5, 1, 3, 3, 4, 2, 9, 5, 8, 6, 7, 2, 3, 9, 2, 2, 6, 4, 8, 6, 3, 4, 9, 7, 0, 5, 6, 1, 8],
    [2, 6, 5, 7, 7, 2, 9, 1, 3, 1, 9, 1, 8, 7, 1, 1, 1, 9, 6, 2, 2, 7, 2, 2, 6, 5, 7, 8, 3, 4],
    [4, 9, 7, 8, 1, 3, 1, 7, 7, 2, 1, 4, 6, 1, 3, 4, 7, 1, 9, 1, 7, 8, 9, 7, 9, 6, 0, 8, 5, 3],
    [6, 2, 2, 2, 5, 7, 5, 1, 6, 6, 3, 2, 9, 6, 7, 2, 1, 3, 2, 5, 6, 2, 2, 2, 9, 8, 5, 0, 1, 4],
    [9, 5, 4, 3, 6, 3, 7, 4, 3, 1, 7, 9, 1, 9, 2, 9, 4, 6, 9, 1, 1, 9, 7, 7, 2, 6, 6, 1, 0, 8],
]

matchup_matrix_15 = [
    [0, 5, 8, 3, 7, 2, 1, 4, 6, 9, 7, 4, 6, 3, 1, 5, 2, 8, 1, 3, 4, 9, 7, 2, 6, 8, 3, 5, 1, 4],
    [5, 0, 7, 4, 6, 9, 8, 3, 1, 2, 8, 5, 7, 1, 4, 6, 9, 2, 5, 7, 3, 1, 6, 5, 7, 1, 4, 6, 3, 2],
    [8, 7, 0, 6, 8, 4, 9, 2, 5, 7, 3, 1, 6, 4, 5, 1, 3, 7, 6, 4, 9, 2, 5, 7, 3, 2, 6, 4, 1, 8],
    [3, 4, 6, 0, 5, 7, 2, 9, 1, 8, 4, 6, 9, 5, 7, 8, 2, 1, 3, 6, 5, 7, 1, 4, 3, 6, 9, 2, 8, 1],
    [7, 6, 8, 5, 0, 3, 6, 7, 2, 4, 6, 1, 5, 8, 2, 3, 4, 6, 7, 5, 2, 8, 1, 9, 5, 7, 3, 1, 6, 4],
    [2, 9, 4, 7, 3, 0, 6, 8, 9, 5, 7, 2, 8, 1, 3, 6, 5, 1, 2, 9, 8, 9, 5, 7, 4, 6, 1, 3, 2, 7],
    [1, 8, 9, 2, 6, 6, 0, 3, 7, 1, 6, 9, 4, 2, 6, 1, 7, 3, 6, 2, 9, 5, 1, 3, 8, 9, 7, 4, 6, 5],
    [4, 3, 2, 9, 7, 8, 3, 0, 4, 7, 1, 5, 2, 9, 1, 4, 6, 5, 8, 3, 7, 1, 8, 9, 2, 3, 4, 7, 6, 1],
    [6, 1, 5, 1, 2, 9, 7, 4, 0, 6, 3, 1, 3, 7, 9, 2, 6, 8, 9, 7, 4, 1, 5, 8, 3, 4, 6, 2, 9, 1],
    [9, 2, 7, 8, 4, 5, 1, 7, 6, 0, 9, 3, 1, 8, 2, 7, 1, 3, 5, 8, 4, 6, 9, 7, 2, 5, 1, 4, 3, 6],
    [7, 8, 3, 4, 6, 7, 6, 1, 3, 9, 0, 6, 5, 4, 6, 5, 3, 7, 9, 2, 1, 4, 3, 6, 2, 8, 1, 5, 7, 9],
    [4, 5, 1, 6, 1, 2, 9, 5, 1, 3, 6, 0, 7, 3, 1, 9, 5, 8, 4, 2, 6, 1, 3, 2, 6, 9, 7, 4, 5, 8],
    [6, 7, 6, 9, 5, 8, 4, 2, 9, 1, 5, 7, 0, 6, 5, 8, 9, 7, 3, 1, 2, 3, 4, 1, 5, 6, 0, 8, 2, 9],
    [3, 1, 4, 5, 8, 1, 2, 9, 1, 8, 4, 3, 6, 0, 8, 1, 4, 6, 5, 9, 7, 5, 8, 2, 7, 1, 3, 6, 4, 9],
    [1, 4, 5, 7, 2, 3, 6, 1, 3, 2, 6, 1, 5, 8, 0, 4, 5, 7, 1, 9, 2, 6, 1, 3, 9, 2, 8, 7, 4, 5],
    [5, 6, 1, 8, 3, 6, 1, 4, 6, 7, 4, 6, 8, 1, 4, 0, 9, 2, 3, 1, 5, 2, 8, 3, 1, 6, 7, 9, 5, 2],
    [2, 9, 3, 2, 4, 5, 7, 6, 5, 1, 6, 5, 9, 4, 5, 9, 0, 3, 6, 1, 8, 7, 2, 8, 1, 7, 4, 2, 3, 6],
    [8, 2, 7, 1, 6, 1, 3, 5, 8, 3, 7, 8, 7, 6, 7, 2, 3, 0, 6, 5, 1, 9, 4, 6, 9, 4, 5, 1, 3, 2],
    [1, 5, 6, 3, 7, 2, 6, 8, 9, 5, 9, 4, 3, 5, 1, 3, 6, 6, 0, 8, 7, 1, 4, 2, 5, 7, 1, 4, 6, 9],
    [4, 7, 4, 6, 5, 9, 2, 3, 7, 8, 2, 2, 6, 9, 9, 1, 1, 5, 8, 0, 3, 6, 5, 8, 3, 6, 1, 9, 7, 4],
    [9, 3, 9, 5, 2, 8, 9, 7, 4, 4, 1, 6, 1, 7, 2, 5, 8, 1, 7, 3, 0, 6, 1, 4, 6, 2, 3, 9, 5, 8],
    [6, 1, 2, 7, 8, 9, 5, 1, 6, 1, 4, 1, 3, 5, 6, 2, 7, 9, 1, 6, 6, 0, 8, 3, 4, 5, 7, 2, 9, 1],
    [7, 6, 5, 1, 1, 5, 1, 8, 9, 3, 3, 4, 4, 8, 1, 8, 2, 4, 4, 5, 1, 8, 0, 9, 5, 2, 7, 6, 1, 3],
    [2, 5, 7, 4, 9, 7, 3, 2, 7, 6, 6, 1, 5, 2, 3, 3, 8, 6, 2, 8, 4, 3, 9, 0, 6, 7, 1, 4, 5, 8],
    [8, 7, 3, 3, 5, 4, 8, 7, 1, 9, 9, 5, 7, 5, 6, 1, 1, 9, 5, 3, 6, 4, 4, 6, 0, 2, 8, 7, 1, 3],
    [1, 1, 2, 6, 7, 6, 9, 1, 3, 4, 4, 6, 1, 7, 2, 7, 7, 4, 7, 6, 2, 5, 5, 7, 2, 0, 8, 1, 9, 4],
    [9, 4, 6, 9, 3, 1, 7, 3, 4, 5, 5, 2, 3, 4, 3, 4, 6, 5, 1, 2, 3, 7, 7, 1, 8, 2, 0, 9, 6, 5],
    [5, 6, 1, 2, 7, 3, 4, 4, 6, 1, 1, 3, 6, 6, 6, 2, 1, 8, 4, 3, 9, 2, 6, 4, 7, 8, 9, 0, 5, 1],
    [7, 3, 8, 8, 3, 2, 6, 7, 2, 4, 9, 9, 4, 1, 1, 6, 3, 3, 6, 7, 5, 9, 1, 5, 1, 7, 6, 5, 0, 2],
    [3, 2, 1, 1, 1, 7, 5, 6, 9, 6, 2, 1, 2, 8, 9, 9, 6, 6, 9, 8, 8, 1, 3, 8, 3, 1, 1, 1, 2, 0],
]



import random

def initialize_availability_matrix(champion_data):
    return {champion["name"]: True for champion in champion_data}

def update_availability(champion, availability_matrix):
    availability_matrix[champion["name"]] = False

def draft_turn(champion_data, synergy_matrix, availability_matrix, ban=False):
    available_champions = [champion for champion in champion_data if availability_matrix[champion["name"]]]
    if available_champions:
        chosen_champion = random.choice(available_champions)
        if ban:
            print(f"Banned: {chosen_champion['name']}")
        else:
            print(f"Picked: {chosen_champion['name']}")
        return chosen_champion
    else:
        print("No available champions.")
        return None

def draft(champion_data, synergy_matrix):
    availability_matrix = initialize_availability_matrix(champion_data)

    # Initialisation des listes pour les bans et les picks
    blue_bans = []
    red_bans = []
    blue_picks = []
    red_picks = []

    # Phase de bans
    for _ in range(3):
        print("Blue Team's Ban:")
        blue_ban = draft_turn(champion_data, synergy_matrix, availability_matrix, ban=True)
        blue_bans.append(blue_ban)
        update_availability(blue_ban, availability_matrix)

        print("Red Team's Ban:")
        red_ban = draft_turn(champion_data, synergy_matrix, availability_matrix, ban=True)
        red_bans.append(red_ban)
        update_availability(red_ban, availability_matrix)

    # Phase de picks
    # Blue Team
    print("Blue Team's Pick:")
    blue_pick_1 = draft_turn(champion_data, synergy_matrix, availability_matrix)
    blue_picks.append(blue_pick_1)
    update_availability(blue_pick_1, availability_matrix)

    # Red Team
    print("Red Team's Picks:")
    red_pick_1 = draft_turn(champion_data, synergy_matrix, availability_matrix)
    red_picks.append(red_pick_1)
    update_availability(red_pick_1, availability_matrix)

    red_pick_2 = draft_turn(champion_data, synergy_matrix, availability_matrix)
    red_picks.append(red_pick_2)
    update_availability(red_pick_2, availability_matrix)

    # Blue Team
    print("Blue Team's Picks:")
    blue_pick_2 = draft_turn(champion_data, synergy_matrix, availability_matrix)
    blue_picks.append(blue_pick_2)
    update_availability(blue_pick_2, availability_matrix)

    blue_pick_3 = draft_turn(champion_data, synergy_matrix, availability_matrix)
    blue_picks.append(blue_pick_3)
    update_availability(blue_pick_3, availability_matrix)

    # Phase de bans
    for _ in range(2):
        print("Red Team's Ban:")
        red_ban = draft_turn(champion_data, synergy_matrix, availability_matrix, ban=True)
        red_bans.append(red_ban)
        update_availability(red_ban, availability_matrix)

        print("Blue Team's Ban:")
        blue_ban = draft_turn(champion_data, synergy_matrix, availability_matrix, ban=True)
        blue_bans.append(blue_ban)
        update_availability(blue_ban, availability_matrix)

    # Phase de picks
    # Red Team
    print("Red Team's Picks:")
    red_pick_3 = draft_turn(champion_data, synergy_matrix, availability_matrix)
    red_picks.append(red_pick_3)
    update_availability(red_pick_3, availability_matrix)

    red_pick_4 = draft_turn(champion_data, synergy_matrix, availability_matrix)
    red_picks.append(red_pick_4)
    update_availability(red_pick_4, availability_matrix)

    # Blue Team
    print("Blue Team's Pick:")
    blue_pick_4 = draft_turn(champion_data, synergy_matrix, availability_matrix)
    blue_picks.append(blue_pick_4)
    update_availability(blue_pick_4, availability_matrix)

    # Afficher les résultats
    print("Blue Bans:", [champion["name"] for champion in blue_bans])
    print("Red Bans:", [champion["name"] for champion in red_bans])
    print("Blue Picks:", [champion["name"] for champion in blue_picks])
    print("Red Picks:", [champion["name"] for champion in red_picks])

# Exécution de la fonction draft
draft(champion_data, synergy_matrix)
