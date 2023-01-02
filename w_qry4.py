'''Interactive program using new functions for filter and ranking'''
#import math
import pandas as pd
from sol_finder import wordFilter
from fn_rank4 import display_rankings
#import numpy as py
#import datetime

#from fn_rank2 import display_rankings
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

#this one calls a rank function to try to rank remaining words, its clever but meaningless

# create dataframe with all the 5 letter words
#words = pd.read_csv("data/5letter.csv", usecols=['word','p1','p2','p3','p4','p5'])
words = pd.read_csv("data/5letter.csv", usecols=['word'])
#word_list = words.values.tolist()
word_list = words["word"].to_numpy()
tempword_list = []
#print(word_list)

# Preview first 5 lines of the file loaded
#print(words.head())
#print(words.tail())

# lets try this first, start with an array of all the positions with all
# possible letters

#pos = [5,2]

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

# not loving this but create an array of letter in the answer in the wrong position
yel = []
can_occ_only_once = [] # the case where you have a yellow then gray these
greens = []            # chars can only occur once in answer

SOLVED = False

# add in a Welcome message
print(" ")
print("Welcome to WordleAssistant version 3.0")
print(" ")
print("...all the help you will ever need.")
print("")

# take in input for the guess, the value and green, yellow gray
# this whole bit needs to be in a while loop to preserve state
# multiple guesses
while not False:
    ans = [5,2]
    ans = [[' ', ' '],[' ',' '],[' ',' '],[' ',' '],[' ',' ']]

    #take in users guess, add input validation later

    for i in range(5):
      #  if p[i]:  #dont reenter green letters if you put this back put it in the loop below too
      #      continue
        print("Enter letter")
        ans[i][0]=input()
        print("Enter color, green, yellow, or gray")
        ans[i][1]=input()

    int_words = wordFilter(word_list, ans, pos, yel, can_occ_only_once, greens,p)
    display_rankings(int_words, pos, greens)
    # need a logic filter for yellow letters make sure both are in the words just in different positions
    # i.e. not where they were guessed, not where there is a green
    
    word_list = int_words
    int_words = []
    