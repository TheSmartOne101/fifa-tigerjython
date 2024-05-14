import csv
import random
import time
import codecs
from collections import defaultdict

# Definieren der Spielerklasse
class Spieler:
    def __init__(self, name, full_name, birth_date, age, height_cm, weight_kgs, positions, nationality, overall_rating, potential, value_euro, wage_euro):
        self.name = name
        self.full_name = full_name
        self.birth_date = birth_date
        self.age = int(age) if age.isdigit() else 0
        self.height_cm = int(height_cm) if height_cm.isdigit() else 0
        self.weight_kgs = int(weight_kgs) if weight_kgs.isdigit() else 0
        self.positions = positions.split(',')
        self.nationality = nationality
        self.overall_rating = int(overall_rating) if overall_rating.isdigit() else 0
        self.potential = potential
        self.value_euro = float(value_euro.replace(',', '.')) if value_euro else 0.0
        self.wage_euro = float(wage_euro.replace(',', '.')) if wage_euro else 0.0

# Funktion zum Einlesen der Spielerdaten aus einer CSV-Datei
def read_players(filename):
    players = []
    with codecs.open(filename, 'r', 'utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            player = Spieler(row['name'], row['full_name'], row['birth_date'], row['age'], row['height_cm'], row['weight_kgs'], row['positions'], row['nationality'], row['overall_rating'], row['potential'], row['value_euro'], row['wage_euro'])
            players.append(player)
    return players

# Funktion zur Verteilung der Spieler auf zwei Teams
def distribute_players(players, team_size=10):
    random.shuffle(players)
    teams = [players[:team_size], players[team_size:team_size*2]]
    return teams

# Funktion zur Simulation eines Spiels mit zufälliger Punktevergabe
def simulate_match():
    team1_score = 0
    team2_score = 0

    for _ in range(3):
        winner = random.choice([1, 2])  # Zufälliger Gewinner für dieses Spiel
        if winner == 1:
            team1_score += 1
        else:
            team2_score += 1

        print("Spielstand: %d - %d" % (team1_score, team2_score))
        time.sleep(1)  # 1 Sekunde Pause

    return team1_score, team2_score

# Funktion zum Speichern des Spielergebnisses in einer CSV-Datei
def save_result(team1, team2, team1_score, team2_score):
    result = []
    if team1_score > team2_score:
        winner, loser = team1, team2
    else:
        winner, loser = team2, team1

    result.append(','.join([player.name.encode("utf32") for player in winner]))
    result.append(','.join([player.name.encode("utf32") for player in loser]))

    with codecs.open('ergebnisse.csv', 'a', 'utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(result)

# Hauptfunktion zur Ausführung des Programms
def main():
    players = read_players('Fifa_Players_2018_reduziert.csv')

    [team1, team2] = distribute_players(players)
    print("Willkommen zum Fußballspiel-Simulator!")
    time.sleep(1)

    # Wetten-Option
    bet = raw_input("Möchten Sie auf ein Team wetten? (j/n) ")
    if bet.lower() == "j":
        team_choice = raw_input("Auf welches Team möchten Sie wetten? (1/2) ")
        if team_choice == "1":
            chosen_team = team1
        elif team_choice == "2":
            chosen_team = team2
        else:
            print("Ungültige Eingabe. Kein Wetten.")
            chosen_team = None
    else:
        chosen_team = None

    print("\nTeam 1:")
    for player in team1:
        print("  %s (%s)" % (player.name, ', '.join(player.positions)))

    print("\nTeam 2:")
    for player in team2:
        print("  %s (%s)" % (player.name, ', '.join(player.positions)))

    print("\nSpielstand: 0 - 0")
    team1_score, team2_score = simulate_match()
    print("\nEndstand: Team 1 %d - %d Team 2" % (team1_score, team2_score))
    save_result(team1, team2, team1_score, team2_score)

    # Wetten-Ergebnis
    if chosen_team:
        if (team1_score > team2_score and chosen_team == team1) or (team1_score < team2_score and chosen_team == team2):
            print("Glückwunsch, Sie haben gewonnen!")
        else:
            print("Tut mir leid, Sie haben verloren.")

if __name__ == "__main__":
    main()
