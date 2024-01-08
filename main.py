import random
from Proba import word_list, get_max_proba
import string


def main(statistics = True): 
    if not statistics: 
        isGuesser = get_role_input()
        tries = 7 

        word = get_word_input(isGuesser)
        run_game(tries, word, isGuesser)
    
    else: 
        tries = 32 #unlimited guesses since machine plays against itself
        word = get_word_input(True) #machine generates word
        print(f"--- {word} ---")
        run_game(tries,word, False) #machine guesses the word 
    
    return

def get_role_input():
    while True:
        user_input = input("Do you want to guess? [Y/N/R]: ").upper()
        if user_input == 'Y':
            return True
        elif user_input == 'N':
            return False
        elif user_input == 'R':
            return random.choice([True, False])
        else:
            print("Invalid input. Please enter 'Y', 'N', or 'R'.")

def get_word_input(isGuesser): 
    if isGuesser: 
        return random.choice(word_list).lower()
     
    while True:
        user_input = input("Please enter your word: ").lower()
        if user_input in word_list: 
            return user_input
        else: 
            print("Invalid word, Please try another")

def get_guess_input_(valid_letters, isGuesser, word, short_list): 
    if not isGuesser: 
        return get_max_proba(word, short_list, valid_letters)
    else: 
        while True: 
            user_input = input("Please enter your guess: ").lower()
            if len(user_input) == 1 and user_input in valid_letters:  
                return user_input
            else: 
                print("invalid guess")

def run_game(tries, word, isGuesser): 
    won = False
    valid_letters = set(string.ascii_lowercase)
    guess_word = list("*"*len(word))
    short_list = [match.lower() for match in word_list if len(match) == len(word)]

    while tries > 0 : 
        print(f"{''.join(guess_word)} \n")
        guess = get_guess_input_(valid_letters, isGuesser, guess_word, short_list)
        valid_letters.remove(guess)
        indexes = []

        if guess not in word: 
            tries -= 1
            print(f"{guess} not in word, you have {tries} tries left ")
            
            if not isGuesser: 
                i = 0 
                while i < len(short_list):
                    if guess in short_list[i]: 
                        short_list.pop(i)
                    else: 
                        i += 1
        else:  
            indexes = [index for index, char in enumerate(word) if char == guess]
            for i in indexes: 
                guess_word[i] = guess

            if not isGuesser: 
                i = 0 
                while i < len(short_list):
                    element = short_list[i]
                    if guess not in element: 
                        short_list.pop(i)
                    else: 
                        if [index for index, char in enumerate(element) if char == guess] != indexes: #check if the position(s) of the guessed letter don't  match
                            short_list.pop(i)
                        else: #if list remains unchanged
                            i += 1

            if ''.join(guess_word) == word:
                tries = 0
                won = True
    
    if won: 
        print(f"Congratulations, you have won, the word was: {word}")
    else: 
        print(f"You are out of tries, you have lost, the word was: {word}")        

        
if __name__ == "__main__": 
    while True: 
        main()
