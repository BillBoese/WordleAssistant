'''Source filel for ansFn wordle coloring function'''

import pandas as pd

#gs = [5,2]
#gs = [[' ', ' '],[' ',' '],[' ',' '],[' ',' '],[' ',' ']]

def ansFn(guess, answer, anslist):

    # build the first column in the 2d array with just the letter
    # do the color after
    #print(guess)
    #print(answer)

    pl =[True, True, True, True, True]
    ym =[True, True, True, True, True]

    for x in range(5):
        anslist[x][0] = guess[x]

    for x in range(5):  #green loop
        if guess[x] == answer[x]:  #easy it is green
            anslist[x][1] = 'green'
            pl[x] = False
            ym[x] = False

    #print(pl)
    #print(ym)
    #print(" ")

    for x in range(5):  #gray loop
        if pl[x]:   # this position is not green
            #print(guess[x])
            m = False
            for y in range(5):
                if pl[y]:
                    #print(answer[y])
                    if guess[x] == answer[y]:
                        m = True  # m starts false if it is never found it is gray
                        if ym[y]:
                            anslist[x][1] = 'yellow'
                            #print("found: yellow")
                            ym[y] = False
                        else:
                            anslist[x][1] = 'gray'
                            #print("not found inner: gray")            
            if not m:
                anslist[x][1] = 'gray'
                #print("not found catch all: gray")
            
            '''
            for y in range(5):
                if ym[y]:                     #it was found somewhere it is yellow
                    if guess[x] == answer[y]:
                        anslist[x][1] = 'yellow'
                        ym[y] = False
                        #print("found: yellow")
                else:
                    anslist[x][1] = 'gray'
                    #print("not found catch all: gray")
            #else:
            #    anslist[x][1] = 'gray'
            #    #print("other: gray")
'''
        #check if all positions are green, ie its solved
            #print(ym)
        #print(pl)
    if not any(pl):
        return True
    else:
        return False
#if ansFn("salet", "mummy", gs):
#    print("it returned true")

#print(gs)