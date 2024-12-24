import pandas as pd
import numpy as np
terror_data_path1 = "C:\\Users\\rozen\\Downloads\\globalterrorismdb_0718dist.csv"
terror_data_path2 = "C:\\Users\\rozen\\Downloads\\RAND_Database_of_Worldwide_Terrorism_Incidents.csv"
data1 = pd.read_csv(terror_data_path1, encoding='iso-8859-1')
data2 = pd.read_csv(terror_data_path2, encoding='iso-8859-1')


data1['date_full'] = data1['iyear'].astype(str) + '-' + data1['imonth'].astype(str).str.zfill(2) + '-' + data1['iday'].astype(str).str.zfill(2)

def fix_year(date_str):
    try:
        date = pd.to_datetime(date_str, format='%d-%b-%y', errors='coerce')
        if date.year > 2023:
            date = date.replace(year=date.year - 100)
        return date
    except:
        return None

data2['Date'] = data2['Date'].apply(fix_year).dt.strftime('%Y-%m-%d')

data2_renamed = data2.rename(columns={'Country': 'country_txt', 'City': 'city', 'Date': 'date_full', 'Injuries': 'injuries', 'Fatalities': 'fatalities', 'Description': "description"})

merged_data = data1.merge(
    data2_renamed[['country_txt', 'city', 'date_full', 'injuries', 'fatalities', 'description']],
    on=['country_txt', 'city', 'date_full'],
    how='left',
    suffixes=('', '_new')
)

merged_data['summary'] = np.where(
    (merged_data['summary'].isna()),
    merged_data['description'],
    merged_data['summary']
)

merged_data['nkill'] = np.where(
    (merged_data['nkill'] < 0) | (merged_data['nkill'].isna()),
    merged_data['fatalities'],
    merged_data['nkill']
)

merged_data['nwound'] = np.where(
    (merged_data['nwound'] < 0) | (merged_data['nwound'].isna()),
    merged_data['injuries'],
    merged_data['nwound']
)

merged_data.drop(columns=['fatalities', 'injuries', 'date_full', 'description'], inplace=True)

merged_data.to_csv(r'C:\Users\rozen\PycharmProjects\final_test\csv_to_db\app\data\merge.csv', encoding='utf-8', index=False)

print("Added missing values in 'nkill':", data1['nkill'].isna().sum() - merged_data['nkill'].isna().sum())
print("Added missing values in 'nwound':", data1['nwound'].isna().sum() - merged_data['nwound'].isna().sum())
print("Added missing values in 'summary':", data1['summary'].isna().sum() - merged_data['summary'].isna().sum())
