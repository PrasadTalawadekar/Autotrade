import pandas as pd

# Reference file (contains all ISIN codes)
reference_file = r"C:\Users\Prasad\Music\NiftyDataBase\ind_niftytotalmarket_list.csv"

# List of CSV files
csv_files = [
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_nifty50list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_niftynext50list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_nifty100list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_nifty200list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_nifty500list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_nifty500Multicap502525_list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_niftymidcap150list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_niftymidcap50list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_niftymidcapselect_list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_niftymidcap100list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_niftysmallcap250list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_niftysmallcap50list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_niftysmallcap100list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_niftymicrocap250_list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_niftylargemidcap250list.csv",
    r"C:\Users\Prasad\Music\NiftyDataBase\ind_niftymidsmallcap400list.csv"
]

full_ref_df=pd.read_csv(reference_file)
reference_df = pd.read_csv(reference_file, usecols=["ISIN Code"])

summary_df = pd.DataFrame(columns=['ISIN Code'])

for csv_file in csv_files:
    df = pd.read_csv(csv_file, usecols=["ISIN Code"])
    
    merged_df = pd.merge(reference_df, df, on="ISIN Code", how="left", indicator=True)
    
    reference_df[csv_file] = merged_df['_merge'] == 'both'


new_column_names = {}
for column_name in reference_df.columns:
    file_name = column_name.split('\\')[-1].split('.')[0]
    file_name=file_name.replace('ind_','')
    file_name=file_name.replace('_list','')
    file_name=file_name.replace('list','')
    new_column_names[column_name] = file_name
reference_df = reference_df.rename(columns=new_column_names)


reference_df = pd.merge(reference_df, full_ref_df[['ISIN Code', 'Company Name']], on='ISIN Code', how='left')
columns = list(reference_df.columns)
columns.insert(1, columns.pop(columns.index('Company Name')))
reference_df = reference_df[columns]

reference_df.to_csv(r"C:\Users\Prasad\Music\NiftyDataBase\summary.csv", index=False)
