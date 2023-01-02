''' Ranking function using pandas simplified for performance'''
import pandas as pd
#import duckdb
#from pandasql import sqldf

pd.options.mode.chained_assignment = None  # default='warn'
pd.set_option('display.max_columns', None, 'display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

# create dataframe with all the 5 letter words
#words = pd.read_csv("data/5letter.csv", usecols=['p1','p2','p3','p4','p5'])
#words = pd.read_csv("data/5letter.csv", usecols=['word'])

def display_rankings(word_list, pos, greens):
    #turn word_list into a df
    rankings = pd.DataFrame(word_list,columns = ['word'])
    #print(rankings)
    rankings['First'] = rankings['word'].str[0]
    rankings['Second'] = rankings['word'].str[1]
    rankings['Third'] = rankings['word'].str[2]
    rankings['Fourth'] = rankings['word'].str[3]
    rankings['Fifth'] = rankings['word'].str[4]
    #print("rankings")
    #print(rankings)
    # do the first column creating the df
    fcnt = rankings['First'].value_counts()
    scnt = rankings['Second'].value_counts()
    tcnt = rankings['Third'].value_counts()
    xcnt = rankings['Fourth'].value_counts()
    ycnt = rankings['Fifth'].value_counts()

    if (len(pos[0]) == 1): # this if the first position and it is green
            #set all column values to 0, try this
        #df_qry['firstcount'].values[:] = 0
        fcnt.iloc[:] = 0
        # now find the location of the value in pos[x][0] and set those values to 0 in each column, this is ugly

    if (len(pos[1]) == 1):
        #df_qry['secondcount'].values[:] = 0
        scnt.iloc[:] = 0

    if (len(pos[2]) == 1):
        #df_qry['thirdcount'].values[:] = 0
        tcnt.iloc[:] = 0

    if (len(pos[3]) == 1):
        #df_qry['fourthcount'].values[:] = 0
        xcnt.iloc[:] = 0

    if (len(pos[4]) == 1):
        #df_qry['fifthcount'].values[:] = 0
        ycnt.iloc[:] = 0

    for green in greens:
        fcnt[green] = 0
        scnt[green] = 0
        tcnt[green] = 0
        xcnt[green] = 0
        ycnt[green] = 0

    # this is the df that will hold the words and the scores

    empDfobj = pd.DataFrame(word_list, columns = ['guess'])
    #add a column for score
    empDfobj['score'] =999

    #for each word
    ps = 0

    for wd in word_list:
        score =0
        score = fcnt[wd[0]] + scnt[wd[1]] + tcnt[wd[2]] + xcnt[wd[3]] + ycnt[wd[4]]
        #update the score for this word
        empDfobj['score'].iloc[ps] = score
        ps = ps + 1

    d_sor = empDfobj.sort_values('score', ascending = False)
    #print(d_sor)
    return d_sor['guess'].iloc[0]
