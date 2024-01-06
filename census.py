import pandas
import requests
import os

#Combine heating data
heating = pandas.DataFrame()
heating_fuel_files = [i for i in os.listdir('inputs/census') if 'B25040' in i]
for i in heating_fuel_files:
    df = pandas.read_csv('inputs/census/'+i)
    assert '!!Estimate' in df.columns[1]
    df['Jurisdiction'] = df.columns[1].replace('!!Estimate','')
    #df['Fuel Source'] = df['Label (Grouping)'].str.replace('[^a-zA-Z, ]', '', regex=True)
    df['Fuel Source'] = df['Label (Grouping)'].str.strip()
    df.rename(columns={df.columns[1]:'Households Using This Fuel'},inplace=True)
    df['Year'] = int(i[7:11])
    df = df[['Jurisdiction','Fuel Source','Households Using This Fuel','Year']]
    heating = pandas.concat([heating,df])
heating.to_csv('outputs/census/census_heating.csv')

#raise BaseException

#Combine transportation to work data
commute = pandas.DataFrame()
commute_data_of_interest = [
'Drove alone','In 2-person carpool','In 3-person carpool','In 4-or-more person carpool','Public transportation (excluding taxicab)','Walked','Bicycle','Taxicab, motorcycle, or other means','Worked from home','Worked at home']
commute_files = [i for i in os.listdir('inputs/census') if 'S0801' in i]
for i in commute_files:
    df = pandas.read_csv('inputs/census/'+i)
    assert 'Total!!Estimate' in df.columns[1]
    df['Year'] = int(i[7:11])
    df['Jurisdiction'] = df.columns[1].replace('!!Total!!Estimate','')
    #print(df['Jurisdiction'])
    df['Commute Means of Transportation'] = df['Label (Grouping)'].str.strip()
    df = df[df['Commute Means of Transportation'].isin(commute_data_of_interest)]
    df.rename(columns={df.columns[1]:'Percent of Households with This Commute Mode'},inplace=True)
    
    try:
        df['Percent of Households with This Commute Mode'] = df['Percent of Households with This Commute Mode'].str.replace('%','').astype(float)
        #print('doof',i,df['Percent of Households with This Commute Mode'].sum())
        assert 99.8 < df['Percent of Households with This Commute Mode'].sum()<=100.2 and df['Percent of Households with This Commute Mode'].sum(),'Conversion to percent did not work'
    except ValueError:
        df['Percent of Households with This Commute Mode'] = 'Not Available'
    
    df = df[['Jurisdiction','Commute Means of Transportation','Percent of Households with This Commute Mode','Year']]
    
    commute = pandas.concat([commute,df])
    
commute.to_csv('outputs/census/census_commute.csv')
    #df.to_csv('goji.csv')
    #raise BaseException






































    #print(df['Year'])
    #rint(df['Jurisdiction'])


#print(heating_fuel_files.columns)





'''
#df = pandas.read_csv('PGE_Interconnected_Project_Sites_2023-10-31.csv',nrows=1000)
#df.to_csv('pge.csv')


#raise BaseException
#import ast
#df = pandas.read_csv('pdb2022bg.csv',nrows=1000)
#df.to_csv('census_test.csv')
#https://www.socialexplorer.com/data/ACS2010/metadata/?ds=ACS10&table=B25040



the_url = 'https://api.census.gov/data/2022/acs/acs1?get=group(B25040)&for=place:*&in=state:*&key=f51d2d46f72b90251e21cc93a6406ceabd928a28'
#the_url = 'https://api.census.gov/data/2022/acs/acs1?get=group(B25040)&for=urban%20area:*&key=f51d2d46f72b90251e21cc93a6406ceabd928a28'

the_data = requests.get(the_url)
print(the_data.content)

the_data = the_data.json()

columns = the_data[0]
#print(columns,len(columns))
rows = the_data[1:]
#print(len(rows))

df = pandas.DataFrame(rows, columns=columns)
print(df.head)

#for i in the_url
#the_data = ast.literal_eval(requests.get(the_url).content)[0:10]

#headers = the_data[0]
#print(headers)

#data = pandas.read_html(the_url)
#df = pandas.DataFrame(the_data)


#the_data = str(requests.get(the_url).content[0:1000])
#print(data[0:10])
#for i in data[0:100]:
#    print(i)

#print(data.content[2:])
#df = pandas.read_table(the_url,names=['A','B','C'])
#print(df)
df.to_csv('census_test3.csv')
'''