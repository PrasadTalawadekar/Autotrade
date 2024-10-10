import asyncio
import pandas as pd
import Authorization


def load_reference_df(reference_file: str) -> pd.DataFrame:
    return pd.read_csv(reference_file, usecols=["ISIN Code"])

reference_file = r"C:\Users\Prasad\Music\NiftyDataBase\ind_niftytotalmarket_list.csv"


reference_df = load_reference_df(reference_file)

access_token_file = r'C:\Users\Prasad\Music\Share market\access_token.txt'
reference_df = load_reference_df(reference_file)

with open(access_token_file, 'r') as file:
    access_token = file.read()



def extract_ohlc(ltp_data):
    if 'status' in ltp_data and ltp_data['status'] == 'success':
        data = ltp_data.get('data', {})
        for key, value in data.items():
            ohlc = value.get('ohlc', {})
            print(ohlc)
            return ohlc
    return None

def extractopen(json_entry):
    try:
        return(json_entry.get('open',None))
    except Exception as ex:
        return None
    
def extracthigh(json_entry):
    try:
        return(json_entry.get('high',None))
    except Exception as ex:
        return None

def extractlow(json_entry):
    try:
        return(json_entry.get('low',None))
    except Exception as ex:
        return None

def extractclose(json_entry):
    try:
        return(json_entry.get('close',None))
    except Exception as ex:
        return None




funds = asyncio.run(Authorization.APIActions.get_funds(access_token))
print(funds)


reference_df['NSE_OPEN'] = None
reference_df['NSE_HIGH'] = None
reference_df['NSE_LOW'] = None
reference_df['NSE_CLOSE'] = None


for index, row in reference_df.iterrows():
    isin_code = row['ISIN Code']
    NSE_LTP = asyncio.run(Authorization.APIActions.get_quote("NSE_EQ|" + isin_code, access_token))
    print(isin_code)
    json_ent = (extract_ohlc(NSE_LTP))
    reference_df.at[index, 'NSE_OPEN'] = extractopen(json_ent)
    reference_df.at[index, 'NSE_HIGH'] = extracthigh(json_ent)
    reference_df.at[index, 'NSE_LOW'] = extractlow(json_ent)
    reference_df.at[index, 'NSE_CLOSE'] = extractclose(json_ent)

    print(extractclose(json_ent))



    
sumarry_path=r"C:\Users\Prasad\Music\NiftyDataBase\summary_olhc.csv"
reference_df.to_csv(sumarry_path, index=False)

print("DataFrame with BSE_LTP and NSE_LTP saved to:", sumarry_path)