from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this'

def calculate_score(row):
    """Calculate performance score using the formula"""
    points = float(row.get('Points', 0))
    assists = float(row.get('Assists', 0))
    rebounds = float(row.get('Rebounds', 0))
    steals = float(row.get('Steals', 0))
    turnovers = float(row.get('Turnovers', 0))
    
    score = (points * 1.0) + (assists * 1.5) + (rebounds * 1.2) + (steals * 2.0) - (turnovers * 1.0)
    return round(score, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("DEBUG: Form was submitted!")
        
        if 'file' not in request.files:
            print("DEBUG: No file in request")
            return "No file uploaded", 400
        
        file = request.files['file']
        
        if file.filename == '':
            print("DEBUG: Empty filename")
            return "No file selected", 400
        
        print(f"DEBUG: File received - {file.filename}")
        
        try:
            # Read the CSV file
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                return "Please upload a CSV or Excel file", 400
            
            print(f"DEBUG: Data loaded - {len(df)} rows")
            
            # Calculate Score for each player
            df['Score'] = df.apply(calculate_score, axis=1)
            
            # Calculate advanced statistics
            highest_score = df['Score'].max()
            lowest_score = df['Score'].min()
            average_score = df['Score'].mean()
            top_scorer = df.loc[df['Score'].idxmax(), 'Name']
            
            # Sort by Score (highest to lowest)
            df = df.sort_values('Score', ascending=False)
            
            # Keep only Name and Score for display
            df_display = df[['Name', 'Score']]
            
            # Store data in session
            session['players'] = df_display.to_dict('records')
            session['stats'] = {
                'highest_score': round(highest_score, 2),
                'lowest_score': round(lowest_score, 2),
                'average_score': round(average_score, 2),
                'top_scorer': top_scorer,
                'total_players': len(df)
            }
            
            print(f"DEBUG: Processing complete - {len(df)} players ranked")
            print(f"DEBUG: Top scorer: {top_scorer} with {highest_score}")
            
            # Redirect to avoid form resubmission
            return redirect(url_for('index'))
            
        except Exception as e:
            print(f"DEBUG: Error occurred - {str(e)}")
            return f"Error processing file: {str(e)}", 500
    
    # GET request - retrieve data from session
    players = session.get('players', None)
    stats = session.get('stats', None)
    
    # Clear session after displaying
    if 'players' in session:
        session.pop('players')
    if 'stats' in session:
        session.pop('stats')
    
    return render_template('index.html', players=players, stats=stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)