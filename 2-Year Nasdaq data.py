import requests
import pandas as pd

#this a list of Nasdaq top 100 companines, I've downloaded it manually
df_list = pd.read_csv('0-nasdaq_companies.csv')
list_apprs = list(df_list['app'])
list_names = list(df_list['company_name'])
#defining my empty dataframe to load all the data insie
col = ['Date','Open','High','Low','Close','Adj Close','Volume','app']
df_all = pd.DataFrame(columns=col)

#files counter
i = 3
#I've found the link from yahoo, finances, I can change the start and finish date depending on user options
for appr in list_apprs:
    url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1=1432425600&period2=1621814400&interval=1d&events=history&includeAdjustedClose=true'.format(appr)

#opening a new csv file to save the company data inside
    with requests.get(url) as rq:
        with open ('{}-{}.csv'.format(i, appr),'wb') as f:
            f.write(rq.content)

#adjuting file data, by adding the company appreviation & adding the company data into my big dataframe
    df = pd.read_csv('{}-{}.csv'.format(i,appr))
    df['app'] = appr
    df.to_csv('{}-{}.csv'.format(i,appr), index=False)
    df_all = df_all.append(df)
    i +=1

#adding company name by vlookup, and saving the whole list in a csv file
df_all = pd.merge(df_all,df_list, on='app',how='left')
df_all.to_csv('1-all_list.csv', index=False)