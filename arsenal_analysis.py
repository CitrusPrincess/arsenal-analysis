"""
Author: Hanna Ross
Date: 03 Nov 2026

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

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from urllib.request import urlopen

#### START: DOWNLOAD 2015/2016 ARSENAL SEASON DATA ####

## The URL for Premier League 2015/2016 match data
url = (
    "https://raw.githubusercontent.com/hudl/open-data/"
    "master/data/matches/2/27.json"
)

## Download the data
with urlopen(url) as response:
    matches = json.load(response)

## Keep only Arsenal match data in list
arsenal_matches = []

## Extract Arsenal matches only
for match in matches:
    home_team = match["home_team"]["home_team_name"]
    away_team = match["away_team"]["away_team_name"]

    if home_team == "Arsenal" or away_team == "Arsenal":
        arsenal_matches.append(match)

#### END: DOWNLOAD 2015/2016 ARSENAL SEASON DATA ####
########################################################
#### START: DOWNLOAD SEASON DATA 4 ARSENAL ####

## Function to get any single match data given its match_id
def analyze_arsenal_match(match_id):
    event_url = (
        "https://raw.githubusercontent.com/hudl/open-data/"
        f"master/data/events/{match_id}.json"
    )

    with urlopen(event_url) as response:
        events = json.load(response)

    arsenal_shots = []
    arsenal_goals = 0

    ## Loop through all events in the match and extract Arsenal's shots
    for event in events:
        if (
            event["type"]["name"] == "Shot"
            and event["team"]["name"] == "Arsenal"
        ):
            ## Keep track of Arsenal's goals
            if event["shot"]["outcome"]["name"] == "Goal":
                arsenal_goals += 1

            ## Maintain data for each Arsenal shot
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
        "arsenal_xg": total_xg
    }

## Get season results by calling "analyze_arsenal_match"
## on every match_id in arsenal_matches
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

#### END: DOWNLOAD SEASON DATA 4 ARSENAL ####
############################################
#### START: Display some stats from the season data ####

print("Arsenal 2015/2016 Season Result (38 Matches):\n")
df = pd.DataFrame(season_results)

## Question: What's the avg num of shots attempted by Arsenal per match?
print("Average shots per match:", round(df["arsenal_shots"].mean(), 2))

## Question: What's the avg num of expected goals per match?
print("Average xG per match:", round(df["arsenal_xg"].mean(), 2))

## Question: Which matches had the greatest quality of chances at goals (xG)?
best_xg_matches = df.sort_values(
    by="arsenal_xg",
    ascending=False # Largest values first
)

print("\nTop 5 matches by xG:")
print(best_xg_matches[
    ["date", "opponent", "arsenal_shots", "arsenal_xg"]
].head(5))

#### END: Display some stats from the season data ####
############################################
#### START: Display charts to visualize Arsenal's attacking performance ####

## Plot the relationship between # of shots and xG
plt.figure(figsize=(8, 5))

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
plt.grid(True)
plt.tight_layout()
plt.savefig("charts/shots_vs_xg.png", dpi=300, bbox_inches="tight")
plt.show()

## Question: Is the relationship between Shots and xG strong enough to indicate a meaningful pattern?
## Calculate the correlation coefficient
correlation = df["arsenal_shots"].corr(df["arsenal_xg"])
print("\nCorrelation between Arsenal shots and xG over entire season: ", round(correlation,3))

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
df["xg_per_shot"] = (
    df["arsenal_xg"] / df["arsenal_shots"].replace(0, np.nan)
)

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

print("\nTop 5 matches by average xG per shot:")
print(
    best_shot_quality[
        ["date", "opponent", "arsenal_shots", "arsenal_xg", "xg_per_shot"]
    ].head(5).round(3)
)

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
plt.figure(figsize=(12, 5))

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
plt.savefig("charts/xg_per_shot_by_match.png", dpi=300, bbox_inches="tight")
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
plt.savefig("charts/goals_vs_xg.png", dpi=300, bbox_inches="tight")
plt.show()

#### END: Display charts to visualize Arsenal's attacking performance ####