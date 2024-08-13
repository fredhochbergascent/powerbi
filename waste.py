import os
import pandas
import numpy

#TODO: Merge clients.csv and get weighted average across cities?

files = [i for i in os.listdir('inputs/waste/') if i.endswith('.xlsx')]
map_to_client = pandas.read_csv('inputs/waste/map_waste_jurisdiction_to_client.csv')

all_waste = pandas.DataFrame()
for i in files:
    df = pandas.read_excel('inputs/waste/'+i)
    jurisdiction = df.iloc[2][1].replace('Jurisdiction: ','')
    assert isinstance(jurisdiction, str) and 'Jurisdiction' in i,'did not grab jurisdiction'
    df.columns = df.iloc[4]
    df = df.iloc[5:]
    df = df[pandas.to_numeric(df['Report Year'], errors='coerce').notna()] #Drop text at the bottom (i.e. where Report Year is not a number)
    df['Jurisdiction'] = jurisdiction    
    all_waste = pandas.concat([df,all_waste])

all_waste = all_waste[['Report Year','Jurisdiction','Reviewed Disposal Tons','Population','Per Capita Disposal Population','Employment','Per Capita Disposal Employment']]
all_waste = all_waste.merge(right=map_to_client,on='Jurisdiction',how='left',copy=True)




#all_waste.reset_index(inplace=True)

#Add totals to bottom of daraset
#gp = 

#all_waste['Weighted Average Disposal Per Capita Across Jurisdictions, Pounds per Capita per Day'] = \
#gp = \
#    all_waste.groupby(['Client Name','Report Year'],as_index=False)['Reviewed Disposal Tons'].transform('sum') / \
#    all_waste.groupby(['Client Name','Report Year'],as_index=False)['Population'].transform('sum') \
#    * 2000 / 365 #Convert from tons per year to pounds per day

#print(gp)
#all_waste = pandas.concat([gp,all_waste])
all_waste['key'] = all_waste['Jurisdiction']+'&'+all_waste['Client Name']

all_waste = all_waste.pivot(index='Report Year',columns='key',values='Per Capita Disposal Population')
all_waste.reset_index(inplace=True)

all_waste.to_csv('outputs/waste/all_waste.csv',index=False)    