import string
import random
from flask import Flask
from flask import request, render_template, redirect, url_for
import pickle
import pandas as pd
from src.createDB import inputGames

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

app.config.from_pyfile('config/flaskconfig.py')

@app.route('/', methods = ['GET', 'POST'])
def home_page():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        homeTeam = request.form['homeT']
        awayTeam = request.form['awayT']
        spread = request.form['pickSpread']
        url_for_post = url_for('addThem', homeTeam=homeTeam, awayTeam=awayTeam, spread=spread)
        return redirect(url_for_post)

@app.route('/prediction/<homeTeam>/<awayTeam>/<spread>', methods = ['GET', 'POST'])
def addThem(homeTeam, awayTeam, spread):
    if request.method == 'GET': 
        with open('models/model.pkl', 'rb') as f:
            rf = pickle.load(f)

        colnames = ['homeSpread','ArizonaV','AtlantaV','BaltimoreV','BuffaloV','CarolinaV','ChicagoV','CincinnatiV','ClevelandV',
                            'DallasV','DenverV','DetroitV','GreenBayV','HoustonV','IndianapolisV','JacksonvilleV','KansasCityV',
                            'LAChargersV','LARamsV','LVRaidersV','MiamiV','MinnesotaV','NYGiantsV','NYJetsV','NewEnglandV',
                            'NewOrleansV','PhiladelphiaV','PittsburghV','SanFranciscoV','SeattleV','TampaBayV','TennesseeV',
                            'WashingtonV','Arizona','Atlanta','Baltimore','Buffalo','Carolina','Chicago','Cincinnati',
                            'Cleveland','Dallas','Denver','Detroit','GreenBay','Houston','Indianapolis','Jacksonville',
                            'KansasCity','LAChargers','LARams','LVRaiders','Miami','Minnesota','NYGiants','NYJets',
                            'NewEngland','NewOrleans','Philadelphia','Pittsburgh','SanFrancisco','Seattle','TampaBay',
                            'Tennessee','Washington']
        inputs = [0,    0,    0,    0,    0,    0,    0,    0,    0,
           0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
           0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
           0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
           0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
           0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
           0]


        testdata = pd.DataFrame([inputs],columns = colnames)
        spreadNum = float(spread)
        testdata['homeSpread']=spreadNum
        if homeTeam == "Arizona":
            testdata['Arizona']=1
        elif homeTeam == "Atlanta":
            testdata['Atlanta']=1
        elif homeTeam == "Baltimore":
            testdata['Baltimore']=1
        elif homeTeam == "Buffalo":
            testdata['Buffalo']=1
        elif homeTeam == "Carolina":
            testdata['Carolina']=1
        elif homeTeam == "Chicago":
            testdata['Chicago']=1
        elif homeTeam == "Cincinnati":
            testdata['Cincinnati']=1
        elif homeTeam == "Cleveland":
            testdata['Cleveland']=1
        elif homeTeam == "Dallas":
            testdata['Dallas']=1
        elif homeTeam == "Denver":
            testdata['Denver']=1
        elif homeTeam == "Detroit":
            testdata['Detroit']=1
        elif homeTeam == "GreenBay":
            testdata['GreenBay']=1
        elif homeTeam == "Houston":
            testdata['Houston']=1
        elif homeTeam == "Indianapolis":
            testdata['Indianapolis']=1
        elif homeTeam == "Jacksonville":
            testdata['Jacksonville']=1
        elif homeTeam == "KansasCity":
            testdata['KansasCity']=1
        elif homeTeam == "LasVegas":
            testdata['LVRaiders']=1
        elif homeTeam == "LosAngelesChargers":
            testdata['LAChargers']=1
        elif homeTeam == "LosAngelesRams":
            testdata['LARams']=1
        elif homeTeam == "Miami":
            testdata['Miami']=1
        elif homeTeam == "Minnesota":
            testdata['Minnesota']=1
        elif homeTeam == "NewEngland":
            testdata['NewEngland']=1
        elif homeTeam == "NewOrleans":
            testdata['NewOrleans']=1
        elif homeTeam == "NewYorkGiants":
            testdata['NYGiants']=1
        elif homeTeam == "NewYorkJets":
            testdata['NYJets']=1
        elif homeTeam == "Philadelphia":
            testdata['Philadelphia']=1
        elif homeTeam == "Pittsburgh":
            testdata['Pittsburgh']=1
        elif homeTeam == "SanFrancisco":
            testdata['SanFrancisco']=1
        elif homeTeam == "Seattle":
            testdata['Seattle']=1
        elif homeTeam == "TampaBay":
            testdata['TampaBay']=1
        elif homeTeam == "Tennessee":
            testdata['Tennessee']=1
        elif homeTeam == "Washington":
            testdata['Washington']=1

        if awayTeam == "Arizona":
            testdata['ArizonaV']=1
        elif awayTeam == "Atlanta":
            testdata['AtlantaV']=1
        elif awayTeam == "Baltimore":
            testdata['BaltimoreV']=1
        elif awayTeam == "Buffalo":
            testdata['BuffaloV']=1
        elif awayTeam == "Carolina":
            testdata['CarolinaV']=1
        elif awayTeam == "Chicago":
            testdata['ChicagoV']=1
        elif awayTeam == "Cincinnati":
            testdata['CincinnatiV']=1
        elif awayTeam == "Cleveland":
            testdata['ClevelandV']=1
        elif awayTeam == "Dallas":
            testdata['DallasV']=1
        elif awayTeam == "Denver":
            testdata['DenverV']=1
        elif awayTeam == "Detroit":
            testdata['DetroitV']=1
        elif awayTeam == "GreenBay":
            testdata['GreenBayV']=1
        elif awayTeam == "Houston":
            testdata['HoustonV']=1
        elif awayTeam == "Indianapolis":
            testdata['IndianapolisV']=1
        elif awayTeam == "Jacksonville":
            testdata['JacksonvilleV']=1
        elif awayTeam == "KansasCity":
            testdata['KansasCityV']=1
        elif awayTeam == "LasVegas":
            testdata['LVRaidersV']=1
        elif awayTeam == "LosAngelesChargers":
            testdata['LAChargersV']=1
        elif awayTeam == "LosAngelesRams":
            testdata['LARamsV']=1
        elif awayTeam == "Miami":
            testdata['MiamiV']=1
        elif awayTeam == "Minnesota":
            testdata['MinnesotaV']=1
        elif awayTeam == "NewEngland":
            testdata['NewEnglandV']=1
        elif awayTeam == "NewOrleans":
            testdata['NewOrleansV']=1
        elif awayTeam == "NewYorkGiants":
            testdata['NYGiantsV']=1
        elif awayTeam == "NewYorkJets":
            testdata['NYJetsV']=1
        elif awayTeam == "Philadelphia":
            testdata['PhiladelphiaV']=1
        elif awayTeam == "Pittsburgh":
            testdata['PittsburghV']=1
        elif awayTeam == "SanFrancisco":
            testdata['SanFranciscoV']=1
        elif awayTeam == "Seattle":
            testdata['SeattleV']=1
        elif awayTeam == "TampaBay":
            testdata['TampaBayV']=1
        elif awayTeam == "Tennessee":
            testdata['TennesseeV']=1
        elif awayTeam == "Washington":
            testdata['WashingtonV']=1

        x = rf.predict(testdata)[0]

        def id_generator(size, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))


        randKey = id_generator(20)

        ig = inputGames(engine_string='sqlite:///data/msia423_db.db')
        #ig.add_game(game_id=randKey, home_team=homeTeam, away_team=awayTeam, spread=spreadNum)

        if homeTeam == "home":
            return render_template('info.html')
        elif homeTeam == awayTeam:
            return render_template('sameTeam.html')
        elif int(x) == 0:
            ig.add_game(game_id=randKey, home_team=homeTeam, away_team=awayTeam, spread=spreadNum, home_cover=int(x))
            return render_template('awayCover.html', awayTeam=awayTeam)
        elif int(x) == 1:
            ig.add_game(game_id=randKey, home_team=homeTeam, away_team=awayTeam, spread=spreadNum, home_cover=int(x))
            return render_template('homeCover.html', homeTeam=homeTeam)


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
    #app.run()