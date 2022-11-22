import pandas as pd
import numpy as py
import math
import datetime
from pandasql import sqldf

pd.options.mode.chained_assignment = None  # default='warn'
pd.set_option('display.max_columns', None, 'display.max_rows', None)  
pd.set_option('display.expand_frame_repr', False)

# create dataframe with all the 5 letter words
#words = pd.read_csv("data/5letter.csv", usecols=['p1','p2','p3','p4','p5'])
#words = pd.read_csv("data/5letter.csv", usecols=['word'])

def display_rankings(word_list):
    #initially i just read rankings from a file, now create them
    #rankings = pd.read_csv("data/rankings.csv", usecols=['First','FirstRank','Second','SecondRank','Third','ThirdRank','Fourth','FourthRank','Fifth','FifthRank'])
#word_list = words["word"].to_numpy()
    #print(word_list)
    #print(rankings)
    #turn word_list into a df
    rankings = pd.DataFrame(word_list,columns = ['word'])
    #print("rankings")
    #print(rankings)
    rankings['First'] = rankings['word'].str[0]
    rankings['Second'] = rankings['word'].str[1]
    rankings['Third'] = rankings['word'].str[2]
    rankings['Fourth'] = rankings['word'].str[3]
    rankings['Fifth'] = rankings['word'].str[4]
    #print("rankings")
    #print(rankings)
    # do the first column creating the df
    query = "select First, count(First) as firstcount from rankings where first is not null group by first order by count(first) desc"
    #query = "select "
    df_qry = sqldf(query)

    # add to the df_qry from now on 
    query = "select second, count(second) secondcount from rankings where second is not null group by second order by count(second) desc"
    df_tmp = sqldf(query)
    df_qry = pd.concat([df_qry, df_tmp], axis=1)

    # add to the df_qry from now on 
    query = "select third, count(third) thirdcount from rankings where third is not null group by third order by count(third) desc"
    df_tmp = sqldf(query)
    df_qry = pd.concat([df_qry, df_tmp], axis=1)

    # add to the df_qry from now on 
    query = "select Fourth, count(Fourth) fourthcount from rankings where Fourth is not null group by Fourth order by count(Fourth) desc"
    df_tmp = sqldf(query)
    df_qry = pd.concat([df_qry, df_tmp], axis=1)

    # add to the df_qry from now on 
    query = "select fifth, count(fifth) fifthcount from rankings where fifth is not null group by fifth order by count(fifth) desc"
    df_tmp = sqldf(query)
    df_qry = pd.concat([df_qry, df_tmp], axis=1)

    #print("df_qry")
    #print(df_qry)
    df_qry.fillna(0,inplace=True)
    print(df_qry)
    df_qry.to_csv('data/r.csv', index=False)

    # this is the df that will hold the words and the scores

    empDfobj = pd.DataFrame(word_list, columns = ['guess'])
    #add a column for score
    empDfobj['score'] =999

    #for each word
    pos = 0

    for wd in word_list:
        score = 0
        result = df_qry['First'].isin([wd[0]]) #create a series of booleans will have one True for the row that matches
        #print(result)
        y = 0
        for x in result:  #iterate through the series of booleans to find the true
            if x:     # this is the one true
                score = score + df_qry['firstcount'].map(int).iloc[y]
                #print("word " + wd)
                #print("x " + str(x))
                #print("y " + str(y))
                #print("from matrix")
                #print(df_qry['firstcount'].map(int).iloc[y])
                #print("score " + str(score))
            else:
                y = y +1

        result = df_qry['Second'].isin([wd[1]]) #create a series of booleans will have one True for the row that matches
        #print(result)
        y = 0
        for x in result:  #iterate through the series of booleans to find the true
            if x:     # this is the one true
                score = score + df_qry['secondcount'].iloc[y]
                #print("word " + wd)
                #print("x " + str(x))
                #print("y " + str(y))
                #print(result)
                #print(df_qry['firstcount'].map(int).iloc[y])
                #print("score " + str(score))
            else:
                y = y +1
        result = df_qry['Third'].isin([wd[2]]) #create a series of booleans will have one True for the row that matches
        #print(result)
        y = 0
        for x in result:  #iterate through the series of booleans to find the true
            if x:     # this is the one true
                score = score + df_qry['thirdcount'].iloc[y]
                #print("word " + wd)
                #print("x " + str(x))
                #print("y " + str(y))
                #print(result)
                #print(df_qry['firstcount'].map(int).iloc[y])
                #print("score " + str(score))
            else:
                y = y +1
                
        result = df_qry['Fourth'].isin([wd[3]]) #create a series of booleans will have one True for the row that matches
        #print(result)
        y = 0
        for x in result:  #iterate through the series of booleans to find the true
            if x:     # this is the one true
                score = score + df_qry['fourthcount'].iloc[y]
                #print("word " + wd)
                #print("x " + str(x))
                #print("y " + str(y))
                #print(result)
                #print(df_qry['firstcount'].map(int).iloc[y])
                #print("score " + str(score))
            else:
                y = y +1
        
        result = df_qry['Fifth'].isin([wd[4]]) #create a series of booleans will have one True for the row that matches
        #print(result)
        y = 0
        for x in result:  #iterate through the series of booleans to find the true
            if x:     # this is the one true
                score = score + df_qry['fifthcount'].iloc[y]
                #print("word " + wd)
                #print("x " + str(x))
                #print("y " + str(y))
                #print(result)
                #print(df_qry['firstcount'].map(int).iloc[y])
                #print("score " + str(score))
            else:
                y = y +1
        
        #now we are at the bottom of the for loop
        #update the score for this word
        empDfobj['score'].iloc[pos] = score
        pos = pos + 1
    #print("empDfobj")    
    #print(empDfobj)
    d_sor = empDfobj.sort_values('score', ascending = False)
    print("sorted")
    print(d_sor)
    d_sor.to_csv('data/res.csv', index=False)
   # print(rankings)
    #print(type(df_qry))

#some = ('trace','every','quick','apple')
#some = ('trace','every','salet','quick','homey','river','stink','shoes','giant','pound','gayly')
#display_rankings(some)