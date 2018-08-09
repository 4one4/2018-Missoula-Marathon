from requests import get
from bs4 import BeautifulSoup
import pandas as pd


def download_results(url, race):
    
    df_columns = ['Place','Name','City','Bib_No','Age','Gender','Age_Group','Chip_Time','Gun_Time','Chip_Diff','Pace', 'Race']
    
    df_rows = []
    
    page = get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    #grab our results table
    result_table = soup.find('table', class_='racetable')
    rows = result_table.find_all('tr')
    
    #loop through rows
    for row in rows:
        first = row.find('td')
        
        #table has extra garbage only look at rows with a number (place) in the
        #first cell
        if first.text.isnumeric():
            #get all cells for this row
            cells = row.find_all('td')
            #grab the first 11 cells
            result = [cells[0].text,
                      cells[1].text,
                      cells[2].text,
                      cells[3].text,
                      cells[4].text,
                      cells[5].text,
                      cells[6].text,
                      cells[7].text,
                      cells[8].text,
                      cells[9].text,
                      cells[10].text,
                      race]
            df_rows.append(result)
    df = pd.DataFrame(df_rows, columns=df_columns)
    return df


#results urls
full_results_url = 'http://competitivetiming.com/results/1850841O'
half_results_url = 'http://competitivetiming.com/results/1850842O'

full_df = download_results(full_results_url, 'full')
half_df = download_results(half_results_url, 'half')

#save to csv
full_df.to_csv('data/2018_missoula_marathon_full.csv', index=False)
half_df.to_csv('data/2018_missoula_marathon_half.csv', index=False)