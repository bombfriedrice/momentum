import os
import csv
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from tqdm import tqdm  # Progress bar

# Load OpenAI API key from environment

# Open the CSV file with player data
input_file = 'nba_topshot_players.csv'
output_file = 'nba_topshot_players_with_stats.csv'

# Open the original CSV and a new file for output with added stats
with open(input_file, mode='r') as infile, open(output_file,
                                                mode='w',
                                                newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Read the headers and add custom columns for new stats
    headers = next(reader)
    writer.writerow(headers + [
        'Offense', 'Defense', 'Points Scored', 'Special Ability',
        'Momentum Status', 'Card Type'
    ])

    # Use tqdm for a progress bar
    total_rows = sum(1 for row in reader)  # Count total rows for progress bar
    infile.seek(0)  # Reset the file pointer after counting
    next(reader)  # Skip header row again

    # For each player, generate custom stats using OpenAI
    for row in tqdm(reader, total=total_rows, desc="Generating stats"):
        player_id, player_name = row

        # Define a detailed prompt for OpenAI
        prompt = f"""
        You are creating stats for a basketball trading card game inspired by Lorcana but adapted for basketball. The game is called "NBA Momentum," where real NBA moments from Top Shot are turned into playable cards.

        The stats you generate will follow the structure below, where each card has a **momentum cost** that influences how strong the player's stats are:

        - **Offense (O)**: A number between 0-10 that represents the player's scoring ability, influenced by the **momentum cost**. 
            - **Momentum Cost 1**: Offense should range between 0-2 (a weaker player).
            - **Momentum Cost 2**: Offense should range between 3-5 (moderate scorer).
            - **Momentum Cost 3**: Offense should range between 6-8 (strong scorer).
            - **Momentum Cost 4 or higher**: Offense should range between 8-10 (elite scorer).
          
        - **Defense (D)**: A number between 0-10 representing how well the player can defend, following the same logic as Offense:
            - **Momentum Cost 1**: Defense should range between 0-2.
            - **Momentum Cost 2**: Defense should range between 3-5.
            - **Momentum Cost 3**: Defense should range between 6-8.
            - **Momentum Cost 4 or higher**: Defense should range between 8-10.
          
        - **Points Scored**: How many points this card can score in a game situation, using the same logic as Offense and Defense. This stat should also be influenced by momentum.
        
        - **Special Ability**: A unique ability that adds strategy to the game, such as "Clutch Play" (performs well under pressure), "Deep Range" (excels at shooting three-pointers), or "Fast Break" (quick transition scoring). The special ability should be relevant to basketball tactics.
          
        - **Momentum Status**: This will either be "Yes" or "No," indicating whether this card generates additional momentum during gameplay. Cards with higher momentum costs typically generate more momentum.
        
        - **Card Type**: Choose from one of the following categories based on the player or moment:
            - **Player Moment**: Represents a specific NBA highlight, balanced between offense and defense.
            - **Hype**: Temporarily boosts a player's abilities.
            - **Playbook**: A strategic play or action that impacts the entire game.
            - **Equipment**: Gear that enhances a player's stats (e.g., shoes, wristbands).
            - **Arena**: A card that affects the entire environment or atmosphere of the game.

        For example, generate stats like this for {player_name}:

        Offense: [X]
        Defense: [X]
        Points Scored: [X]
        Special Ability: [Ability]
        Momentum Status: [Yes/No]
        Card Type: [Type]

        Please stick to this format and ensure the stats reflect real basketball play styles while also making the card game strategic.
        """

        # Use the ChatCompletion API to get the stats
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role":
                "system",
                "content":
                "You are a trading card game designer for an NBA-themed card game."
            }, {
                "role": "user",
                "content": prompt
            }])

        # Parse the response from OpenAI safely
        generated_stats = response.choices[0].message.content.strip().split(
            '\n')
        stats_dict = {}
        for stat in generated_stats:
            if ':' in stat:
                try:
                    key, value = stat.split(
                        ':', 1)  # Use max split of 1 to handle multiple colons
                    stats_dict[key.strip()] = value.strip()
                except ValueError:
                    continue  # Skip lines that don't fit the expected format

        # Write the player data and generated stats to the new CSV
        writer.writerow([
            player_id, player_name,
            stats_dict.get('Offense', 'N/A'),
            stats_dict.get('Defense', 'N/A'),
            stats_dict.get('Points Scored', 'N/A'),
            stats_dict.get('Special Ability', 'N/A'),
            stats_dict.get('Momentum Status', 'N/A'),
            stats_dict.get('Card Type', 'N/A')
        ])

print(f"Player data with generated stats has been saved to {output_file}")
