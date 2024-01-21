from flask import render_template, Flask, jsonify, request, send_from_directory
import random
import json
import csv
from elo import EloRating

app = Flask(__name__, static_folder='../client/svelte/static')

@app.route("/")
def base():
    return send_from_directory('../client/svelte/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('../client/svelte/public', path)


# app = Flask(__name__, static_folder='../client/svelte/public')

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/api/getFoods', methods=['GET'])
def getFoods():
    # read csv file
    with open('foods.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows = list(reader)

        # get random food
        random_rows = random.sample(rows, 2)
        print(random_rows)
        return jsonify({'food1': {'name': random_rows[0][0], 'elo': random_rows[0][1]}, 'food2': {'name': random_rows[1][0], 'elo': random_rows[1][1]}})
    
@app.route('/api/updateFoods', methods=['POST'])
def updateFoods():
    data = request.get_json()
    winner = data.get('winner')
    loser = data.get('loser')
    #get old elo from csv
    winnerElo = 0
    loserElo = 0
    winnerIDx = 0
    loserIDx = 0
    rows = []
    with open('foods.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        rows = list(reader)
    for row in rows:
        if row[0] == winner:
            winnerElo = int(row[1])
            winnerIDx = rows.index(row)
        if row[0] == loser:
            loserElo = int(row[1])
            loserIDx = rows.index(row)
    #calculate new elo
    K = 30
    d = 1
    print(winnerElo, loserElo)
    winnerElo, loserElo = EloRating(winnerElo, loserElo, K, d)
    
    rows[winnerIDx][1] = winnerElo
    rows[loserIDx][1] = loserElo

    #update csv
    with open('foods.csv', 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(['name', 'elo'])
        write.writerows(rows)
        
    return jsonify({'success': True})

    


if __name__ == '__main__':
    app.run(debug=True)