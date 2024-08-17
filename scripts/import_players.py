import sqlitecloud
from dotenv import load_dotenv
import os

load_dotenv()

database = os.getenv("SQLITE_DB")
host = os.getenv("SQLITE_URI")
api_key = os.getenv("SQLITE_API_KEY")

# example:  sqlitecloud://myhost.sqlitecloud.io:8860/mydb?apikey=abc123&compression=true&timeout=10
conn = sqlitecloud.connect(f"{host}/{database}?apikey={api_key}")

def main():
  # test_connection()
  import_players()
  conn.close()

def test_connection():
  try:
    cursor = conn.execute("SELECT * FROM players")
    result = cursor.fetchone()
  except sqlitecloud.Error as e:
    print(e)

  print(result)

def import_players():
  cursor = conn.cursor()

  with open('player_ids_current_season.csv', 'r') as file:
    next(file)
    for line in file:
      player_id, full_name, stats_url = line.strip().split(',')
      cursor.execute("INSERT OR IGNORE INTO players VALUES (?, ?, ?)", ((player_id, full_name, stats_url)))

if __name__ == '__main__':
  main()