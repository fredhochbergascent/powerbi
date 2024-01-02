import zipfile
import pandas as pd

def readin(file_path):
    print('now reading: ',file_path)
    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as z:
            if z.namelist()[0] == '_MACOSX':
                file_in_zip = z.namelist()[1]
            else:
                file_in_zip = z.namelist()[0]
            try:
                df = pd.read_excel(z.open(file_in_zip), engine='openpyxl')
            except:
                df = pd.read_csv(z.open(file_in_zip))
        return df
    else:
        try:
            df = pd.read_excel(file_path, engine='openpyxl') #,header=None)
            if 'Usage Aggregation by Zip code for Web Posting' in df.columns:
                df.columns = df.iloc[1]
                df = df[2:]
            return df
        except Exception as e_xlsx:
            try:
                df = pd.read_excel(file_path, engine='xlrd')
                if 'Usage Aggregation by Zip code for Web Posting' in df.columns:
                    df.columns = df.iloc[1]
                    df = df[2:]
                return df
            except Exception as e_xls:
                try:
                    df = pd.read_csv(file_path)
                    return df
                except Exception as e_csv:
                    raise e_csv
