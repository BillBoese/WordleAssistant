import pandas as pd

#gs = [5,2]
#gs = [[' ', ' '],[' ',' '],[' ',' '],[' ',' '],[' ',' ']]

def ansFn(guess, answer, anslist):

    # build the first column in the 2d array with just the letter
    # do the color after
    #print(guess)
    #print(answer)

    pl =[True, True, True, True, True]

    for x in range(5):
        anslist[x][0] = guess[x]

    for x in range(5):  #green loop
        if guess[x] == answer[x]:  #easy it is green
            anslist[x][1] = 'green'
            pl[x] = False

    for x in range(5):  #gray loop
        if pl[x]:   # this position is not green
            m = False
            for y in range(5):
                if pl[y]:
                    if guess[x] in answer[y]:
                        m = True  # m starts false if it is never found it is gray
            if not m:
                anslist[x][1] = 'gray'
            else:                         #does this work?
                anslist[x][1] = 'yellow'
    #print(anslist)
    #check if all positions are green, ie its solved
    #print(pl)
    if not any(pl):
        return True
    else:
        return False

#if ansFn("salet", "mummy", gs):
#    print("it returned true")

#print(gs)