import pandas
import numpy


index_cols=['Client Name','Client City','ZIP','year','Owner Type Code']
df = pandas.read_csv('inputs/chargers/alt_fuel_stations (Jan 2 2024).csv')
out_dir = 'outputs/chargers/'


df['ZIP'] = df['ZIP'].astype(str)
clients = pandas.read_csv('inputs/common/clients.csv')
clients['ZIP_CODE'] = clients['ZIP_CODE'].astype(str)

df[df['Fuel Type Code']=='ELEC'] #EV chargers only
df['year'] = pandas.to_datetime(df['Open Date']).dt.year
df['year'] = numpy.where(df['year'].isnull(),'unknown',df['year'])

df = df.merge(right=clients,left_on = 'ZIP',right_on = 'ZIP_CODE',how='left',copy=True)
print(df.columns)

for i in index_cols:
    df[i] = numpy.where(df[i].isnull(),'unknown',df[i])
    #assert not df[i].isnull().any(),'null vals in '+i

df = pandas.pivot_table(data=df,
                        values=['EV Level1 EVSE Num','EV Level2 EVSE Num', 'EV DC Fast Count'],
                        index=index_cols,
                        aggfunc=sum)
df.reset_index(inplace=True)
df.to_csv(out_dir+'chargers_by_year_and_zip.csv',index=False)        
