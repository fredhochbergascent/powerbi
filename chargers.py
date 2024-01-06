import pandas
import numpy

index_cols=['Client Name','Client City','ZIP','year','Owner Type Code']
df = pandas.read_csv('inputs/chargers/alt_fuel_stations (Jan 2 2024).csv')
df['ZIP'] = df['ZIP'].astype(str)
clients = pandas.read_csv('inputs/common/clients.csv')
clients['ZIP_CODE'] = clients['ZIP_CODE'].astype(str)
out_dir = 'outputs/chargers/'

#Check
for i in ['EV Level1 EVSE Num','EV Level2 EVSE Num', 'EV DC Fast Count']:
    df[i] = df[i].fillna(value=0)
    print(i+' total chargers before: ',df[i].sum())

df[df['Fuel Type Code']=='ELEC'] #Keep EV chargers only
#Get year and delete unknown years from data
df['year'] = None
for i in ['Open Date','Expected Date','Date Last Confirmed']:
    df['year'] = numpy.where(df['year'].isnull(),
        pandas.to_datetime(df[i]).dt.year,
        df['year'])
assert not df['year'].isnull().any(),'null vals present'
df['year'] = df['year'].astype(int)



df = df.merge(right=clients,left_on = 'ZIP',right_on = 'ZIP_CODE',how='left',copy=True)

#Fill blanks
for i in index_cols:
    df[i] = numpy.where(df[i].isnull(),'unknown',df[i])




#Reshape data to get cumulative counts. Need to generate data for missing year/zip code combos.
#Unfortunately this means a pivot table to make an observation for every year
#then a melt to extract info we need, then another pivot to make it PowerBI friendly.
df = pandas.pivot_table(data=df,
                        values=['EV Level1 EVSE Num','EV Level2 EVSE Num', 'EV DC Fast Count'],
                        index=['Client Name','Client City','ZIP'],
                        columns=['year'],
                        aggfunc=sum)
df.reset_index(inplace=True)


flattened_columns = [''.join(map(str, col)).strip() for col in df.columns]
df.columns = flattened_columns
for i in df.columns:
    if i.startswith('EV'):
        df[i] = df[i].fillna(value=0)

#Extract year and charger type
df = df.melt(id_vars = ['Client Name','Client City','ZIP'])
df['year'] = df['variable'].str[-4:].astype(int)
df['charger_type'] = df['variable'].str[0:-4]
df = df.pivot(columns='charger_type',index=['Client Name','Client City','ZIP','year'],values='value')
df.reset_index(inplace=True)

#Get cumulative totals
df.sort_values(by=['Client Name','Client City','ZIP','year'],inplace=True)
for i in ['EV Level1 EVSE Num','EV Level2 EVSE Num', 'EV DC Fast Count']:
    df['Cumulative Total '+i] = df.groupby(['Client Name','Client City','ZIP'])[i].cumsum()

#Check
for i in ['EV Level1 EVSE Num','EV Level2 EVSE Num', 'EV DC Fast Count']:
    print(i+' total chargers before: ',df[i].sum())


df.to_csv(out_dir+'chargers_by_year_and_zip.csv',index=False)





'''
df = pandas.pivot_table(data=df,
                        values=['EV Level1 EVSE Num','EV Level2 EVSE Num', 'EV DC Fast Count'],
                        index=['Client Name','Client City','ZIP','year'],
                        aggfunc=sum)
df.reset_index(inplace=True)


df.sort_values(by=['Client Name','Client City','ZIP','year'],inplace=True)
for i in ['EV Level1 EVSE Num','EV Level2 EVSE Num', 'EV DC Fast Count']:
    df['Cumulative Total '+i] = df.groupby(['Client Name','Client City','ZIP'])[i].cumsum()


df.to_csv(out_dir+'chargers_by_year_and_zip.csv',index=False)        


df = pandas.pivot_table(data=df,
                        values=['EV Level1 EVSE Num','EV Level2 EVSE Num', 'EV DC Fast Count'],
                        index=index_cols,
                        aggfunc=sum)


for i in ['EV Level1 EVSE Num','EV Level2 EVSE Num', 'EV DC Fast Count']:
    df['Cumulative Total '+i] = df.groupby(['Client Name','year'])[i].cumsum()

#raise BaseException

'''