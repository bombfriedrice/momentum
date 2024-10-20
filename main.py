import requests
import csv

# NBA Top Shot GraphQL Query to get all players
query = """
{
  allPlayers {
    data {
      id
      name
    }
  }
}
"""

# Send the request to the NBA Top Shot API
response = requests.post('https://public-api.nbatopshot.com/graphql', json={'query': query})

# Check if the request was successful
if response.status_code == 200:
    players = response.json()['data']['allPlayers']['data']
else:
    print(f"Error: {response.status_code}")
    exit()

# Create/Open CSV file to store the player data
csv_file = 'nba_topshot_players.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Player ID', 'Player Name'])  # Initial columns for Player ID and Name

    # For each player, save to CSV
    for player in players:
        writer.writerow([player['id'], player['name']])

print(f"Player data has been saved to {csv_file}")