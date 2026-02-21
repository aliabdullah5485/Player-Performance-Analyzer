from flask import Flask, render_template, request, redirect, url_for, session, send_file
import pandas as pd
import io
import json

app = Flask(__name__)
app.secret_key = 'player-performance-analyzer-2026-secret-key'

def calculate_score(row):
    """Calculate performance score using the weighted formula"""
    points = float(row.get('Points', 0))
    assists = float(row.get('Assists', 0))
    rebounds = float(row.get('Rebounds', 0))
    steals = float(row.get('Steals', 0))
    turnovers = float(row.get('Turnovers', 0))
    
    score = (points * 1.0) + (assists * 1.5) + (rebounds * 1.2) + (steals * 2.0) - (turnovers * 1.0)
    return round(score, 2)

def categorize_performance(score, avg_score):
    """Categorize player performance into tiers"""
    if score >= avg_score * 1.25:
        return "Elite"
    elif score >= avg_score * 1.05:
        return "Strong"
    elif score >= avg_score * 0.85:
        return "Average"
    else:
        return "Developing"

def get_player_strengths(row):
    """Identify top 2 strengths for a player"""
    metrics = {
        'Scoring': float(row.get('Points', 0)) * 1.0,
        'Playmaking': float(row.get('Assists', 0)) * 1.5,
        'Rebounding': float(row.get('Rebounds', 0)) * 1.2,
        'Defense': float(row.get('Steals', 0)) * 2.0
    }
    sorted_metrics = sorted(metrics.items(), key=lambda x: x[1], reverse=True)
    return [metric[0] for metric in sorted_metrics[:2]]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
        
        file = request.files['file']
        
        if file.filename == '':
            return "No file selected", 400
        
        try:
            # Read the file
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                return "Please upload a CSV or Excel file", 400
            
            # Calculate scores
            df['Score'] = df.apply(calculate_score, axis=1)
            
            # Calculate statistics
            highest_score = df['Score'].max()
            lowest_score = df['Score'].min()
            average_score = df['Score'].mean()
            top_scorer = df.loc[df['Score'].idxmax(), 'Name']
            
            # Add performance tiers
            df['Tier'] = df['Score'].apply(lambda x: categorize_performance(x, average_score))
            
            # Add player strengths
            df['Strengths'] = df.apply(lambda row: ', '.join(get_player_strengths(row)), axis=1)
            
            # Sort by Score
            df = df.sort_values('Score', ascending=False)
            
            # Calculate category leaders
            category_leaders = {
                'points': {'name': df.loc[df['Points'].idxmax(), 'Name'], 
                          'value': float(df['Points'].max())},
                'assists': {'name': df.loc[df['Assists'].idxmax(), 'Name'], 
                           'value': float(df['Assists'].max())},
                'rebounds': {'name': df.loc[df['Rebounds'].idxmax(), 'Name'], 
                            'value': float(df['Rebounds'].max())},
                'steals': {'name': df.loc[df['Steals'].idxmax(), 'Name'], 
                          'value': float(df['Steals'].max())}
            }
            
            # Calculate score distribution for chart
            score_bins = [0, 30, 40, 50, 60, 100]
            score_labels = ['0-30', '30-40', '40-50', '50-60', '60+']
            df['ScoreBin'] = pd.cut(df['Score'], bins=score_bins, labels=score_labels, include_lowest=True)
            score_distribution = df['ScoreBin'].value_counts().sort_index().to_dict()
            score_distribution = {str(k): int(v) for k, v in score_distribution.items()}
            
            # Prepare full player data for detail view
            players_full = df.to_dict('records')
            
            # Display data (Name, Score, Tier)
            df_display = df[['Name', 'Score', 'Tier', 'Strengths']]
            
            # Store in session
            session['players'] = df_display.to_dict('records')
            session['players_full'] = players_full
            session['stats'] = {
                'highest_score': round(highest_score, 2),
                'lowest_score': round(lowest_score, 2),
                'average_score': round(average_score, 2),
                'top_scorer': top_scorer,
                'total_players': len(df)
            }
            session['category_leaders'] = category_leaders
            session['score_distribution'] = score_distribution
            
            return redirect(url_for('index'))
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return f"Error processing file: {str(e)}", 500
    
    # GET request
    players = session.get('players', None)
    players_full = session.get('players_full', None)
    stats = session.get('stats', None)
    category_leaders = session.get('category_leaders', None)
    score_distribution = session.get('score_distribution', None)
    
    # Don't clear session - keep data available
    
    return render_template('index.html', 
                         players=players, 
                         players_full=json.dumps(players_full) if players_full else None,
                         stats=stats,
                         category_leaders=category_leaders,
                         score_distribution=json.dumps(score_distribution) if score_distribution else None)

@app.route('/export')
def export():
    """Export current results as CSV"""
    players = session.get('players', None)
    if not players:
        return "No data to export", 400
    
    # Create DataFrame
    df = pd.DataFrame(players)
    
    # Create CSV in memory
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    # Convert to bytes
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    
    return send_file(
        mem,
        mimetype='text/csv',
        as_attachment=True,
        download_name='player_performance_results.csv'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)