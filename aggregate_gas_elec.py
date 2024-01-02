import xlrd
import zipfile
import pandas as pd
import numpy
import os
import re
from aggregate_gas_elec_funcs import readin

#TODO: Compare with old CAPS

#Read in lookup tables
renames = dict(pd.read_csv('colnames.csv').values) #Column renames to standardize across datasets
geography = pd.read_csv('California_Zip_Codes.csv')
geography['ZIP_CODE'] = geography['ZIP_CODE'].astype(str)
classes = pd.read_csv('classes.csv')

#Read in files into one big file, adding columns for electric/gas and utility
big_df = pd.DataFrame()
for i in os.listdir('input'):
    df = readin('input/'+i)
    df['dataset']=i
    df.columns = [re.sub(r'[^a-zA-Z0-9]', '',i) for i in df.columns] #Remove special chars from colnames
    if 'Electric' in i or 'ELEC' in i:
        df['elec_or_gas'] = 'electric'
    elif 'GAS' in i or 'Gas' in i:
        df['elec_or_gas'] = 'gas'
    else:
        raise BaseException('Could not classify into electric or gas')   

    if i.startswith('PGE'):
        df['utility']='PG&E'
    elif i.startswith('SCE'):
        df['utility']='SCE'
    elif i.startswith('SCG'):
        df['utility']='SoCalGas'
    elif i.startswith('SDGE'):
        df['utility']='SDG&E'
    else:
        raise BaseException('Could not assign utility')
    
    df.rename(columns=renames,inplace=True)
    df['ZIP_CODE'] = df['ZIP_CODE'].astype(str)
    assert len(df.columns)==11,'Should be 11 cols'
    big_df = pd.concat([df,big_df])


#Clean commas and blanks from usage data, and convert to float
for i in ['std_total_kwh','std_total_therms','std_total_custs']:
    big_df[i] = numpy.where(big_df[i]==' ',0,big_df[i])
    big_df[i] = numpy.where(big_df[i].isnull(),0,big_df[i])
    big_df[i]=big_df[i].replace(',', '',inplace=False,regex=True)   
    big_df[i]=big_df[i].astype(float)
    assert not big_df[i].isnull().any(), 'Assertion Error: NaN values found in '+i


#Merge class info and zip code
big_df= big_df.merge(right=classes,on='std_class',how='left')
big_df= big_df.merge(right=geography,on='ZIP_CODE',how='left')
data_before = big_df['std_total_kwh'].sum()/10**6
big_df['PO_NAME'] = numpy.where(big_df['PO_NAME'].isnull(),'unknown',big_df['PO_NAME'])
big_df['POPULATION'] = numpy.where(big_df['POPULATION'].isnull(),'unknown',big_df['POPULATION'])
big_df['county'] = numpy.where(big_df['county'].isnull(),'unknown',big_df['county'])


#Get total customers and usage, by year and zip code
big_df = pd.pivot_table(data=big_df,values=['std_total_kwh','std_total_therms','std_total_custs'],index=['utility','std_year','std_class_clean','elec_or_gas','ZIP_CODE','PO_NAME','county','POPULATION'],aggfunc=sum)
big_df.reset_index(inplace=True)
data_after = big_df['std_total_kwh'].sum()/10**6
print('Make sure totals match before and after pivot: ',data_before,data_after)
assert data_before==data_after,'observations were dropped during pivot. Make sure there are no NaNs in the index column'
big_df.to_csv('total_usage_year_zip.csv',index=False)


#Get per household by year
big_df = pd.pivot_table(data=big_df,values=['std_total_kwh','std_total_therms','std_total_custs'],index=['PO_NAME','county','std_year','std_class_clean'],columns=['elec_or_gas'],aggfunc=sum)
flattened_columns = [' '.join(map(str, col)).strip() for col in big_df.columns]
big_df.columns = flattened_columns

big_df['kwh_per_customer_per_month'] = big_df['std_total_kwh electric']/big_df['std_total_custs electric']
big_df['therms_per_customer_per_month'] = big_df['std_total_therms gas']/big_df['std_total_custs gas']
big_df.reset_index(inplace=True)
big_df.to_csv('per_capita.csv',index=False)




