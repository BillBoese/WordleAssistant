'''Main test harness for bulk testing'''

import pandas as pd
from tester2 import ansFn
from sol_finder import wordFilter
from fn_rank4 import display_rankings
from datetime import datetime

#I didnt do a good job of designing this modular

# create dataframe with all the 5 letter words
st_guess = "slice" # hardcoded for first guess, change later
words = pd.read_csv("data/5letter.csv", usecols=['word'])
word_list = words["word"].to_numpy()
#word_list = ['broke','salet']
results_df = pd.DataFrame(columns=['guess', 'word', 'num_guesses'])


gs = [5,2]
gs = [[' ', ' '],[' ',' '],[' ',' '],[' ',' '],[' ',' ']]

# loop through each word, as they will be the answers

for word in word_list:
    #figure out colors for letters
    guess = st_guess
    sol_words = word_list
    int_words = []
    pos = [["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r",
        "s","t","u","v","w","x","y","z"],
       ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r",
       "s","t","u","v","w","x","y","z"],
       ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r",
       "s","t","u","v","w","x","y","z"],
       ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r",
       "s","t","u","v","w","x","y","z"],
       ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r",
       "s","t","u","v","w","x","y","z"]]

    p =[False,False,False,False,False]

    yel = []
    can_occ_only_once = [] # the case where you have a yellow then gray these
    greens = []            # chars can only occur once in answer

    guesses = 0

    for x in range(1,10):
        #print(len(int_words))
        guesses = guesses + 1
        if ansFn(guess,word,gs):
            break
        else:
            #filter function pass it the gs array and the current wordlist
            int_words = wordFilter(sol_words, gs, pos, yel, can_occ_only_once, greens,p)
            guess = display_rankings(int_words, pos, greens)
    res_row = [st_guess,word,guesses]
    results_df.loc[len(results_df)] = res_row
    #if len(results_df) >= 500:
    #    break
#print(results_df)
tstamp = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
fname = "data/results_" + st_guess + "_fn_rank4_" + tstamp + ".csv"
results_df.to_csv(fname, index=False)
