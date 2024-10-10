from selenium import webdriver
import time

download_path = r"C:\Users\Prasad\Music\NiftyDataBase"
url_array = ["https://nsearchives.nseindia.com/content/indices/ind_nifty50list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_niftynext50list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_nifty100list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_nifty200list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_niftytotalmarket_list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_nifty500list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_nifty500Multicap502525_list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_niftymidcap150list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_niftymidcap50list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_niftymidcapselect_list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_niftymidcap100list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_niftysmallcap250list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_niftysmallcap50list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_niftysmallcap100list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_niftymicrocap250_list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_niftylargemidcap250list.csv",
"https://nsearchives.nseindia.com/content/indices/ind_niftymidsmallcap400list.csv"]

options = webdriver.ChromeOptions()
prefs = {"download.default_directory": download_path}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)

try:
    for url in url_array:
        driver.get(url)
        time.sleep(3)  
    print("Files downloaded successfully")
except Exception as e:
    print(f"Error occurred: {str(e)}")
finally:
    driver.quit()
