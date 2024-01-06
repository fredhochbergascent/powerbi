import pandas

input_wkbk = 'inputs/transit/October 2023 Complete Monthly Ridership (with adjustments and estimates) (4).xlsx'
sheets = {
'UPT':'Transit Unlinked Passenger Trips',
'VRM':'Transit Vehicle Revenue Miles',
'VRH':'Transit Vehicle Revenue Hours',
'VOMS':'Transit Peak Vehicles'
}
modes = pandas.read_csv('inputs/transit/modes.csv')
tos = pandas.read_csv('inputs/transit/tos.csv')

for each_sheet in sheets:
    df = pandas.read_excel(input_wkbk,sheet_name=each_sheet)
    df = df.merge(right=modes,on='Mode',how='left',copy=True)
    df = df.merge(right=tos,on='TOS',how='left',copy=True)
    df=df[df['NTD ID'].notnull()] #Get rid of totals at the bottom
    date_cols = [i for i in df.columns if '/' in i]
    index_cols = [i for i in df.columns if '/' not in i]
    df = pandas.melt(df,id_vars = index_cols,value_vars = date_cols,var_name='Date',value_name = sheets[each_sheet])
    df.reset_index(inplace=True)
    df['year'] = pandas.to_datetime(df['Date']).dt.year
    assert not df['year'].isnull().any(),'Date parsing did not work'
    df.to_csv('outputs/transit/'+sheets[each_sheet]+'.csv',index=False)