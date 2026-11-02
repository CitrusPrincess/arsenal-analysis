"""
Arsenal Attacking Analysis
2015-2016 Season

This project analyzes Arsenal's attacking performance across
38 Premier League matches using StatsBomb open event data.

Metrics include:
- Total shots
- Expected goals (xG)
- Actual goals
- Average xG per shot
- Goals compared with expected goals

The script generates three visualizations to explore
Arsenal's attacking performance throughout the season.
"""

import json; import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from urllib.request import urlopen

#### START: DOWNLOAD 2015/2016 ARSENAL SEASON DATA ####

# The URL for Premier League 2015/2016 match data
url = (
    "https://raw.githubusercontent.com/hudl/open-data/"
    "master/data/matches/2/27.json"
)

# Download the data
with urlopen(url) as response:
    matches = json.load(response)

# Keep only Arsenal match data in list
arsenal_matches = []

# Extract Arsenal matches only
for match in matches:
    home_team = match["home_team"]["home_team_name"]
    away_team = match["away_team"]["away_team_name"]

    if home_team == "Arsenal" or away_team == "Arsenal":
        arsenal_matches.append(match)

## Lines 29-89: Print stmts to be uncommented if needed to explore the data set

## Question: Do we have data from an entire season (38 matches)?
# print("Arsenal matches found:", len(arsenal_matches))

## Inspect the structure of match data -- 
## Question: What information is available to us about each match?
# print("\nKeys in a match record:")
# print(arsenal_matches[0].keys())

## Get a sense of the dates and opponents of 5 matches
# for match in arsenal_matches:
#     print(
#         match["match_date"],
#         match["home_team"]["home_team_name"],
#         "vs",
#         match["away_team"]["away_team_name"]
#     )
#print(arsenal_matches[:5])

## Display the complete record in a legible manner
# print("\nFirst Arsenal match record:")
# print(json.dumps(arsenal_matches[0], indent=4))

## Create a match summary of the first 5 matches to see wins and losses
match_summary = []

# for match in arsenal_matches:
#     match_info = {
#         "date" : match["match_date"],
#         "home_team" : match["home_team"]["home_team_name"],
#         "away_team" : match["away_team"]["away_team_name"],
#         "home_score" : match.get("home_score"),
#         "away_score" : match.get("away_score"),
#         "match_id" : match["match_id"]
#     }

#     match_summary.append(match_info)

## Display the first 5 matches
# for match in match_summary:
#      print(json.dumps(match, indent = 4))

## Question: How many matches did Arsenal win?
# arsenal_wins = 0
# arsenal_draws = 0
# arsenal_losses = 0

# for match in match_summary:
#     if (match["away_team"] == "Arsenal"
#     and match.get("away_score") > match.get("home_score")
#     or match["home_team"] == "Arsenal"
#     and match.get("away_score") < match.get("home_score")):
#         arsenal_wins += 1
#     elif (match.get("away_score") == match.get("home_score")):
#         arsenal_draws += 1
#     else:
#         arsenal_losses += 1

# print("Arsenal Wins:", arsenal_wins)
# print("Arsenal Draws:", arsenal_draws)
# print("Arsenal Losses:", arsenal_losses)

#### END: DOWNLOAD 2015/2016 ARSENAL SEASON DATA ####
####################################################
#### START: DOWNLOAD DATA 4 ONE MATCH & EXAMINE DATA ####

## Question: What are the match_ids of every Arsenal match and who did they play?
# for match in arsenal_matches:
#     print(
#         match["match_sdate"],
#         match["match_id"],
#         match["home_team"]["home_team_name"],
#         "vs",
#         match["away_team"]["away_team_name"]
#     )

# Download event data for a single match of choice based on 7-digit match id -- note: different fields for match level data
event_url = (
    "https://raw.githubusercontent.com/hudl/open-data/"
    "master/data/events/3754217.json"
)

with urlopen(event_url) as response:
    events = json.load(response)

## Print stmts to be commented out if needed
# print("Total events in the match:", len(events))
# print("\nFirst event in the match:")
# print(json.dumps(events[0], indent=4))

## Question: What type of events were recorded in this match specifically?
event_counts = {} # this Dict will store each event type and how many times it appears

# for event in events:
#     event_type = event["type"]["name"] # retrieve event type name

#     if event_type in event_counts:
#         event_counts[event_type] += 1
#     else:
#         event_counts[event_type] = 1

# ## Display the event types, from most common to least common instead of by name of event type
# sorted_event_counts = sorted(
#     event_counts.items(),
#     key=lambda item: item[1],
#     reverse=True
# )

## Question: Which events occurred during this specific match and how many times?
# for event_type, count in sorted_event_counts:
#     print(f"{event_type}: {count}")

## Question: Where did a "shot" first occur in the match?
# for event in events:
#     if event["type"]["name"] == "Shot":
#         #print(json.dumps(event, indent=4))
#         print("Shot taken by: ")
#         print(event["player"]["name"])
#         print("for ")
#         print(event["team"]["name"])
#         print("Outcome: ")
#         print(["shot"]["outcome"]["name"])
#         break # Necessary bc we're only printing FIRST shot

## Extract Arsenal's shots
arsenal_shots = []

## Question: When did each shot by Arsenal occur, what was the outcome,
## who made the shot, what was the shot's xG, etc...?
for event in events:
    if (
        event["type"]["name"] == "Shot"
        and event["team"]["name"] == "Arsenal"
    ):
        shot_info = {
            "minute": event["minute"],
            "player": event["player"]["name"],
            "xg": event["shot"]["statsbomb_xg"],
            "outcome": event["shot"]["outcome"]["name"],
            "body_part": event["shot"]["body_part"]["name"]
        } 
        
        arsenal_shots.append(shot_info)

# for shot in arsenal_shots:
#     print(shot)

## Question: How many shots total did Arsenal take in this specific match?
# print(len(arsenal_shots))

# Some specific metrics from arsenal_shots

## Question: What's Arsenal's total expected goals over the entire match?
total_xg = 0

for shot in arsenal_shots:
    total_xg += shot['xg']

# print("Arsenal's total xG:", round(total_xg,2))

## Question: Which players took shots and how many?
player_shots = {}

for shot in arsenal_shots:
    player = shot["player"]

    if player in player_shots:
        player_shots[player] += 1
    else:
        player_shots[player] = 1

# print("\nShots by player: ")
# for player, count in player_shots.items():
#     print(f"{player}: {count}")

#### END: DOWNLOAD DATA 4 ONE MATCH & EXAMINE DATA ####
########################################################
#### START: DOWNLOAD SEASON DATA 4 ARSENAL ####

# Function to get any single match data
def analyze_arsenal_match(match_id):
    event_url = (
        "https://raw.githubusercontent.com/hudl/open-data/"
        f"master/data/events/{match_id}.json"
    )

    with urlopen(event_url) as response:
        events = json.load(response)

    arsenal_shots = []
    arsenal_goals = 0

    for event in events:
        if (
            event["type"]["name"] == "Shot"
            and event["team"]["name"] == "Arsenal"
        ):
            if event["shot"]["outcome"]["name"] == "Goal":
                arsenal_goals += 1

            shot_info = {
                "minute": event["minute"],
                "player": event["player"]["name"],
                "xg": event["shot"]["statsbomb_xg"],
                "outcome": event["shot"]["outcome"]["name"],
            }

            arsenal_shots.append(shot_info)

    total_shots = len(arsenal_shots)

    total_xg = 0
    for shot in arsenal_shots:
        total_xg += shot["xg"]

    return {
        "match_id": match_id,
        "arsenal_shots": total_shots,
        "arsenal_goals": arsenal_goals,
        "arsenal_xg": round(total_xg, 2)
    }

## Test "analyze_arsenal_match" by calling it
#result = analyze_arsenal_match(3754217)

## Get season results by calling "analyze_arsenal_match" on every match_id in arsenal_matches
season_results = []

for match in arsenal_matches:
    match_id = match["match_id"]

    result = analyze_arsenal_match(match_id)

    result["date"] = match["match_date"]
    result["opponent"] = (
        match["away_team"]["away_team_name"]
        if match["home_team"]["home_team_name"] == "Arsenal"
        else match["home_team"]["home_team_name"]
    )
    season_results.append(result)

# for result in season_results:
#     print(result)

#### END: DOWNLOAD SEASON DATA 4 ARSENAL ####
############################################
#### START: Display some stats from the season data ####

df = pd.DataFrame(season_results)
# print(df.head()) # Print the season_results as a table

## Question: How many rows & columns are in our season data?
# print(df.shape)
## Question: What are the different labels in the season's data set?
# print(df.columns)

## Question: What's the avg num of shots attempted by Arsenal per match?
# print("Average shots per match:", round(df["arsenal_shots"].mean(), 2))

## Question: What's the avg num of expected goals per match?
# print("Average xG per match:", round(df["arsenal_xg"].mean(), 2))

## Question: Which matches had the greatest quality of chances at goals (xG)?
best_xg_matches = df.sort_values(
    by="arsenal_xg",
    ascending=False # Largest values first
)

# print(best_xg_matches[
#     ["date", "opponent", "arsenal_shots", "arsenal_xg"]
# ].head(5))

#### END: Display some stats from the season data ####
############################################
#### START: Display some charts showing the relationship between 1) # of shots taken and xG, 2) ####

## Create a scatter plot to show the relationship between # of shots, xG

plt.figure(figsize=(8, 5)) ## 8 in wide, 5 in tall

plt.scatter(
    df["arsenal_shots"], ## Horizontal coordinates (x-axis)
    df["arsenal_xg"]     ## Vertical coordinates (y-axis)
)

## Calculate the slope and intercept
slope, intercept = np.polyfit(
    df["arsenal_shots"],
    df["arsenal_xg"],
    1
)

## Create 100 evenly spaced x-values between lowest & highest shot totals
x_values = np.linspace(
    df["arsenal_shots"].min(),
    df["arsenal_shots"].max(),
    100
)

y_values = slope * x_values + intercept ## Calculates the corresponding xG values

## Draw the trend line
plt.plot(
    x_values,
    y_values,
    label="Trend line"
)

plt.title("Arsenal Shots vs. Expected Goals (2015–2016)")
plt.xlabel("Shots per Match")
plt.ylabel("Expected Goals (xG)")

plt.legend()
plt.grid(True)      ## Add gridlines to make values easier to estimate
plt.tight_layout()
plt.savefig("shots_vs_xg.png", dpi=300, bbox_inches="tight")
plt.show()

## Question: Is the relationship between Shots and xG strong enough to measure statistically?
## Calculate the correlation coefficient
correlation = df["arsenal_shots"].corr(df["arsenal_xg"])
print("Correlation between Arsenal shots and xG over entire season: ", round(correlation,3))

## Analytics Question: Did Arsenal create more expected goals
## because it took more shots, or did the team also generate
## better-quality chances?

## Season level average of xG per shot (to get a basic measure of shot quality)
average_xg_per_shot = df["arsenal_xg"].sum() / df["arsenal_shots"].sum()
print("Average xG per shot:", round(average_xg_per_shot, 3))

## Calculate Arsenal's total goals and expected goals across the entire season
total_goals = df["arsenal_goals"].sum()
total_xg = df["arsenal_xg"].sum()

print("Total actual goals:", total_goals)
print("Total expected goals (xG):", round(total_xg, 2))

## Compare actual goals with expected goals at season level
goals_vs_xg = total_goals - total_xg

print("Goals minus xG:", round(goals_vs_xg, 2))

## Match level average xG per shot
df["xg_per_shot"] = df["arsenal_xg"] / df["arsenal_shots"] ## Calculate average xG per shot for each match

## Actual goals vs expected goals per match
df["goals_minus_xg"] = df["arsenal_goals"] - df["arsenal_xg"]

## Question: In which matches did Arsenal score most above xG?
print("\nMatches where Arsenal scored most above xG:")
print(
    df.sort_values(by="goals_minus_xg", ascending=False)[
        ["date", "opponent", "arsenal_goals", "arsenal_xg", "goals_minus_xg"]
    ].head(5).round(2)
)

## Question: In which matches did Arsenal score most below xG?
print("\nMatches where Arsenal scored most below xG:")
print(
    df.sort_values(by="goals_minus_xg", ascending=True)[
        ["date", "opponent", "arsenal_goals", "arsenal_xg", "goals_minus_xg"]
    ].head(5).round(2)
)

## Sort matches by shot quality, highest first
best_shot_quality = df.sort_values(
    by="xg_per_shot",
    ascending=False
)

# print("\nTop 5 matches by average xG per shot:")
# print(
#     best_shot_quality[
#         ["date", "opponent", "arsenal_shots", "arsenal_xg", "xg_per_shot"]
#     ].head(5).round(3)
# )

## Sort matches by average xG per shot, lowest first
worst_shot_quality = df.sort_values(
    by="xg_per_shot",
    ascending=True
)

print("\nBottom 5 matches by average xG per shot:")
print(
    worst_shot_quality[
        ["date", "opponent", "arsenal_shots", "arsenal_goals", "arsenal_xg", "xg_per_shot"]
    ].head(5).round(3)
)

## Second chart showing average xG per shot in each match
shot_quality_by_date = df.sort_values(by="date")

## Figure #2 answers the question: What is the average xG of all shots
## taken during each match? Were high or low quality opportunities made?
plt.figure(figsize=(12, 5)) ## 12 in wide, 5 in tall

plt.plot(
    shot_quality_by_date["date"],
    shot_quality_by_date["xg_per_shot"],
    marker="o"
)

## Show Arsenal's season-wide average
plt.axhline(
    y=average_xg_per_shot,
    linestyle="--",
    label="Season average"
)

plt.title("Arsenal Average xG per Shot by Match (2015–2016)")
plt.xlabel("Match Date")
plt.ylabel("Average xG per Shot")

plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("xg_per_shot_by_match.png", dpi=300, bbox_inches="tight")
plt.show()

## Figure #3 answers the question: How many goals did Arsenal actually score
## in comparison how to many goals their chances were expected to produce?
plt.figure(figsize=(8, 6))

plt.scatter(
    df["arsenal_xg"],
    df["arsenal_goals"]
)

## Reference line: actual goals equal expected goals
max_value = max(
    df["arsenal_xg"].max(),
    df["arsenal_goals"].max()
)

plt.plot(
    [0, max_value],
    [0, max_value],
    linestyle="--",
    label="Goals equal xG"
)

plt.title("Arsenal Actual Goals vs. Expected Goals (2015–2016)")
plt.xlabel("Expected Goals (xG)")
plt.ylabel("Actual Goals")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("goals_vs_xg.png", dpi=300, bbox_inches="tight")
plt.show()