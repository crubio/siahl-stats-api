import sys
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
from player_ids import *

STATS_URL = "https://stats.sharksice.timetoscore.com/display-player-stats.php?player="

def main(player_name):
    print(f'hello {player_name}, looking you up...this may take a while\n')
    get_find_player_by_name(player_name)

def get_find_player_by_name(player_name_str): 
    '''Iterates thru stats pages to find player id by full name'''
    player_names = []
    for player_id in player_ids:
        page = urlopen(f"{STATS_URL}{player_id}")
        html_bytes = page.read()
        html = html_bytes.decode()
        soup = BeautifulSoup(html, 'html.parser')

        # html tag containing name of the player
        name_tag = "#player_bio th"
        try:
            name_tag = soup.css.select(name_tag)[0].text
            if (name_tag.lower() == player_name_str.lower()):
                print(f"Found {name_tag} with id: {player_id}")
                player_names.append(player_id)
                # if we find one name, just return that one
                break
        except:
            continue
    return print(player_names)
    
def get_valid_ids():
    '''Returns valid player ids, pipe output to a file and use as input for get_find_player_by_name function'''
    player_ids = []
    # valid ids seem to be in this range
    for id in range(50141, 58000):
        page = urlopen(f"{STATS_URL}{id}")
        html_bytes = page.read()
        html = html_bytes.decode()
        soup = BeautifulSoup(html, 'html.parser')

        name_tag = "#player_bio th"
        try:
            name = soup.css.select(name_tag)[0].text
            if name:
                player_ids.append(id)
        except:
            continue
    return print(player_ids)
    
if __name__ == '__main__':
    main(sys.argv[1])