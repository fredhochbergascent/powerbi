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
    df['Commute Means of Transportation'] = df['Label (Grouping)'].str.strip()
    df = df[df['Commute Means of Transportation'].isin(commute_data_of_interest)]
    df.rename(columns={df.columns[1]:'Percent of Households with This Commute Mode'},inplace=True)
    
    try:
        df['Percent of Households with This Commute Mode'] = df['Percent of Households with This Commute Mode'].str.replace('%','').astype(float)
        assert 99.8 < df['Percent of Households with This Commute Mode'].sum()<=100.2 and df['Percent of Households with This Commute Mode'].sum(),'Conversion to percent did not work'
    except ValueError:
        df['Percent of Households with This Commute Mode'] = 'Not Available'
    
    df = df[['Jurisdiction','Commute Means of Transportation','Percent of Households with This Commute Mode','Year']]
    
    commute = pandas.concat([commute,df])
    
commute.to_csv('outputs/census/census_commute.csv')