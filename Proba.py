import nltk
from nltk.corpus import words
import string


nltk.download("words")
word_list = words.words()

def get_all_probas(word, short_list, alphabet): 
    probas = dict()

    for letter in alphabet: 
        probas[letter] = get_letter_proba(letter, short_list)

    return probas

def get_letter_proba(letter, short_list):
    total = len(short_list) 
    count = 0
    for word in short_list: 
        if letter in word: 
            count += 1

    return count/total

def get_max_proba(word, short_list, alphabet): 
    probas = get_all_probas(word, short_list, alphabet)
    return max(probas, key = probas.get)

