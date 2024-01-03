import pandas #as pd
import zipfile
import numpy

clients = pandas.read_csv('inputs/common/clients.csv')
clients['ZIP_CODE'] = clients['ZIP_CODE'].astype(str)
assert '92604' in clients['ZIP_CODE'].values
#raise BaseException
zipped_directory_path = 'inputs/dg/Interconnected_Project_Sites_2023-10-31 (1).zip'
csv_files_within_zip = [
    'PGE_Interconnected_Project_Sites_2023-10-31.csv',
    'SCE_Interconnected_Project_Sites_2023-10-31.csv',
    'SDGE_Interconnected_Project_Sites_2023-10-31.csv']
index_cols = ['Year','Utility','Service City','Service Zip','Service County','Technology Type','Customer Sector']
output_dir = 'outputs/dg/'

big_df = pandas.DataFrame()
for i in csv_files_within_zip:
    with zipfile.ZipFile(zipped_directory_path, 'r') as z:
        with z.open(i) as f:
            df = pandas.read_csv(f)
            #df.head(10000).to_csv('boof.csv')
            df['Year'] = pandas.to_datetime(df['App Approved Date']).dt.year #, format='%m/%d/%Y')
            df['counter']=1
            for i in index_cols:
                df[i] = numpy.where(df[i].isnull(),'unknown',df[i])
            df = pandas.pivot_table(data=df,values=['System Size AC','Storage Size (kW AC)','counter'],
                                    index=index_cols,
                                    aggfunc=sum)
            df.reset_index(inplace=True)
            big_df = pandas.concat([big_df,df])

big_df['Service Zip'] = big_df['Service Zip'].astype(str).str.replace('\.0$', '') #Deal with pesky zip code issue - being imported like this "91001.0"
assert '92806' in big_df['Service Zip'].values
assert '92604' in big_df['Service Zip'].values

big_df = pandas.merge(left=big_df,right=clients,left_on='Service Zip',right_on='ZIP_CODE',how='left',copy=True,indicator=True)
print(big_df['_merge'].unique())

big_df.to_csv(output_dir+'dg_by_year_and_zip.csv', index = False)
