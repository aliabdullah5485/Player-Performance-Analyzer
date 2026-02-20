"""
Player Performance Analyzer — Advanced Version (pandas)
=========================================================
Author: [Your Name]
Project: Habib University CS Application Portfolio
Description:
    An improved version of the Player Performance Analyzer using pandas
    for more powerful data manipulation, cleaner validation, and richer
    summary statistics.

Performance Formula:
    Score = (Points × 1.0) + (Assists × 1.5) + (Rebounds × 1.2)
          + (Steals × 2.0) − (Turnovers × 1.0)
"""

import pandas as pd
import os


# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
WEIGHTS = {
    "Points":    1.0,
    "Assists":   1.5,
    "Rebounds":  1.2,
    "Steals":    2.0,
    "Turnovers": -1.0
}

INPUT_FILE  = "players.csv"
OUTPUT_FILE = "ranked_players_advanced.csv"


# ─────────────────────────────────────────────
#  FUNCTION: Load and validate data
# ─────────────────────────────────────────────
def load_and_validate(filepath):
    """
    Loads the CSV file into a pandas DataFrame.
    Validates column presence, coerces non-numeric stat values to NaN,
    fills NaN stats with 0, and drops rows with no player name.

    Parameters:
        filepath (str): Path to the input CSV file.

    Returns:
        pd.DataFrame: A cleaned DataFrame ready for analysis.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find '{filepath}'. "
                                "Please check the file path.")

    df = pd.read_csv(filepath)

    # Check that all required columns are present
    required = {"Name"} | set(WEIGHTS.keys())
    missing_cols = required - set(df.columns)
    if missing_cols:
        raise ValueError(f"CSV is missing required columns: {missing_cols}")

    # Drop rows where Name is blank or NaN
    initial_count = len(df)
    df = df.dropna(subset=["Name"])
    df = df[df["Name"].str.strip() != ""]
    dropped = initial_count - len(df)
    if dropped > 0:
        print(f"  [WARNING] Dropped {dropped} row(s) with missing player names.")

    # Coerce all stat columns to numeric, setting invalid strings to NaN
    stat_cols = list(WEIGHTS.keys())
    df[stat_cols] = df[stat_cols].apply(pd.to_numeric, errors="coerce")

    # Count how many NaN values were found across stat columns
    nan_count = df[stat_cols].isna().sum().sum()
    if nan_count > 0:
        print(f"  [WARNING] Found {nan_count} invalid stat value(s). "
              "Replacing with 0.")

    # Fill any NaN stats with 0 and clip negatives to 0
    df[stat_cols] = df[stat_cols].fillna(0).clip(lower=0)

    # Clean whitespace from player names
    df["Name"] = df["Name"].str.strip()

    return df


# ─────────────────────────────────────────────
#  FUNCTION: Calculate performance scores
# ─────────────────────────────────────────────
def calculate_scores(df):
    """
    Applies the weighted formula to each row and adds a
    'Performance Score' column to the DataFrame.

    The formula is applied using a dot product of the stat columns
    and their corresponding weights — concise and efficient with pandas.

    Parameters:
        df (pd.DataFrame): Cleaned player DataFrame.

    Returns:
        pd.DataFrame: DataFrame with an added 'Performance Score' column.
    """
    stat_cols = list(WEIGHTS.keys())
    weight_values = list(WEIGHTS.values())

    # Dot product of stat values × weights = performance score
    df["Performance Score"] = (
        df[stat_cols]
        .mul(weight_values)   # Multiply each column by its weight
        .sum(axis=1)          # Sum across columns for each row
        .round(2)             # Round to 2 decimal places
    )

    return df


# ─────────────────────────────────────────────
#  FUNCTION: Rank and sort players
# ─────────────────────────────────────────────
def rank_players(df):
    """
    Sorts players by 'Performance Score' in descending order
    and adds a 'Rank' column (1 = best).

    Parameters:
        df (pd.DataFrame): DataFrame with performance scores.

    Returns:
        pd.DataFrame: Sorted DataFrame with a 'Rank' column.
    """
    df = df.sort_values("Performance Score", ascending=False)
    df.insert(0, "Rank", range(1, len(df) + 1))
    df = df.reset_index(drop=True)
    return df


# ─────────────────────────────────────────────
#  FUNCTION: Print leaderboard
# ─────────────────────────────────────────────
def print_leaderboard(df):
    """
    Prints a formatted leaderboard to the terminal.

    Parameters:
        df (pd.DataFrame): Ranked player DataFrame.
    """
    print("\n" + "═" * 55)
    print("        🏆  PLAYER PERFORMANCE LEADERBOARD  🏆")
    print("═" * 55)
    print(f"{'Rank':<6} {'Name':<20} {'Score':>10}")
    print("─" * 55)
    for _, row in df.iterrows():
        print(f"{int(row['Rank']):<6} {row['Name']:<20} {row['Performance Score']:>10.2f}")
    print("═" * 55)


# ─────────────────────────────────────────────
#  FUNCTION: Print summary statistics
# ─────────────────────────────────────────────
def print_summary(df):
    """
    Prints descriptive summary statistics for the performance scores
    and each individual stat — useful for analysis and insight.

    Parameters:
        df (pd.DataFrame): Ranked player DataFrame.
    """
    print("\n── Summary Statistics ──────────────────────────────")
    stats_df = df[list(WEIGHTS.keys()) + ["Performance Score"]].describe().round(2)
    print(stats_df.to_string())
    print()

    top = df.iloc[0]
    print(f"  🥇 Top Performer : {top['Name']} ({top['Performance Score']} pts)")
    print(f"  📊 Average Score : {df['Performance Score'].mean():.2f}")
    print(f"  📈 Highest Score : {df['Performance Score'].max():.2f}")
    print(f"  📉 Lowest Score  : {df['Performance Score'].min():.2f}")


# ─────────────────────────────────────────────
#  FUNCTION: Export to CSV
# ─────────────────────────────────────────────
def export_results(df, filepath):
    """
    Exports the ranked DataFrame to a CSV file.

    Parameters:
        df       (pd.DataFrame): Ranked player DataFrame.
        filepath (str)         : Output file path.
    """
    df.to_csv(filepath, index=False)


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    print("\n── Player Performance Analyzer (Advanced / pandas) ──")
    print(f"Reading data from '{INPUT_FILE}'...\n")

    try:
        # Pipeline: Load → Score → Rank → Display → Export
        df = load_and_validate(INPUT_FILE)
        print(f"  ✓ Loaded {len(df)} player(s) successfully.\n")

        df = calculate_scores(df)
        df = rank_players(df)

        print_leaderboard(df)
        print_summary(df)

        export_results(df, OUTPUT_FILE)

        print(f"\n  ✓ Ranked results exported to '{OUTPUT_FILE}'.")
        print("  ✓ Analysis complete!\n")

    except FileNotFoundError as e:
        print(f"\n[FILE ERROR] {e}")
    except ValueError as e:
        print(f"\n[DATA ERROR] {e}")


if __name__ == "__main__":
    main()
