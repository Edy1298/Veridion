import requests
from time import sleep
import random
import spacy
from nltk.corpus import wordnet

nlp = spacy.load("en_core_web_md")

host = "http://172.18.4.158:8000"
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5

words = {
    1: {"id": 1, "text": "Feather", "cost": 1},
    2: {"id": 2, "text": "Coal", "cost": 1},
    3: {"id": 3, "text": "Pebble", "cost": 1},
    4: {"id": 4, "text": "Leaf", "cost": 2},
    5: {"id": 5, "text": "Paper", "cost": 2},
    6: {"id": 6, "text": "Rock", "cost": 2},
    7: {"id": 7, "text": "Water", "cost": 3},
    8: {"id": 8, "text": "Twig", "cost": 3},
    9: {"id": 9, "text": "Sword", "cost": 4},
    10: {"id": 10, "text": "Shield", "cost": 4},
    11: {"id": 11, "text": "Gun", "cost": 5},
    12: {"id": 12, "text": "Flame", "cost": 5},
    13: {"id": 13, "text": "Rope", "cost": 5},
    14: {"id": 14, "text": "Disease", "cost": 6},
    15: {"id": 15, "text": "Cure", "cost": 6},
    16: {"id": 16, "text": "Bacteria", "cost": 6},
    17: {"id": 17, "text": "Shadow", "cost": 7},
    18: {"id": 18, "text": "Light", "cost": 7},
    19: {"id": 19, "text": "Virus", "cost": 7},
    20: {"id": 20, "text": "Sound", "cost": 8},
    21: {"id": 21, "text": "Time", "cost": 8},
    22: {"id": 22, "text": "Fate", "cost": 8},
    23: {"id": 23, "text": "Earthquake", "cost": 9},
    24: {"id": 24, "text": "Storm", "cost": 9},
    25: {"id": 25, "text": "Vaccine", "cost": 9},
    26: {"id": 26, "text": "Logic", "cost": 10},
    27: {"id": 27, "text": "Gravity", "cost": 10},
    28: {"id": 28, "text": "Robots", "cost": 10},
    29: {"id": 29, "text": "Stone", "cost": 11},
    30: {"id": 30, "text": "Echo", "cost": 11},
    31: {"id": 31, "text": "Thunder", "cost": 12},
    32: {"id": 32, "text": "Karma", "cost": 12},
    33: {"id": 33, "text": "Wind", "cost": 13},
    34: {"id": 34, "text": "Ice", "cost": 13},
    35: {"id": 35, "text": "Sandstorm", "cost": 13},
    36: {"id": 36, "text": "Laser", "cost": 14},
    37: {"id": 37, "text": "Magma", "cost": 14},
    38: {"id": 38, "text": "Peace", "cost": 14},
    39: {"id": 39, "text": "Explosion", "cost": 15},
    40: {"id": 40, "text": "War", "cost": 15},
    41: {"id": 41, "text": "Enlightenment", "cost": 15},
    42: {"id": 42, "text": "Nuclear Bomb", "cost": 16},
    43: {"id": 43, "text": "Volcano", "cost": 16},
    44: {"id": 44, "text": "Whale", "cost": 17},
    45: {"id": 45, "text": "Earth", "cost": 17},
    46: {"id": 46, "text": "Moon", "cost": 17},
    47: {"id": 47, "text": "Star", "cost": 18},
    48: {"id": 48, "text": "Tsunami", "cost": 18},
    49: {"id": 49, "text": "Supernova", "cost": 19},
    50: {"id": 50, "text": "Antimatter", "cost": 19},
    51: {"id": 51, "text": "Plague", "cost": 20},
    52: {"id": 52, "text": "Rebirth", "cost": 20},
    53: {"id": 53, "text": "Tectonic Shift", "cost": 21},
    54: {"id": 54, "text": "Gamma-Ray Burst", "cost": 22},
    55: {"id": 55, "text": "Human Spirit", "cost": 23},
    56: {"id": 56, "text": "Apocalyptic Meteor", "cost": 24},
    57: {"id": 57, "text": "Earth’s Core", "cost": 25},
    58: {"id": 58, "text": "Neutron Star", "cost": 26},
    59: {"id": 59, "text": "Supermassive Black Hole", "cost": 35},
    60: {"id": 60, "text": "Entropy", "cost": 45},
}

def find_antonyms(word):
    antonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.antonyms():
                antonyms.add(lemma.antonyms()[0].name())
    return antonyms

def find_best_counter(input_word, words):
    antonyms = find_antonyms(input_word)
    input_doc = nlp(input_word)

    best_match = None
    best_score = float('-inf')

    for word in words.values():
        word_text = word["text"]
        word_doc = nlp(word_text)

        score = -input_doc.similarity(word_doc)  
        if word_text.lower() in antonyms:
            score += 2
        
        if score > best_score or (score == best_score and word["cost"] < best_match["cost"]):
            best_score = score
            best_match = word

    return f'{best_match["id"]}'

def what_beats(word):
    sleep(random.randint(1, 3))
    return find_best_counter(word, words)

def play_game(player_id):

    for round_id in range(1, NUM_ROUNDS+1):
        round_num = -1
        while round_num != round_id:
            response = requests.get(get_url)
            print(response.json())
            sys_word = response.json()['word']
            round_num = response.json()['round']

            sleep(1)

        if round_id > 1:
            status = requests.get(status_url)
            print(status.json())

        choosen_word = what_beats(sys_word)
        data = {"player_id": player_id, "word_id": choosen_word, "round_id": round_id}
        response = requests.post(post_url, json=data)
        print(response.json())


if __name__ == "__main__":
    play_game("f85ZIXKKeG")
