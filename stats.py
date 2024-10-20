import os
import csv
import openai

# Load OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Open the CSV file with player data
input_file = 'nba_topshot_players.csv'
output_file = 'nba_topshot_players_with_stats.csv'

# Open the original CSV and a new file for output with added stats
with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Read the headers and add custom columns for new stats
    headers = next(reader)
    writer.writerow(headers + ['Offense', 'Defense', 'Points Scored', 'Special Ability', 'Momentum Status', 'Card Type'])

    # For each player, generate custom stats using OpenAI
    for row in reader:
        player_id, player_name = row

        # Define a detailed prompt for OpenAI
        prompt = f"""
        Create stats for {player_name} in a basketball trading card game. The card has a momentum cost, which determines the power of its stats. 
        Please follow this format:

        - **Offense (O)**: A number between 0-10 based on the card's momentum cost.
            - If the momentum cost is 1, O is between 0-2.
            - If the momentum cost is 2, O is between 3-5.
            - If the momentum cost is 3, O is between 6-8.
            - If the momentum cost is 4 or higher, O is between 8-10.

        - **Defense (D)**: Similar rules apply as for Offense, with values ranging between 0-10.
        - **Points Scored**: Number of points the moment scores, using the same range rules as Offense/Defense.
        - **Special Ability**: Unique attribute like "Clutch Play," "Deep Range," or "Fast Break."
        - **Momentum Status**: Whether the card generates momentum (Yes/No).

        There are different card types:
        - **Player Moment**: Represents a key NBA play, with balanced offense, defense, and scoring stats.
        - **Hype**: Boosts a player's abilities for a short time.
        - **Playbook**: A strategic play that affects the entire game.
        - **Equipment**: Gear that enhances a player's ability.
        - **Arena**: A special card that affects the gameplay environment.

        Generate these stats for {player_name}, and provide the Card Type.
        """

        # Use the new ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a trading card game designer for an NBA-themed card game."},
                {"role": "user", "content": prompt}
            ]
        )

        # Parse the response from OpenAI
        generated_stats = response['choices'][0]['message']['content'].strip().split('\n')
        stats_dict = {}
        for stat in generated_stats:
            if ':' in stat:
                key, value = stat.split(':')
                stats_dict[key.strip()] = value.strip()

        # Write the player data and generated stats to the new CSV
        writer.writerow([
            player_id,
            player_name,
            stats_dict.get('Offense', 'N/A'),
            stats_dict.get('Defense', 'N/A'),
            stats_dict.get('Points Scored', 'N/A'),
            stats_dict.get('Special Ability', 'N/A'),
            stats_dict.get('Momentum Status', 'N/A'),
            stats_dict.get('Card Type', 'N/A')
        ])

print(f"Player data with generated stats has been saved to {output_file}")