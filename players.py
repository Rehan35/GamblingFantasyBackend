from nba_api.stats.static import players
from nba_api.stats.static import teams
import requests
import os
import csv

def get_player_image_url():
    data = [["Name", "Link"]]
    current_players = [player for player in players.get_players() if player['is_active']]
    for player in current_players:
        id = player['id']
        name = player['full_name']
        url = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{id}.png'
        data.append([name, url])
    
    directory = "output_files"
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist

    # File path
    file_path = os.path.join(directory, "data.csv")

    # Write to CSV
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"CSV file saved at: {file_path}")

def get_team_nicknames():
    data = [["Name", "Nickname", "Abbreviation"]]
    for team in teams.get_teams():
        team_name = team['full_name']
        nickname = team['nickname']
        abbreviation = team['abbreviation']
        data.append([team_name, nickname, abbreviation])
    directory = "output_files"
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist

    # File path
    file_path = os.path.join(directory, "TeamNicknames.csv")

    # Write to CSV
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"CSV file saved at: {file_path}")

def get_team_image_urls():

    team_ids = [1610612737, 1610612738, 1610612751, 1610612766, 1610612741, 1610612739, 1610612742, 
               1610612743, 1610612765, 1610612744, 1610612745, 1610612754, 1610612746, 1610612747, 
               1610612763, 1610612748, 1610612749, 1610612750, 1610612740, 161061275, 1610612760, 
               1610612753, 1610612755, 1610612756, 1610612757, 1610612758, 1610612759, 1610612761, 
               1610612762, 1610612764]
    save_folder='nba_logos'
    for team in teams.get_teams():
        base_url = "https://cdn.nba.com/logos/nba"
        team_id = team['id']
        team_name = team['full_name']
        final_url = f'{base_url}/{team_id}/primary/L/logo.svg'
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        
        # Send a GET request to fetch the image content
        response = requests.get(final_url, stream=True)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Save the image to the specified folder
            file_path = os.path.join(save_folder, f'{team_name}.svg')
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Image saved to {file_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code} {team_name} {team_id}")
# get_team_image_urls()

# get_player_image_url()

get_team_nicknames()