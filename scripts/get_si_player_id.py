import sys
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
from player_ids import *
import csv
import logging
import datetime
import re

STATS_URL_BASE = "https://stats.sharksice.timetoscore.com/display-player-stats.php?player="
BASE_URL = "https://stats.sharksice.timetoscore.com/"

def main():
    # logging if you want it
    # timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    # logging.basicConfig(filename=f'player_id_{timestamp}.log', filemode='w', level=logging.DEBUG)
    get_player_ids_to_csv()

def get_divisional_urls():
    '''Returns a list of urls for each division'''
    division_urls = []
    # this url represents the current season in play
    current_season_url = 'https://stats.sharksice.timetoscore.com/display-stats.php?league=1'
    soup = BeautifulSoup(urlopen(current_season_url), 'html.parser')
    try:
        division_links = soup.select('a[href^="display-league-stats?stat_class=1"]')
        for link in division_links:
            href = link['href']
            division_urls.append(f"{BASE_URL}{href}")
    except:
        return None
    return division_urls


def get_player_ids_to_csv():
    url_base = "https://stats.sharksice.timetoscore.com/"
    # a full list of divisional active players will be at a url like https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=64&level=221&conf=0
    urls = get_divisional_urls()
    players = []

    for url in urls:
        soup = BeautifulSoup(urlopen(url), 'html.parser')
        player_links = soup.find_all('a', href=lambda href: href and href.startswith("display-player-stats.php?player="))
        
        for player in player_links:
            player_id = re.search(r'player=(\d+)', player['href']).group(1)
            full_name = player.text.strip()
            stats_url = f"{url_base}{player['href'].strip(']}')}"
            players.append({'player_id': player_id, 'full_name': f'{full_name}', 'stats_url': f'{stats_url}'})
        
        with open('player_ids_current_season.csv', 'w', newline='') as csvfile:
          fieldnames = ['player_id', 'full_name', 'stats_url']
          writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

          writer.writeheader()
          for row in players:
            writer.writerow(row)
        
    return print('done')
    
if __name__ == '__main__':
    main()