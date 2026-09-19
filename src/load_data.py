import pandas as pd

df1 = pd.read_csv("data/E0 (6).csv")
df2 = pd.read_csv("data/E0 (5).csv")
df3 = pd.read_csv("data/E0 (4).csv")
df4 = pd.read_csv("data/E0 (3).csv")
df5 = pd.read_csv("data/E0 (2).csv")
df6 = pd.read_csv("data/E0 (1).csv")
df7 = pd.read_csv("data/E0.csv")

df = pd.concat(
    [df1, df2, df3, df4, df5, df6, df7],
    ignore_index=True
)
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df = df.sort_values("Date").reset_index(drop=True)


team_history = {}
elo_ratings = {}

home_elo_list = []
away_elo_list = []
home_form5_list = []
away_form5_list = []


home_goals_for5_list = []
home_goals_against5_list = []
home_shots5_list = []
home_sot5_list = []
home_corners5_list = []

away_goals_for5_list = []
away_goals_against5_list = []
away_shots5_list = []
away_sot5_list = []
away_corners5_list = []
for index, row in df.iterrows():

    home_team = row["HomeTeam"]
    away_team = row["AwayTeam"]
    if home_team not in elo_ratings:
       elo_ratings[home_team] = 1500

    if away_team not in elo_ratings:
       elo_ratings[away_team] = 1500

    home_elo = elo_ratings[home_team]
    away_elo = elo_ratings[away_team]

    home_elo_list.append(home_elo)
    away_elo_list.append(away_elo)
    
    if home_team not in team_history:
        team_history[home_team] = {
            "points": [],
            "goals_for": [],
            "goals_against": [],
            "shots": [],
            "shots_on_target": [],
            "corners": []
        }

    if away_team not in team_history:
        team_history[away_team] = {
            "points": [],
            "goals_for": [],
            "goals_against": [],
            "shots": [],
            "shots_on_target": [],
            "corners": []
        }
    home_points_history = team_history[home_team]["points"]
    away_points_history = team_history[away_team]["points"]
    home_goals_for_history = team_history[home_team]["goals_for"]
    home_goals_against_history = team_history[home_team]["goals_against"]
    home_shots_history = team_history[home_team]["shots"]
    home_sot_history = team_history[home_team]["shots_on_target"]
    home_corners_history = team_history[home_team]["corners"]

    away_goals_for_history = team_history[away_team]["goals_for"]
    away_goals_against_history = team_history[away_team]["goals_against"]
    away_shots_history = team_history[away_team]["shots"]
    away_sot_history = team_history[away_team]["shots_on_target"]
    away_corners_history = team_history[away_team]["corners"]
    

    home_form5 = sum(home_points_history[-5:]) / len(home_points_history[-5:]) if home_points_history else 0
    away_form5 = sum(away_points_history[-5:]) / len(away_points_history[-5:]) if away_points_history else 0
    home_goals_for5 = sum(home_goals_for_history[-5:]) / len(home_goals_for_history[-5:]) if home_goals_for_history else 0
    home_goals_against5 = sum(home_goals_against_history[-5:]) / len(home_goals_against_history[-5:]) if home_goals_against_history else 0
    home_shots5 = sum(home_shots_history[-5:]) / len(home_shots_history[-5:]) if home_shots_history else 0
    home_sot5 = sum(home_sot_history[-5:]) / len(home_sot_history[-5:]) if home_sot_history else 0
    home_corners5 = sum(home_corners_history[-5:]) / len(home_corners_history[-5:]) if home_corners_history else 0

    away_goals_for5 = sum(away_goals_for_history[-5:]) / len(away_goals_for_history[-5:]) if away_goals_for_history else 0
    away_goals_against5 = sum(away_goals_against_history[-5:]) / len(away_goals_against_history[-5:]) if away_goals_against_history else 0
    away_shots5 = sum(away_shots_history[-5:]) / len(away_shots_history[-5:]) if away_shots_history else 0
    away_sot5 = sum(away_sot_history[-5:]) / len(away_sot_history[-5:]) if away_sot_history else 0
    away_corners5 = sum(away_corners_history[-5:]) / len(away_corners_history[-5:]) if away_corners_history else 0
    home_form5_list.append(home_form5)
    away_form5_list.append(away_form5)
    home_goals_for5_list.append(home_goals_for5)
    home_goals_against5_list.append(home_goals_against5)
    home_shots5_list.append(home_shots5)
    home_sot5_list.append(home_sot5)
    home_corners5_list.append(home_corners5)

    away_goals_for5_list.append(away_goals_for5)
    away_goals_against5_list.append(away_goals_against5)
    away_shots5_list.append(away_shots5)
    away_sot5_list.append(away_sot5)
    away_corners5_list.append(away_corners5) 
    home_goals = row["FTHG"]
    away_goals = row["FTAG"]

    home_shots = row["HS"]
    away_shots = row["AS"]

    home_sot = row["HST"]
    away_sot = row["AST"]

    home_corners = row["HC"]
    away_corners = row["AC"]

    result = row["FTR"]

    expected_home = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
    expected_away = 1 - expected_home
    if result == "H":
      actual_home = 1
      actual_away = 0

    elif result == "D":
      actual_home = 0.5
      actual_away = 0.5

    else:
      actual_home = 0
      actual_away = 1 
    

    new_home_elo = home_elo + 20 * (actual_home - expected_home)
    new_away_elo = away_elo + 20 * (actual_away - expected_away)

    elo_ratings[home_team] = new_home_elo
    elo_ratings[away_team] = new_away_elo

    if result == "H":
        home_points = 3
        away_points = 0

    elif result == "D":
        home_points = 1
        away_points = 1

    else:
        home_points = 0
        away_points = 3
    

    team_history[home_team]["points"].append(home_points)
    team_history[home_team]["goals_for"].append(home_goals)
    team_history[home_team]["goals_against"].append(away_goals)
    team_history[home_team]["shots"].append(home_shots)
    team_history[home_team]["shots_on_target"].append(home_sot)
    team_history[home_team]["corners"].append(home_corners)

    team_history[away_team]["points"].append(away_points)
    team_history[away_team]["goals_for"].append(away_goals)
    team_history[away_team]["goals_against"].append(home_goals)
    team_history[away_team]["shots"].append(away_shots)
    team_history[away_team]["shots_on_target"].append(away_sot)
    team_history[away_team]["corners"].append(away_corners)

df["home_form5"] = home_form5_list
df["away_form5"] = away_form5_list
df["home_goals_for5"] = home_goals_for5_list
df["home_goals_against5"] = home_goals_against5_list
df["home_shots5"] = home_shots5_list
df["home_sot5"] = home_sot5_list
df["home_corners5"] = home_corners5_list

df["away_goals_for5"] = away_goals_for5_list
df["away_goals_against5"] = away_goals_against5_list
df["away_shots5"] = away_shots5_list
df["away_sot5"] = away_sot5_list
df["away_corners5"] = away_corners5_list
df["home_elo"] = home_elo_list
df["away_elo"] = away_elo_list

df["elo_diff"] = df["home_elo"] - df["away_elo"]


df["goal_diff5"] = (
    df["home_goals_for5"] - df["home_goals_against5"]
) - (
    df["away_goals_for5"] - df["away_goals_against5"]
)

df["shot_diff5"] = df["home_shots5"] - df["away_shots5"]

df["sot_diff5"] = df["home_sot5"] - df["away_sot5"]

df["corner_diff5"] = df["home_corners5"] - df["away_corners5"]

df["form_diff5"] = df["home_form5"] - df["away_form5"]

features = [
    "home_form5",
    "away_form5",
    "home_goals_for5",
    "away_goals_for5",
    "home_goals_against5",
    "away_goals_against5",
    "home_shots5",
    "away_shots5",
    "home_sot5",
    "away_sot5",
    "home_corners5",
    "away_corners5",
    "elo_diff",
    "goal_diff5",
    "shot_diff5",
    "sot_diff5",
    "corner_diff5",
    "form_diff5"
]

X = df[features]
y = df["FTR"]

split = int(len(df) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
"""
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)
from sklearn.metrics import confusion_matrix, classification_report

print(confusion_matrix(y_test, y_pred))

print(classification_report(y_test, y_pred))

"""
importance = pd.Series(
    model.feature_importances_,
    index=features
).sort_values(ascending=False)

print(importance)

