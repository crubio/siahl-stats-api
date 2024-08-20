from bs4 import BeautifulSoup
from pandas import DataFrame

class PlayerStats():
  def __init__(self, player_id):
    self.player_id = player_id
    self.full_name = None
    self.teams = []
    self.games_played = 0
    self.goals = 0
    self.assists = 0
    self.penalty_minutes = 0
    self.points = 0
    self.powerplay_goals = 0
    self.shorthanded_goals = 0


  @property 
  def stats_url_base(self):
    return f"https://stats.sharksice.timetoscore.com/display-player-stats.php?player={self.player_id}"
  
  def get_test_html(self):
    with open('player_stats_sample.html', 'r') as file:  # r to open file in READ mode
      html_as_string = file.read()
      return html_as_string

  def url(self):
      return self.stats_url_base

  def setFullName(self, name):
    self.full_name = name.strip()

  def parseRow(self, row):
    '''parse a row of stats'''
    tds = row.find_all('td', recursive=False)
    if tds[0].text.strip() not in self.teams:
      self.teams.append(tds[0].text.strip())

    self.games_played += int(tds[2].text)
    self.goals += int(tds[3].text)
    self.assists += int(tds[4].text)
    self.penalty_minutes += int(tds[5].text)
    self.points += int(tds[6].text)
    self.powerplay_goals += int(tds[7].text)
    self.shorthanded_goals += int(tds[8].text)
    

  def parse_stats_html(self, html):
    # refer to the html page url for stucture
    try :
      soup = BeautifulSoup(html, 'html.parser')
      name_tag = "#player_bio th"
      stat_table = "#playerstattable"
      trs = soup.select(stat_table)[0].find_all(bgcolor="#CCCCCC")
      for tr in trs:
        self.parseRow(tr)

      name = soup.select(name_tag)[0].text
      self.setFullName(name)
    except:
      return None
    
  def parse_team_stats(self, html, json=False):
    '''parse the team stats'''
    try:
      soup = BeautifulSoup(html, 'html.parser')
      name_tag = "#player_bio th"
      stat_table = "#playerstattable"
      trs = soup.select(stat_table)[0].find_all(bgcolor="#CCCCCC")
      all_rows = []
      for tr in trs:
        row = tr.find_all('td', recursive=False)
        all_rows.append([row[0].text, row[1].text, int(row[2].text), int(row[3].text), int(row[4].text), int(row[5].text), int(row[6].text), int(row[7].text), int(row[8].text)])
      
      df = DataFrame(all_rows, columns=['Team', 'Season', 'GP', 'G', 'A', 'PIM', 'PTS', 'PPG', 'SHG'])
      df['Team'] = df['Team'].str.strip()
      df.drop('Season', axis=1, inplace=True)

      aggregate_functions = {'GP': 'sum', 'G': 'sum', 'A': 'sum', 'PIM': 'sum', 'PTS': 'sum', 'PPG': 'sum', 'SHG': 'sum'}
      df = df.groupby('Team').agg(aggregate_functions).reset_index()
      df.set_index('Team', inplace=True)
      
      if json:
        return df.to_dict(orient='index')
      
      name = soup.select(name_tag)[0].text
      self.setFullName(name)

      return df
      
    except:
      return None
