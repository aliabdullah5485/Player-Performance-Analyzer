"""
Player Performance Analyzer
============================
Author: [Your Name]
Project: Habib University CS Application Portfolio
Description:
    Reads player statistics from a CSV file, calculates a weighted
    performance score for each player, sorts them by score (highest first),
    exports the ranked results to a new CSV file, and prints a summary.

Performance Formula:
    Score = (Points × 1.0) + (Assists × 1.5) + (Rebounds × 1.2)
          + (Steals × 2.0) − (Turnovers × 1.0)
"""

import csv
import os


# ─────────────────────────────────────────────
#  CONSTANTS — Weights used in the scoring formula
# ─────────────────────────────────────────────
WEIGHTS = {
    "Points":    1.0,
    "Assists":   1.5,
    "Rebounds":  1.2,
    "Steals":    2.0,
    "Turnovers": -1.0   # Negative weight — turnovers hurt performance
}

INPUT_FILE  = "players.csv"
OUTPUT_FILE = "ranked_players.csv"


# ─────────────────────────────────────────────
#  FUNCTION: Safe numeric conversion with validation
# ─────────────────────────────────────────────
def safe_float(value, field_name, player_name):
    """
    Safely converts a string value to a float.
    Returns None if the value is missing or non-numeric,
    and prints a warning so the user knows which data was skipped.

    Parameters:
        value       (str)  : The raw string from the CSV cell.
        field_name  (str)  : The column name (e.g., "Points").
        player_name (str)  : The player's name for error context.

    Returns:
        float | None
    """
    try:
        converted = float(value.strip())
        # Basic sanity check — stats shouldn't be negative
        if converted < 0:
            print(f"  [WARNING] '{field_name}' for '{player_name}' is negative "
                  f"({converted}). Treating as 0.")
            return 0.0
        return converted
    except (ValueError, AttributeError):
        print(f"  [WARNING] Invalid value for '{field_name}' in player "
              f"'{player_name}'. Treating as 0.")
        return 0.0


# ─────────────────────────────────────────────
#  FUNCTION: Calculate performance score
# ─────────────────────────────────────────────
def calculate_score(player):
    """
    Applies the weighted formula to compute a player's performance score.

    Formula:
        Score = (Points × 1.0) + (Assists × 1.5) + (Rebounds × 1.2)
              + (Steals × 2.0) − (Turnovers × 1.0)

    Parameters:
        player (dict): A dictionary with player stats as keys.

    Returns:
        float: The calculated performance score, rounded to 2 decimal places.
    """
    score = 0.0
    for stat, weight in WEIGHTS.items():
        score += player.get(stat, 0.0) * weight

    return round(score, 2)


# ─────────────────────────────────────────────
#  FUNCTION: Read players from CSV
# ─────────────────────────────────────────────
def read_players(filepath):
    """
    Reads player data from a CSV file and returns a list of player dictionaries
    with numeric stat values. Rows with a missing 'Name' field are skipped.

    Parameters:
        filepath (str): Path to the input CSV file.

    Returns:
        list[dict]: A list of player records with validated numeric stats.
    """
    players = []

    # Check that the file actually exists before opening it
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Input file '{filepath}' was not found. "
                                f"Please make sure it exists in the same folder.")

    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        # Validate that the CSV has all the expected columns
        required_columns = {"Name"} | set(WEIGHTS.keys())
        if not required_columns.issubset(set(reader.fieldnames or [])):
            missing = required_columns - set(reader.fieldnames or [])
            raise ValueError(f"CSV is missing required columns: {missing}")

        for row in reader:
            name = row.get("Name", "").strip()

            # Skip rows where the player name is blank
            if not name:
                print("  [WARNING] Found a row with no player name. Skipping.")
                continue

            # Build a clean player record with validated numeric stats
            player = {"Name": name}
            for stat in WEIGHTS.keys():
                player[stat] = safe_float(row.get(stat, "0"), stat, name)

            players.append(player)

    return players


# ─────────────────────────────────────────────
#  FUNCTION: Rank players by performance score
# ─────────────────────────────────────────────
def rank_players(players):
    """
    Calculates performance scores for all players and sorts them
    in descending order (highest score first).

    Parameters:
        players (list[dict]): Validated player records.

    Returns:
        list[dict]: Players sorted by 'Performance Score', highest first.
    """
    # Add a 'Performance Score' key to each player dictionary
    for player in players:
        player["Performance Score"] = calculate_score(player)

    # Sort by 'Performance Score' in descending order
    ranked = sorted(players, key=lambda p: p["Performance Score"], reverse=True)

    # Add rank numbers (1 = best) for clarity in the output
    for i, player in enumerate(ranked, start=1):
        player["Rank"] = i

    return ranked


# ─────────────────────────────────────────────
#  FUNCTION: Export ranked results to CSV
# ─────────────────────────────────────────────
def export_results(ranked_players, filepath):
    """
    Writes the ranked player data to a new CSV file.

    The output columns are ordered logically:
        Rank, Name, Points, Assists, Rebounds, Steals, Turnovers, Performance Score

    Parameters:
        ranked_players (list[dict]): Sorted player records with scores and ranks.
        filepath       (str)       : Path to the output CSV file.
    """
    # Define the exact column order for the output file
    fieldnames = ["Rank", "Name"] + list(WEIGHTS.keys()) + ["Performance Score"]

    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ranked_players)


# ─────────────────────────────────────────────
#  FUNCTION: Print a formatted leaderboard
# ─────────────────────────────────────────────
def print_leaderboard(ranked_players):
    """
    Prints a formatted leaderboard to the terminal for quick review.

    Parameters:
        ranked_players (list[dict]): Sorted player records.
    """
    print("\n" + "═" * 55)
    print("        🏆  PLAYER PERFORMANCE LEADERBOARD  🏆")
    print("═" * 55)
    print(f"{'Rank':<6} {'Name':<20} {'Score':>10}")
    print("─" * 55)
    for player in ranked_players:
        print(f"{player['Rank']:<6} {player['Name']:<20} {player['Performance Score']:>10.2f}")
    print("═" * 55)


# ─────────────────────────────────────────────
#  MAIN — Entry point of the program
# ─────────────────────────────────────────────
def main():
    """
    Orchestrates the full pipeline:
        1. Read player stats from CSV
        2. Calculate and rank by performance score
        3. Export ranked results to a new CSV
        4. Print leaderboard and confirmation
    """
    print("\n── Player Performance Analyzer ──")
    print(f"Reading data from '{INPUT_FILE}'...\n")

    try:
        # Step 1: Load player data
        players = read_players(INPUT_FILE)

        if not players:
            print("[ERROR] No valid player records found. Exiting.")
            return

        print(f"  ✓ Successfully loaded {len(players)} player(s).\n")

        # Step 2: Score and rank players
        ranked = rank_players(players)

        # Step 3: Export to CSV
        export_results(ranked, OUTPUT_FILE)

        # Step 4: Display results
        print_leaderboard(ranked)

        print(f"\n  ✓ Ranked results exported to '{OUTPUT_FILE}'.")
        print("  ✓ Analysis complete!\n")

    except FileNotFoundError as e:
        print(f"\n[FILE ERROR] {e}")
    except ValueError as e:
        print(f"\n[DATA ERROR] {e}")


# Run the program
if __name__ == "__main__":
    main()
