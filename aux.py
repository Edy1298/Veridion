import requests
import json
import random
import spacy
from time import sleep
from nltk.corpus import wordnet

nlp = spacy.load("en_core_web_md")

with open("words.json", "r") as file:
    words = json.load(file)["words"]

# Configurări server
host = "http://172.18.4.158:8000"
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5

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

    for word in words:
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
            sys_word = response.json()['word']
            round_num = response.json()['round']
            sleep(1)

        if round_id > 1:
            status = requests.get(status_url)

        choosen_word = what_beats(sys_word)
        data = {"player_id": player_id, "word_id": choosen_word, "round_id": round_id}
        response = requests.post(post_url, json=data)

if __name__ == "__main__":
    play_game("f85ZIXKKeG")
