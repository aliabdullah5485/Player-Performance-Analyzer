# 🏆 Player Performance Analyzer

A beginner-to-intermediate Python automation project that reads player statistics from a CSV file, calculates a weighted performance score for each player, ranks them, and exports the results — all automatically.

Built as a portfolio project for a Computer Science application, this project demonstrates data processing, algorithm design, automation, and clean code practices.

---

## 📌 Project Overview

Given a CSV file of basketball player statistics, the analyzer:

1. **Reads** the raw data from `players.csv`
2. **Validates** entries — handling missing, invalid, or negative values gracefully
3. **Calculates** a custom weighted performance score for each player
4. **Sorts** players by score from highest to lowest
5. **Exports** the ranked results to a new `ranked_players.csv` file
6. **Prints** a formatted leaderboard and confirmation to the terminal

---

## ✨ Features

- Clean function-based structure (readable and maintainable)
- Input validation with descriptive warnings for bad data
- Handles missing or non-numeric stat values without crashing
- Prints a formatted leaderboard directly in the terminal
- Exports ranked results to a new CSV automatically
- Two versions available:
  - `performance.py` — uses Python's built-in `csv` module (no dependencies)
  - `performance_advanced.py` — uses `pandas` for richer analysis and summary statistics

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| Python 3.x | Core programming language |
| `csv` (built-in) | Reading and writing CSV files |
| `pandas` | Data manipulation (advanced version) |
| `os` (built-in) | File existence validation |

---

## 📂 Project Structure

```
player-performance-analyzer/
│
├── players.csv                  # Input: raw player statistics
├── performance.py               # Main script (csv module version)
├── performance_advanced.py      # Advanced script (pandas version)
├── ranked_players.csv           # Output: generated after running the script
└── README.md                    # This file
```

---

## 📊 Performance Formula

Each player's score is computed using this weighted formula:

```
Score = (Points × 1.0) + (Assists × 1.5) + (Rebounds × 1.2)
      + (Steals × 2.0) − (Turnovers × 1.0)
```

**Why these weights?**

| Stat | Weight | Reasoning |
|------|--------|-----------|
| Points | 1.0 | Standard offensive contribution |
| Assists | 1.5 | Valued higher — reflects playmaking and team play |
| Rebounds | 1.2 | Important for possession control |
| Steals | 2.0 | High-impact defensive play, directly creates turnovers for the other team |
| Turnovers | −1.0 | Penalized — a turnover gives the opponent an opportunity |

---

## ▶️ How to Run

### Prerequisites

- Python 3.7 or higher installed
- For the advanced version: `pandas` library

Install pandas (if needed):

```bash
pip install pandas
```

### Steps

1. **Clone or download** this repository.

2. **Make sure `players.csv` is in the same folder** as the script.

3. **Run the basic version** (no extra libraries needed):

```bash
python performance.py
```

4. **Or run the advanced pandas version:**

```bash
python performance_advanced.py
```

5. **Check the output:**
   - A ranked leaderboard is printed in the terminal
   - A new file `ranked_players.csv` (or `ranked_players_advanced.csv`) is created automatically

---

## 📋 Sample Input (`players.csv`)

```csv
Name,Points,Assists,Rebounds,Steals,Turnovers
Ali Hassan,22,7,10,3,2
Sara Khan,18,12,6,4,3
Zain Mirza,30,5,8,2,4
Fatima Noor,15,9,11,5,1
Hamza Raza,25,6,9,3,3
```

## 📋 Sample Output (`ranked_players.csv`)

```csv
Rank,Name,Points,Assists,Rebounds,Steals,Turnovers,Performance Score
1,Fatima Noor,15,9,11,5,1,52.7
2,Mariam Yousuf,23,11,9,5,3,55.3
...
```

---

## ⚙️ Input Validation Behavior

The script handles messy data gracefully:

| Issue | Behavior |
|-------|---------|
| Missing stat value | Treated as `0`, warning printed |
| Non-numeric value (e.g. `"N/A"`) | Treated as `0`, warning printed |
| Negative stat value | Clipped to `0`, warning printed |
| Missing player name | Row is skipped entirely |
| File not found | Descriptive error message, clean exit |
| Missing required columns | Descriptive error message, clean exit |

---

## 🔮 Future Improvements

### 1. 🌐 Web Dashboard (Flask or Streamlit)
Build an interactive web interface where users can upload a CSV, adjust stat weights using sliders, and see the leaderboard update in real time — making the tool far more usable and impressive.

### 2. 📈 Data Visualization (matplotlib / seaborn)
Generate bar charts, radar plots per player, and score distribution graphs automatically alongside the CSV export. Visual output dramatically improves the impact of the analysis.

### 3. 🔧 Configurable Weights via CLI or Config File
Allow users to pass custom weights at runtime (e.g. `--steals-weight 3.0`) using `argparse`, or load weights from a `config.json` file — making the tool flexible for any sport or scoring system without touching the code.

---

## 👤 Author

**[Your Name]**  
Computer Science Applicant — Habib University  
[Your GitHub Profile] | [Your Email]

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
