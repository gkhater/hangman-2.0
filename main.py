import random
import nltk
from nltk.corpus import words
import string


def main(): 
    isGuesser = get_role_input()
    tries = 7 

    word = get_word_input(isGuesser)
    run_game(tries, word, isGuesser)
    
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
        return random.choice(word_list)
     
    while True:
        user_input = input("Please enter your word: ").lower()
        if user_input in word_list: 
            return user_input
        else: 
            print("Invalid word, Please try another")

def get_guess_input_(valid_letters, isGuesser): 
    if not isGuesser: 
        return
    
    while True: 
        user_input = input("Please enter your guess: ").lower()
        if len(user_input) == 1 and user_input in valid_letters:  
            return user_input
        else: 
            print("invalid guess")

def run_game(tries, word, isGuesser): 
    won = False
    valid_letters = set(set(string.ascii_lowercase))
    guess_word = list("*"*len(word))

    while tries > 0 : 
        print(f"{''.join(guess_word)} \n")
        guess = get_guess_input_(valid_letters, isGuesser)
        valid_letters.remove(guess)

        if guess not in word: 
            tries -= 1
            print(f"wrong, you have {tries} tries left ")

        else: 
            for letter_index in range(len(word)): 
                if word[letter_index] == guess: 
                    guess_word[letter_index] = guess

            if ''.join(guess_word) == word:
                tries = 0
                won = True
    
    if won: 
        print(f"Congratulations, you have won, the word was: {word}")
    else: 
        print(f"You are out of tries, you have lost, the word was: {word}")        

        
if __name__ == "__main__": 
    nltk.download("words")
    word_list = words.words()
    main()
