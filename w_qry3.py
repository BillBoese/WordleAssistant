'''Interactive main using old original ranking and inline word filter'''
#import math
import pandas as pd
#import numpy as py
#import datetime

from fn_rank2 import display_rankings
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

#this one calls a rank function to try to rank remaining words, its clever but meaningless
#include tatty bug update

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

    #tatty bug
    c = []
    c = [i[0] for i in ans]

    #print(ans[0][0])
    #print(ans[0][1])

    # reduce character position arrays
    # loop through the array of responses
    # first check for green, thats easy
    
    for r in range(5):           #one loop for each answer
        if ans[r][1] == 'green':  #need to add logic to remove letter that goes from yellow to green
            pos[r] = [ans[r][0]]  #also need to update yellow mask
            p[r] = True
            # add to list of greens if not there
            if ans[r][0] not in greens:
                greens.append(ans[r][0])
            #lastly check the yellow list to see if this was in there, if it was remove it
            b = 0
            for z in yel:
                if ans[r][0] == z: #yel[b]: #tatty bug update
                #if (ans[r][0] == yel[b]) and (ans[r][0] not in ans[0:r][0]): 
                    if ans[r][0] not in c[:r]: #this cond for tatty bug green before gray
                        yel.pop(b)
                    elif len(can_occ_only_once) > 0:
                        #gray before green
                        yel.pop(b)
                b = b + 1
        elif ans[r][1] == 'gray':  #remove character from all positions,except when this char is already yellow
            if ans[r][0] in yel: # answer is a duplicate its gray now but was yellow before
                pos[r].remove(ans[r][0]) # then just remove it from its current position
                can_occ_only_once.append(ans[r][0])
            else:  #it just isnt in the answer
                for z in range(5):
                    #try:
                    #    pos[z].remove(ans[r][0])
                    #except ValueError:
                    #    pass
                    if len(pos[z]) > 1: #i.e. its not green
                        try:
                            pos[z].remove(ans[r][0])
                        except ValueError:
                            pass

        else:  #yellow
            #remove character from this position only
            try:
                pos[r].remove(ans[r][0])
            except ValueError:
                pass
            if ans[r][0] not in yel: #add to list of yellows
                yel.append(ans[r][0])

    for q in range(5):
        print(pos[q])
    print("Yellows")
    print(yel)
    print("Greens")
    print(greens)
    print("Can only occ once")
    print(can_occ_only_once)

    # ok now for the list of possible words.

    for wrd in word_list:
        #print(wrd)
        match = True
        for j in range(5):     #for loop through each letter in word, if one not match break
            if wrd[j:j+1] not in pos[j]:
                match = False
            #if q[2] == pos[1][8]:
                    #print("match")
        if match:
            # put the check for wrd against the yellow mask here
            # check each letter of the word against the mask it's position should
            # match a true in the mask as well as at least one of the yellows in one
            # of those spaces
            sh = ''
            for w, q in zip(wrd, range(5)): #need to shorten the word, loop through each letter
                if not p[q]:        #if the position isnt green
                    sh = sh + w    # add character to end of string, now we have the part of the word to match
                #print(sh)
            all_in = all([char in sh for char in yel]) #this bit down here doesnt accomodate duplicates where one is yellow
            if all_in:    # really need to remove chars from yel when they are found, still work to be done
                tempword_list.append(wrd)

        #break

    # need a logic filter for yellow letters make sure both are in the words just in different positions
    # i.e. not where they were guessed, not where there is a green
    #print(p)
    #print(tempword_list)
    display_rankings(tempword_list, pos, greens)
    word_list = tempword_list
    tempword_list = []
    