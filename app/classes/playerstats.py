from bs4 import BeautifulSoup

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

  def url(self):
      return self.stats_url_base

  def setFullName(self, name):
    self.full_name = name

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
