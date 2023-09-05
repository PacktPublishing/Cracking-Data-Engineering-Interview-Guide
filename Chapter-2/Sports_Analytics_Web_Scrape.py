import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def league_table():

    url = 'https://www.bbc.com/sport/football/premier-league/table'
    headers = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text,  "html.parser")
    table= soup.find("table", class_="ssrcss-14j0ip6-Table e3bga5w5")

    for i in table.find_all('th'):
        title = i.text
        headers.append(title)
    league_table = pd.DataFrame(columns = headers)
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(league_table)
        league_table.loc[length] = row
    league_table.drop(["Form, Last 6 games, Oldest first"], axis=1, inplace=True)
    return league_table

def top_scorers():
    url = 'https://www.bbc.com/sport/football/premier-league/top-scorers'
    headers = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text,  "html.parser")
    table= soup.find("table", class_="gs-o-table")

    for i in table.find_all('th'):
        title = i.text
        headers.append(title)
    top_scorers = pd.DataFrame(columns = headers)
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(top_scorers)
        top_scorers.loc[length] = row

    top_scorers.Name = top_scorers.Name.replace(r'([A-Z])', r' \1', regex=True).str.split()
    top_scorers.Name = top_scorers.Name.apply(lambda x: ' '.join(dict.fromkeys(x).keys()))

    top_scorers['Club'] = top_scorers.Name.str.split().str[2:].str.join(' ')
    top_scorers.Name = top_scorers.Name.str.split().str[:2].str.join(' ')
    col = top_scorers.pop("Club")
    top_scorers.insert(2, 'Club', col)
    top_scorers.Club = top_scorers.Club.apply(lambda x: 'Manchester City' if 'Manchester City' in x else x)
    top_scorers.Club = top_scorers.Club.apply(lambda x: 'Manchester United' if 'Manchester United' in x else x)
    top_scorers.Club = top_scorers.Club.apply(lambda x: 'Brighton & Hove Albion' if 'Brighton & Hove Albion' in x else x)

    return top_scorers

def detail_top():
    url = 'https://www.worldfootball.net/goalgetter/eng-premier-league-2023-2024/'
    headers = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text,  "html.parser")
    table= soup.find("table", class_="standard_tabelle")

    for i in table.find_all('th'):
        title = i.text
        headers.append(title)
    detail_top_scorer = pd.DataFrame(columns = headers)
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(detail_top_scorer)
        detail_top_scorer.loc[length] = row

    detail_top_scorer = detail_top_scorer.drop([''],axis=1)
    detail_top_scorer.Team = detail_top_scorer.Team.str.replace('\n\n','')
    detail_top_scorer['Penalty'] = detail_top_scorer['Goals (Penalty)'].str.split().str[-1:].str.join(' ')
    detail_top_scorer['Penalty'] = detail_top_scorer['Penalty'].str.replace('(','')
    detail_top_scorer['Penalty'] = detail_top_scorer['Penalty'].str.replace(')','')
    detail_top_scorer['Goals (Penalty)'] = detail_top_scorer['Goals (Penalty)'].str.split().str[0].str.join('')
    detail_top_scorer.rename(columns = {'Goals (Penalty)':'Goals'}, inplace = True)
    detail_top_scorer = detail_top_scorer.drop(['#'], axis = 1)
    return detail_top_scorer

def player_table():
    url = [f'https://www.worldfootball.net/players_list/eng-premier-league-2023-2024/nach-name/{i:d}' for i in (range(1, 12))]
    header = ['Player','','Team','born','Height','Position']
    df = pd.DataFrame(columns=header)
    def player(ev):
        url = ev
        headers = []
        page = requests.get(url)
        soup = BeautifulSoup(page.text,  "html.parser")
        table= soup.find("table", class_="standard_tabelle")

        for i in table.find_all('th'):
            title = i.text
            headers.append(title)
        players = pd.DataFrame(columns = headers)
        for j in table.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            length = len(players)
            players.loc[length] = row
        return players

    for i in url:
        a = player(i)
        df = pd.concat([df, a], axis=0).reset_index(drop=True)

    df = df.drop([''], axis=1)
    return df

def all_time_table():
    url = 'https://www.worldfootball.net/alltime_table/eng-premier-league/pl-only/'
    headers = ['pos','#','Team','Matches','wins','Draws','Losses','Goals','Dif','Points']
    page = requests.get(url)
    soup = BeautifulSoup(page.text,  "html.parser")
    table= soup.find("table", class_="standard_tabelle")


    alltime_table= pd.DataFrame(columns = headers)
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(alltime_table)
        alltime_table.loc[length] = row

    alltime_table = alltime_table.drop(['#'], axis=1)
    alltime_table.Team = alltime_table.Team.str.replace('\n', '')
    return alltime_table

def all_time_winner_club():
    url = 'https://www.worldfootball.net/winner/eng-premier-league/'
    headers = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text,  "html.parser")
    table= soup.find("table", class_="standard_tabelle")

    for i in table.find_all('th'):
        title = i.text
        headers.append(title)
    winners = pd.DataFrame(columns = headers)
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(winners)
        winners.loc[length] = row

    winners = winners.drop([''], axis=1)
    winners['Year'] = winners['Year'].str.replace('\n', '')
    return winners


def top_scorers_seasons():
    url = 'https://www.worldfootball.net/top_scorer/eng-premier-league/'
    headers = ['Season','#','Top scorer','#','Team','goals']
    page = requests.get(url)
    soup = BeautifulSoup(page.text,  "html.parser")
    table= soup.find("table", class_="standard_tabelle")
    winners = pd.DataFrame(columns = headers)
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(winners)
        winners.loc[length] = row

    winners = winners.drop(['#'], axis=1)
    winners=winners.replace('\\n','',regex=True).astype(str)
    winners['Season'] = winners['Season'].replace('', np.nan).ffill()
    return winners

def goals_per_season():
    url = 'https://www.worldfootball.net/stats/eng-premier-league/1/'
    headers = []
    page = requests.get(url)
    soup = BeautifulSoup(page.text,  "html.parser")
    table= soup.find("table", class_="standard_tabelle")

    for i in table.find_all('th'):
        title = i.text
        headers.append(title)
    goals_per_season = pd.DataFrame(columns = headers)
    for j in table.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(goals_per_season)
        goals_per_season.loc[length] = row
    goals_per_season.drop(goals_per_season.index[-1],inplace=True)

    goals_per_season = goals_per_season.drop(['#'], axis=1)
    goals_per_season.rename(columns = {'goals':'Goals','Ø goals':'Average Goals'}, inplace = True)

    return goals_per_season
