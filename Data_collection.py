import json
import uuid

def collect_game_data(target_word, result, sequence): 
    game_id = generate_game_id()

    return {
         game_id : {
              "Target word"     : target_word, 
              "Game Result "        : result, 
              "Game evolution"  : sequence
         }
    }

def generate_game_id():
    # Generate a random UUID and convert it to a string
    #about 2^128 different combinations ==> high probability of uniqueness

    game_id = str(uuid.uuid4())
    return game_id



        