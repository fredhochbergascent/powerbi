import pandas #as pd
import zipfile
import numpy

clients = pandas.read_csv('inputs/common/clients.csv')
keep_me = pandas.read_csv('inputs/dg/keep_me.csv')
clients['ZIP_CODE'] = clients['ZIP_CODE'].astype(str)
assert '92604' in clients['ZIP_CODE'].values
#raise BaseException
zipped_directory_path = 'inputs/dg/Interconnected_Project_Sites_2023-10-31 (1).zip'
csv_files_within_zip = [
    'PGE_Interconnected_Project_Sites_2023-10-31.csv',
    'SCE_Interconnected_Project_Sites_2023-10-31.csv',
    'SDGE_Interconnected_Project_Sites_2023-10-31.csv']
index_cols = ['Utility','Service City','Service Zip','Service County','Technology Type','Customer Sector']
cumsum_cols = ['Utility','Service City','Service Zip','Service County','Technology Type','Customer Sector']
output_dir = 'outputs/dg/'

big_df = pandas.DataFrame()
for i in csv_files_within_zip:
    with zipfile.ZipFile(zipped_directory_path, 'r') as z:
        with z.open(i) as f:
            df = pandas.read_csv(f)
            #df.head(10000).to_csv('boof.csv')
            df['Year'] = pandas.to_datetime(df['App Approved Date']).dt.year #.astype(int) #, format='%m/%d/%Y')
            assert df['App Approved Date'].isnull().sum() < 2, 'NaN error in datetime'
            #assert not df['Year'].isnull().any(),'Null vals found'
            #df['counter']=1
            for i in index_cols:
                df[i] = numpy.where(df[i].isnull(),'unknown',df[i])
            df = pandas.pivot_table(data=df,values=['System Size AC','Storage Size (kW AC)'],
                                    index=index_cols,
                                    columns=['Year'],
                                    aggfunc=sum)
            df.reset_index(inplace=True)
            big_df = pandas.concat([big_df,df])



flattened_columns = [''.join(map(str, col)).strip() for col in big_df.columns]
big_df.columns = flattened_columns
for i in big_df.columns:
    if i.startswith('Storage Size') or i.startswith('System Size'):
        big_df[i] = big_df[i].fillna(value=0)

big_df = big_df.melt(id_vars = index_cols)
big_df['year'] = big_df['variable'].str[-6:-2].astype(int)
big_df['batteries_or_solar'] = big_df['variable'].str[0:-6]
big_df = big_df.pivot(columns='batteries_or_solar',index=index_cols+['year'],values='value')
big_df.reset_index(inplace=True)#print(

big_df.head().to_csv('chacarron.csv')
#raise BaseException



big_df['Service Zip'] = big_df['Service Zip'].astype(str).str.replace('\.0$', '') #Deal with pesky zip code issue - being imported like this "91001.0"
assert '92806' in big_df['Service Zip'].values
assert '92604' in big_df['Service Zip'].values

big_df = pandas.merge(left=big_df,right=clients,left_on='Service Zip',right_on='ZIP_CODE',how='left',copy=True,indicator=True)
print(big_df['_merge'].unique())


#big_df = big_df.pivot(index=index_cols,columns='Year')

#print(big_df.head)




#for i in index_cols:
#    assert not big_df[i].isnull().any(),i+' null in'



#Add cumulative sum
big_df.sort_values(index_cols,inplace=True)

big_df['Cumulative Solar MW installed'] = big_df.groupby(cumsum_cols)['System Size AC'].cumsum()/1000
big_df['Cumulative Battery MW installed'] = big_df.groupby(cumsum_cols)['Storage Size (kW AC)'].cumsum()/1000


#Only keep solar and wind
big_df = big_df.merge(right=keep_me,on='Technology Type',how='left',copy=True)
big_df = big_df[big_df['keep_me']==1]

big_df.to_csv(output_dir+'dg_by_year_and_zip.csv', index = False)
