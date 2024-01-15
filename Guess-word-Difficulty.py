import csv
import nltk
import pandas as pd

from Decision_Tree import DecisionTree
from nltk.corpus import words, cmudict, reuters
from collections import defaultdict
import math


nltk.download("words")
nltk.download('cmudict')
nltk.download('reuters')

# Get a list of English words from the 'words' corpus
english_words = words.words()

csv_file = './Word-Difficulty/Labelled_difficulty.csv'
games_data = [] 
phonetic_dict = cmudict.dict()
letters = reuters.words()
bigram_freq = defaultdict(lambda: 0.01)  # Avoid zero frequency

''' 
This evaluates the frequency of all possible bigrams in the english language
Note: this frequency is independant of the frequency of the word
'''

for word in letters:
    word = word.lower()
    for i in range(len(word) - 1):
        bigram = word[i:i+2]
        if bigram.isalpha():
            bigram_freq[bigram] += 1

total_bigrams = sum(bigram_freq.values())


def get_info(row): 
    def calculate_word_regularity(word):
        def bigram_probability(word):
            prob = 0
            for i in range(len(word) - 1):
                bigram = word[i:i+2]
                prob += math.log(bigram_freq[bigram] / total_bigrams)
                
            return prob / (len(word) - 1)
        
        def phonetic_consistency(word):
            word_phonetic = phonetic_dict.get(word.lower())
            if word_phonetic:
                # Use the first pronunciation variant
                phonetic_word = ''.join([phoneme for phoneme in word_phonetic[0] if phoneme.isalpha()])
                # Calculate Levenshtein distance (edit distance)
                return nltk.edit_distance(word.lower(), phonetic_word) / max(len(word), len(phonetic_word))
            else:
                return 1 #max irregularity for words not in the dictionnary
            
        # Higher values for bigram_probability indicate more regularity
        bigram_prob = bigram_probability(word)
        # Lower values of phonetic_consistency indicate more regularity
        phonetic_consist = phonetic_consistency(word)

        # Bigram probability is negative, so we invert it to make higher values indicate more regularity
        normalized_bigram_score = (1 / (1 + math.exp(-bigram_prob))) #normalized using the sigmoid function
        normalized_phonetic_score = (1 - phonetic_consist) #normalized to fit the same scale, where higher values also indicate more regularity.

        # Weighted average 
        #Note: Weight could be tweeked for possibly better improvement
        regularity_score = (0.66 * normalized_bigram_score) + (0.34 * normalized_phonetic_score)

        return regularity_score

    def calculate_different_letter_ratio(word):
        unique_letters = set(word)
        
        num_different_letters = len(unique_letters)
        word_length = len(word)
        

        return num_different_letters / word_length

    def calculate_word_frequency(word):
        word_count = english_words.count(word)
        return word_count

    def calculate_vowel_to_consonant_ratio(word):
        vowels = "aeiou"
        vowels_count = 0 
        

        for letter in word: 
            if letter in vowels: 
                vowels_count += 1

        return vowels_count / len(word)

    def calculate_average_letter_frequency(word):
        ''' 
        Different Letter frequencies in the English Language
        source: https://en.wikipedia.org/wiki/Letter_frequency
        '''
        letterFrequency = {
            'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97,
            'n': 6.75, 's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25,
            'l': 4.03, 'c': 2.78, 'u': 2.76, 'm': 2.41, 'w': 2.36,
            'f': 2.23, 'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.49,
            'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15, 'q': 0.10,
            'z': 0.07
        }


        total_frequency = 0.0
        word_length = len(word)


        for letter in word: 
            total_frequency += letterFrequency[letter]


        return total_frequency / word_length
    
    game_id, word_to_guess, difficulty = row

    word_length = len(word_to_guess)
    average_letter_frequency = calculate_average_letter_frequency(word_to_guess)
    vowel_to_consonant__ratio = calculate_vowel_to_consonant_ratio(word_to_guess)
    word_frequency = calculate_word_frequency(word_to_guess)
    different_letters_ratio = calculate_different_letter_ratio(word_to_guess)
    word_regularity = calculate_word_regularity(word_to_guess)

    # return {
    #     "game id"               : game_id, 
    #     "word to guess"         : word_to_guess, 
    #     "difficulty"            : difficulty,
    #     "length"                : word_length, 
    #     "average letter freq"   : average_letter_frequency, 
    #     "vowel ratio"           : vowel_to_consonant__ratio, 
    #     "word frequency"        : word_frequency, 
    #     "repeated letters"      : different_letters_ratio, 
    #     "regularity"            : word_regularity      
    # }

    return [
        game_id, 
        word_to_guess, 
        word_length, 
        average_letter_frequency, 
        vowel_to_consonant__ratio, 
        word_frequency, 
        different_letters_ratio, 
        word_regularity,
        difficulty
    ]


# Read the CSV file into a Pandas DataFrame
df = pd.read_csv(csv_file)

# Filter out rows with empty difficulty
df = df[df['difficulty'].notna()]

# Now, iterate through each row in the DataFrame and calculate the additional features
for index, row in df.iterrows():
    difficulty = row['difficulty']
    info = get_info(row)
    df.at[index, 'game_id'] = info[0]
    df.at[index, 'word_to_guess'] = info[1]
    df.at[index, 'word_length'] = info[2]
    df.at[index, 'average_letter_frequency'] = info[3]
    df.at[index, 'vowel_to_consonant_ratio'] = info[4]
    df.at[index, 'word_frequency'] = info[5]
    df.at[index, 'different_letters_ratio'] = info[6]
    df.at[index, 'word_regularity'] = info[7]
    df.at[index, 'difficulty'] = info[8]

# games_data is now a DataFrame
games_data = df