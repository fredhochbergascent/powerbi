import os
import pandas
import numpy

files = [i for i in os.listdir('inputs/waste/') if i.endswith('.xlsx')]

all_waste = pandas.DataFrame()
for i in files:
    df = pandas.read_excel('inputs/waste/'+i)
    jurisdiction = df.iloc[2][1].replace('Jurisdiction: ','')
    #print(jurisdiction)
    assert isinstance(jurisdiction, str) and 'Jurisdiction' in i,'did not grab jurisdiction'
    df.columns = df.iloc[4]
    df = df.iloc[5:]
    df = df[pandas.to_numeric(df['Report Year'], errors='coerce').notna()] #Drop text at the bottom (i.e. where Report Year is not a number)
    df['Jurisdiction'] = jurisdiction    
    all_waste = pandas.concat([df,all_waste])
    #assert 'Jurisdiction' in all_waste.columns
    #assert 'Jurisdiction' in all_waste.columns
    #print(all_waste.columns)
    #raise BaseException

all_waste = all_waste[['Report Year','Jurisdiction','Reviewed Disposal Tons','Population','Per Capita Disposal Population','Employment','Per Capita Disposal Employment']]
all_waste.to_csv('outputs/waste/all_waste.csv')    
    #print(df.head)
    #df.to_csv('BERRIES.csv',index=False)
    #raise BaseException