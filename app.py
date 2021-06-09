import string
import random
import logging
import logging.config

from flask import Flask
from flask import request, render_template, redirect, url_for
import pickle
import pandas as pd

from src.createDB import inputGames
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

app.config.from_pyfile('config/flaskconfig.py')

## DOWNLOAD FROM S3

@app.route('/', methods = ['GET', 'POST'])
def home_page():
    if request.method == 'GET':
        try:
            logger.info("Home page was accessed")
            return render_template('index.html')
        except:
            logger.error("Error occured when trying to access home page")
            return render_template('fullError.html')

    if request.method == 'POST':
        homeTeam = request.form['homeT']
        awayTeam = request.form['awayT']
        spread = request.form['pickSpread']
        url_for_post = url_for('addThem', homeTeam=homeTeam, awayTeam=awayTeam, spread=spread)
        try:
            logger.info("Successful push from home page with homeTeam = %s, awayTeam = %s and spread = %s", homeTeam, awayTeam, spread)
            return redirect(url_for_post)
        except:
            logger.error("Unable to push from home page with homeTeam = %s, awayTeam = %s and spread = %s", homeTeam, awayTeam, spread)
            return render_template('fullError.html')

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
        try:
            spreadNum = float(spread)
        except:
            logger.warning("Spread was input as '%s' and could not be converted to float", spread)
            return render_template('error.html')
        testdata['homeSpread']=spreadNum
        if homeTeam == "Arizona":
            testdata['Arizona']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/crd.png'
        elif homeTeam == "Atlanta":
            testdata['Atlanta']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/atl.png'
        elif homeTeam == "Baltimore":
            testdata['Baltimore']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/rav.png'
        elif homeTeam == "Buffalo":
            testdata['Buffalo']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/buf.png'
        elif homeTeam == "Carolina":
            testdata['Carolina']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/car.png'
        elif homeTeam == "Chicago":
            testdata['Chicago']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/chi.png'
        elif homeTeam == "Cincinnati":
            testdata['Cincinnati']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/cin.png'
        elif homeTeam == "Cleveland":
            testdata['Cleveland']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/cle.png'
        elif homeTeam == "Dallas":
            testdata['Dallas']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/dal.png'
        elif homeTeam == "Denver":
            testdata['Denver']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/den.png'
        elif homeTeam == "Detroit":
            testdata['Detroit']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/det.png'
        elif homeTeam == "GreenBay":
            testdata['GreenBay']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/gnb.png'
        elif homeTeam == "Houston":
            testdata['Houston']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/htx.png'
        elif homeTeam == "Indianapolis":
            testdata['Indianapolis']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/clt.png'
        elif homeTeam == "Jacksonville":
            testdata['Jacksonville']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/jax.png'
        elif homeTeam == "KansasCity":
            testdata['KansasCity']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/kan.png'
        elif homeTeam == "LasVegas":
            testdata['LVRaiders']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/rai.png'
        elif homeTeam == "LosAngelesChargers":
            testdata['LAChargers']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/sdg.png'
        elif homeTeam == "LosAngelesRams":
            testdata['LARams']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/ram.png'
        elif homeTeam == "Miami":
            testdata['Miami']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/mia.png'
        elif homeTeam == "Minnesota":
            testdata['Minnesota']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/min.png'
        elif homeTeam == "NewEngland":
            testdata['NewEngland']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/nwe.png'
        elif homeTeam == "NewOrleans":
            testdata['NewOrleans']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/nor.png'
        elif homeTeam == "NewYorkGiants":
            testdata['NYGiants']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/nyg.png'
        elif homeTeam == "NewYorkJets":
            testdata['NYJets']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/nyj.png'
        elif homeTeam == "Philadelphia":
            testdata['Philadelphia']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/phi.png'
        elif homeTeam == "Pittsburgh":
            testdata['Pittsburgh']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/pit.png'
        elif homeTeam == "SanFrancisco":
            testdata['SanFrancisco']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/sfo.png'
        elif homeTeam == "Seattle":
            testdata['Seattle']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/sea.png'
        elif homeTeam == "TampaBay":
            testdata['TampaBay']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/tam.png'
        elif homeTeam == "Tennessee":
            testdata['Tennessee']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/oti.png'
        elif homeTeam == "Washington":
            testdata['Washington']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/was.png'

        if awayTeam == "Arizona":
            testdata['ArizonaV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/crd.png'
        elif awayTeam == "Atlanta":
            testdata['AtlantaV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/atl.png'
        elif awayTeam == "Baltimore":
            testdata['BaltimoreV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/rav.png'
        elif awayTeam == "Buffalo":
            testdata['BuffaloV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/buf.png'
        elif awayTeam == "Carolina":
            testdata['CarolinaV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/car.png'
        elif awayTeam == "Chicago":
            testdata['ChicagoV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/chi.png'
        elif awayTeam == "Cincinnati":
            testdata['CincinnatiV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/cin.png'
        elif awayTeam == "Cleveland":
            testdata['ClevelandV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/cle.png'
        elif awayTeam == "Dallas":
            testdata['DallasV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/dal.png'
        elif awayTeam == "Denver":
            testdata['DenverV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/den.png'
        elif awayTeam == "Detroit":
            testdata['DetroitV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/det.png'
        elif awayTeam == "GreenBay":
            testdata['GreenBayV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/gnb.png'
        elif awayTeam == "Houston":
            testdata['HoustonV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/htx.png'
        elif awayTeam == "Indianapolis":
            testdata['IndianapolisV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/clt.png'
        elif awayTeam == "Jacksonville":
            testdata['JacksonvilleV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/jax.png'
        elif awayTeam == "KansasCity":
            testdata['KansasCityV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/kan.png'
        elif awayTeam == "LasVegas":
            testdata['LVRaidersV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/rai.png'
        elif awayTeam == "LosAngelesChargers":
            testdata['LAChargersV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/sdg.png'
        elif awayTeam == "LosAngelesRams":
            testdata['LARamsV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/ram.png'
        elif awayTeam == "Miami":
            testdata['MiamiV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/mia.png'
        elif awayTeam == "Minnesota":
            testdata['MinnesotaV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/min.png'
        elif awayTeam == "NewEngland":
            testdata['NewEnglandV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/nwe.png'
        elif awayTeam == "NewOrleans":
            testdata['NewOrleansV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/nor.png'
        elif awayTeam == "NewYorkGiants":
            testdata['NYGiantsV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/nyg.png'
        elif awayTeam == "NewYorkJets":
            testdata['NYJetsV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/nyj.png'
        elif awayTeam == "Philadelphia":
            testdata['PhiladelphiaV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/phi.png'
        elif awayTeam == "Pittsburgh":
            testdata['PittsburghV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/pit.png'
        elif awayTeam == "SanFrancisco":
            testdata['SanFranciscoV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/sfo.png'
        elif awayTeam == "Seattle":
            testdata['SeattleV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/sea.png'
        elif awayTeam == "TampaBay":
            testdata['TampaBayV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/tam.png'
        elif awayTeam == "Tennessee":
            testdata['TennesseeV']=1
            roadimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/oti.png'
        elif awayTeam == "Washington":
            testdata['WashingtonV']=1
            homeimg = 'https://d2p3bygnnzw9w3.cloudfront.net/req/202105061/tlogo/pfr/was.png'

        pred = rf.predict(testdata)[0]

        def id_generator(size, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))

        randKey = id_generator(20)

        #ig = inputGames(engine_string='sqlite:///data/msia423_db.db')
        ig = inputGames(engine_string=SQLALCHEMY_DATABASE_URI)

        try:
            if homeTeam == "home":
                logger.info("Instructions/description page was accessed")
                return render_template('info.html')
            elif homeTeam == awayTeam:
                logger.warning("Input was given to prediction page with %s as home AND away team", homeTeam)
                return render_template('sameTeam.html')
            elif int(pred) == 0:
                ig.add_game(game_id=randKey, home_team=homeTeam, away_team=awayTeam, spread=spreadNum, home_cover=int(pred))
                logger.info("Prediction succesfully made where away team covers")
                return render_template('awayCover.html', homeTeam=homeTeam, awayTeam=awayTeam, spread=spread, roadimg=roadimg)
            elif int(pred) == 1:
                ig.add_game(game_id=randKey, home_team=homeTeam, away_team=awayTeam, spread=spreadNum, home_cover=int(pred))
                logger.info("Prediction succesfully made where home team covers")
                return render_template('homeCover.html', homeTeam=homeTeam, awayTeam=awayTeam, spread=spread, homeimg=homeimg)
        except:
            logger.error("An error occured when trying to make a prediction")
            return render_template('fullError.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
