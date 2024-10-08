import pandas
import os
import sys

input_dir = 'inputs/vehicles/'
output_dir = 'outputs/vehicles/'
clients = pandas.read_csv('inputs/common/clients.csv')
clients['ZIP_CODE'] = clients['ZIP_CODE'].astype(str)
files = [i for i in os.listdir(input_dir) if i.startswith('vehicle')]

big_df = pandas.DataFrame()
for i in files:
    df = pandas.read_csv(input_dir+i)
    df.rename(columns={'ZIP Code': 'Zip Code'}, inplace=True) #Added August 2024 to deal with misnamed 2023 file
    df['Zip Code'] = df['Zip Code'].astype(str)
    big_df = pandas.concat([df,big_df])

big_df = pandas.pivot_table(data=big_df,values=['Vehicles'],index=['Date','Fuel','Zip Code','Duty'],aggfunc=sum)
big_df.reset_index(inplace=True)
big_df = big_df.merge(right=clients,left_on='Zip Code',right_on='ZIP_CODE',how='left',copy=True)



raise BaseException
big_df.to_csv(output_dir+'vehicle_counts.csv',index=False)