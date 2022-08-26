from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np


#URL = 'https://www.transfermarkt.com/istanbul-basaksehir-fk/kader/verein/6890/saison_id/2022/plus/1'
URL = 'https://www.transfermarkt.com/fenerbahce-sk/kader/verein/36/saison_id/2022/plus/1'
heads = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
page = requests.get(URL, headers=heads)
soup = BeautifulSoup(page.content, "html.parser")


player_names = soup.find_all("table", {"class": 'inline-table'})
player_info = soup.find_all("td", {"class": "zentriert"})
values = soup.find_all("td", {"class": "rechts hauptlink"})

columns = ['Name', 'Position']
df1 = pd.DataFrame(columns=columns)
for i in range(0, len(player_names)):
    df1.loc[len(df1), df1.columns] = [
        str(player_names[i]).split('<img alt="')[1].split('" class')[0],
        str(player_names[i]).split('/a>')[1].split('<td>')[1].split('</')[0].strip()]


columns = ['Number', 'Date of birth / Age', 'Nationality',
           'Height', 'Foot', 'Joined', 'Signed from', 'Contract']
df2 = pd.DataFrame(columns=columns)


for i in range(0, len(player_info), 8):
    df2.loc[len(df2), df2.columns] = [
        str(player_info[i]).split('rn_nummer">')[1].split('</')[0],
        str(player_info[i+1]).split('">')[1].split('</')[0],
        str(player_info[i+2]).split('title="')[1].split('"')[0],
        str(player_info[i+3]).split('">')[1].split('</')[0],
        str(player_info[i+4]).split('">')[1].split('</')[0],
        str(player_info[i+5]).split('">')[1].split('</')[0],
        str(player_info[i+6]).split('alt="')[1].split('"')[0],
        str(player_info[i+7]).split('">')[1].split('</')[0]]


value_list = []

for i in range(0, len(values)):
    value_list.append(str(values[i]).split('">')[1].split('<')[0])
df3 = pd.DataFrame(value_list, columns=['Market Value'])


data = pd.concat([df1, df2, df3], axis=1)

team_name = URL.split('com/')[1].split('/')[0]
data.to_csv('{}.csv'.format(team_name))
print("------- CSV Downloaded -------")