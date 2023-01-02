''' Ranking function using duck DB'''
import pandas as pd
import duckdb
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
    query = "select First, count(First) as firstcount from rankings where first is not null group by first order by count(first) desc"
    # df_qry = sqldf(query)
    df_qry = duckdb.query(query).to_df()

    # add to the df_qry from now on
    query = "select second, count(second) secondcount from rankings where second is not null group by second order by count(second) desc"
    # df_tmp = sqldf(query)
    df_tmp = duckdb.query(query).to_df()
    df_qry = pd.concat([df_qry, df_tmp], axis=1)

    # add to the df_qry from now on
    query = "select third, count(third) thirdcount from rankings where third is not null group by third order by count(third) desc"
    #df_tmp = sqldf(query)
    df_tmp = duckdb.query(query).to_df()
    df_qry = pd.concat([df_qry, df_tmp], axis=1)

    # add to the df_qry from now on
    query = "select Fourth, count(Fourth) fourthcount from rankings where Fourth is not null group by Fourth order by count(Fourth) desc"
    #df_tmp = sqldf(query)
    df_tmp = duckdb.query(query).to_df()
    df_qry = pd.concat([df_qry, df_tmp], axis=1)

    # add to the df_qry from now on
    query = "select fifth, count(fifth) fifthcount from rankings where fifth is not null group by fifth order by count(fifth) desc"
    #df_tmp = sqldf(query)
    df_tmp = duckdb.query(query).to_df()
    df_qry = pd.concat([df_qry, df_tmp], axis=1)

    df_qry.fillna(0,inplace=True)
    #print(df_qry)
    #df_qry.to_csv('data/r.csv', index=False)

    #Enhancement per user request, refine results to eliminate bias to double letters

    # walk through each position, check for len = 1, if so, set all counts for that pos to 0
    # there is no need to count the occurence when it is green it just skews the result

    if (len(pos[0]) == 1): # this if the first position and it is green
            #set all column values to 0, try this
        df_qry['firstcount'].values[:] = 0
        # now find the location of the value in pos[x][0] and set those values to 0 in each column, this is ugly

    if (len(pos[1]) == 1):
        df_qry['secondcount'].values[:] = 0

    if (len(pos[2]) == 1):
        df_qry['thirdcount'].values[:] = 0

    if (len(pos[3]) == 1):
        df_qry['fourthcount'].values[:] = 0

    if (len(pos[4]) == 1):
        df_qry['fifthcount'].values[:] = 0

    #print(df_qry)

    # tweak the counts again, reduce the score for words that have doubles in
    # i.e. if it is green give it a score of zero in other positions too

    fine = df_qry.isin(greens)
    #print(fine)

    for idx in fine.index:
        if (fine['First'][idx]):
            df_qry['firstcount'][idx] = 0
        if (fine['Second'][idx]):
            df_qry['secondcount'][idx] = 0
        if (fine['Third'][idx]):
            df_qry['thirdcount'][idx] = 0
        if (fine['Fourth'][idx]):
            df_qry['fourthcount'][idx] = 0
        if (fine['Fifth'][idx]):
            df_qry['fifthcount'][idx] = 0

    #print(df_qry)

    # this is the df that will hold the words and the scores

    empDfobj = pd.DataFrame(word_list, columns = ['guess'])
    #add a column for score
    empDfobj['score'] =999

    #for each word
    ps = 0

    for wd in word_list:
        score = 0
        result = df_qry['First'].isin([wd[0]]) #create a series of booleans will have one True for the row that matches
        #print(result)
        y = 0
        for x in result:  #iterate through the series of booleans to find the true
            if x:     # this is the one true
                score = score + df_qry['firstcount'].map(int).iloc[y]
            else:
                y = y +1

        result = df_qry['Second'].isin([wd[1]]) #create a series of booleans will have one True for the row that matches
        #print(result)
        y = 0
        for x in result:  #iterate through the series of booleans to find the true
            if x:     # this is the one true
                score = score + df_qry['secondcount'].iloc[y]
            else:
                y = y +1
        result = df_qry['Third'].isin([wd[2]]) #create a series of booleans will have one True for the row that matches
        #print(result)
        y = 0
        for x in result:  #iterate through the series of booleans to find the true
            if x:     # this is the one true
                score = score + df_qry['thirdcount'].iloc[y]
            else:
                y = y +1
                
        result = df_qry['Fourth'].isin([wd[3]]) #create a series of booleans will have one True for the row that matches
        #print(result)
        y = 0
        for x in result:  #iterate through the series of booleans to find the true
            if x:     # this is the one true
                score = score + df_qry['fourthcount'].iloc[y]
            else:
                y = y +1
        
        result = df_qry['Fifth'].isin([wd[4]]) #create a series of booleans will have one True for the row that matches
        #print(result)
        y = 0
        for x in result:  #iterate through the series of booleans to find the true
            if x:     # this is the one true
                score = score + df_qry['fifthcount'].iloc[y]
            else:
                y = y +1
        
        #now we are at the bottom of the for loop
        #update the score for this word
        empDfobj['score'].iloc[ps] = score
        ps = ps + 1
    #print("empDfobj")    
    #print(empDfobj)
    d_sor = empDfobj.sort_values('score', ascending = False)
    #print("sorted")
    #print(d_sor)
    return d_sor['guess'].iloc[0]

    # d_sor.to_csv('data/res.csv', index=False)
    # print(rankings)
    #print(type(df_qry))

#some = ('trace','every','quick','apple')
#some = ('trace','every','salet','quick','homey','river','stink','shoes','giant','pound','gayly')
#display_rankings(some)
