import pandas
import os

input_dir = 'inputs/vehicles/'
output_dir = 'outputs/vehicles/'
clients = pandas.read_csv('inputs/common/clients.csv')
clients['ZIP_CODE'] = clients['ZIP_CODE'].astype(str)
files = [i for i in os.listdir(input_dir) if i.startswith('vehicle')]

big_df = pandas.DataFrame()
for i in files:
    df = pandas.read_csv(input_dir+i)
    df['year'] = pandas.to_datetime(df['Date']).dt.year
    df['Zip Code'] = df['Zip Code'].astype(str)
    big_df = pandas.concat([df,big_df])


big_df = pandas.pivot_table(data=big_df,values=['Vehicles'],index=['year','Fuel','Zip Code','Duty'],aggfunc=sum)
big_df.reset_index(inplace=True)
big_df = big_df.merge(right=clients,left_on='Zip Code',right_on='ZIP_CODE',how='left',copy=True)
big_df.to_csv(output_dir+'vehicle_counts.csv',index=False)



'''
files = [i for i in os.listdir('input') if i.startswith('vehicle')]
mapping = pandas.read_csv('input/client_city_census_zip.csv')
mapping['Zip Code'] = mapping['Zip Code'].astype(str)
print(files)

big_df = pandas.DataFrame()
for i in files:
    df = pandas.read_csv('input/'+i)
    df['year'] = int(i[-8:-4])
    df['Zip Code'] = df['Zip Code'].astype(str)
    df = pandas.pivot_table(data=df,values=['Vehicles'],index=['year','Fuel','Zip Code','Duty'],aggfunc=sum)
    df.reset_index(inplace=True)
    big_df = pandas.concat([df,big_df])
    print(df.head())
    #raise BaseException

big_df = big_df.merge(right=mapping,on='Zip Code',how='inner',copy=True)
big_df.to_csv('clean_vehicle_data.csv')
'''
