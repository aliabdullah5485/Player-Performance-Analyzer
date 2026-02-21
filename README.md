# 🏆 Player Performance Analyzer

An advanced, data-driven web application for analyzing and ranking player performance across multiple metrics. Built with Flask, Python, and modern web technologies.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Overview

The Player Performance Analyzer is a comprehensive analytics platform that processes player statistics and generates detailed performance insights, rankings, and visualizations. It features an intuitive web interface with real-time data processing and interactive analytics.

## ✨ Key Features

### 📊 Advanced Analytics
- **Multi-Metric Scoring System** - Weighted formula considering Points, Assists, Rebounds, Steals, and Turnovers
- **Performance Tier Classification** - Automatic categorization into Elite, Strong, Average, and Developing tiers
- **Statistical Insights** - Highest, lowest, and average scores with comprehensive breakdowns
- **Category Leaders** - Identifies top performers in each individual metric

### 🎯 Interactive Visualizations
- **Score Distribution Chart** - Visual representation of performance distribution using Chart.js
- **Real-time Search** - Instant player search functionality
- **Tier Filtering** - Filter players by performance tier
- **Player Detail Cards** - Click any player to view complete metric breakdown

### 💾 Data Management
- **File Upload Support** - Accepts CSV and Excel (.xlsx, .xls) formats
- **Export Functionality** - Download analyzed results as CSV
- **Session Management** - Secure data handling with Flask sessions

### 🎨 Modern UI/UX
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Animated Counters** - Smooth number animations for statistics
- **Dark Theme** - Professional cyberpunk-inspired interface
- **Intuitive Navigation** - Clean, user-friendly layout

## 🚀 Technology Stack

- **Backend:** Flask (Python)
- **Data Processing:** Pandas
- **Frontend:** HTML5, CSS3, JavaScript
- **Visualization:** Chart.js
- **Styling:** Custom CSS with animations

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/aliabdullah5485/Player-Performance-Analyzer.git
cd Player-Performance-Analyzer
```

2. **Install dependencies**
```bash
pip install flask pandas openpyxl
```

3. **Run the application**
```bash
python app.py
```

4. **Access the application**
```
Open your browser and navigate to: http://localhost:5000
```

## 📖 Usage

### Input Data Format

Your CSV/Excel file should contain the following columns:

| Name | Points | Assists | Rebounds | Steals | Turnovers |
|------|--------|---------|----------|--------|-----------|
| Player Name | Numeric | Numeric | Numeric | Numeric | Numeric |

### Performance Score Formula

```
Score = (Points × 1.0) + (Assists × 1.5) + (Rebounds × 1.2) + (Steals × 2.0) - (Turnovers × 1.0)
```

This weighted formula emphasizes:
- **Steals** (2.0x) - High value on defensive plays
- **Assists** (1.5x) - Rewards playmaking ability
- **Rebounds** (1.2x) - Values positioning and hustle
- **Points** (1.0x) - Standard scoring metric
- **Turnovers** (-1.0x) - Penalizes ball control issues

### Performance Tiers

- **Elite:** Score ≥ 125% of average
- **Strong:** Score ≥ 105% of average
- **Average:** Score ≥ 85% of average
- **Developing:** Score < 85% of average

## 🎯 Features in Detail

### Search & Filter
- Real-time search by player name
- Filter by performance tier (Elite, Strong, Average, Developing)
- Instant results with smooth animations

### Interactive Player Cards
- Click any player to view detailed breakdown
- Shows all individual metrics
- Modal overlay with professional design

### Visual Analytics
- Bar chart showing score distribution across ranges
- Category leader cards for top performers
- Animated statistics cards

### Export Capabilities
- One-click CSV export
- Preserves all calculated fields
- Formatted for further analysis

## 📁 Project Structure

```
Player-Performance-Analyzer/
├── app.py                      # Flask application (backend)
├── templates/
│   └── index.html             # Main web interface
├── players.csv                # Sample data
├── performance.py             # Basic CLI script
├── performance_advanced.py    # Advanced CLI script
├── README.md                  # Documentation
└── ranked_players.csv         # Sample output
```

## 🎓 Learning Outcomes

This project demonstrates proficiency in:

- **Full-Stack Web Development** - Flask backend with modern frontend
- **Data Analysis** - Pandas for data manipulation and statistics
- **UI/UX Design** - Responsive, accessible interface design
- **Algorithm Development** - Custom scoring and classification systems
- **Software Architecture** - Clean, maintainable code structure
- **Problem Solving** - Real-world sports analytics application

## 🔮 Future Enhancements

- [ ] Player comparison feature (side-by-side analysis)
- [ ] Historical data tracking and trend analysis
- [ ] Advanced visualizations (radar charts, heat maps)
- [ ] Team formation optimizer
- [ ] PDF report generation
- [ ] Database integration for persistent storage
- [ ] User authentication and saved analyses
- [ ] API endpoints for external integration

## 👨‍💻 Author

**Ali Abdullah**
- GitHub: [@aliabdullah5485](https://github.com/aliabdullah5485)
- Project Link: [Player Performance Analyzer](https://github.com/aliabdullah5485/Player-Performance-Analyzer)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Inspired by modern sports analytics platforms
- Built as a demonstration of full-stack development capabilities
- Designed for educational and portfolio purposes

---

**Note:** This project showcases technical skills in web development, data analysis, and software design. It was created as part of a portfolio to demonstrate programming proficiency and problem-solving abilities for university applications and professional opportunities.
