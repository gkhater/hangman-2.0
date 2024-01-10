import uuid

def collect_game_data(target_word, result, sequence, tries): 
    game_id = generate_game_id()

    game_data = {
        "Target word"     : target_word, 
        "Game Result "    : result, 
        "Tries used"      :tries, 
        "Game evolution"  : sequence
        }

    return game_id, game_data
    
         

def generate_game_id():
    # Generate a random UUID and convert it to a string
    #about 2^128 different combinations ==> high probability of uniqueness

    game_id = str(uuid.uuid4())
    return game_id



        