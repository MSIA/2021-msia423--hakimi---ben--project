from flask import Flask
import traceback
from flask import request, render_template, redirect, url_for
import pickle
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, confusion_matrix, accuracy_score

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

@app.route('/', methods = ['GET', 'POST'])
def home_page():
    if request.method == 'GET':
        with open('models/model.pkl', 'rb') as f:
            rf = pickle.load(f)

        colnames = ['homeSpread',
                            'ArizonaV',
                            'AtlantaV',
                            'BaltimoreV',
                            'BuffaloV',
                            'CarolinaV',
                            'ChicagoV',
                            'CincinnatiV',
                            'ClevelandV',
                            'DallasV',
                            'DenverV',
                            'DetroitV',
                            'GreenBayV',
                            'HoustonV',
                            'IndianapolisV',
                            'JacksonvilleV',
                            'KansasCityV',
                            'LAChargersV',
                            'LARamsV',
                            'LVRaidersV',
                            'MiamiV',
                            'MinnesotaV',
                            'NYGiantsV',
                            'NYJetsV',
                            'NewEnglandV',
                            'NewOrleansV',
                            'PhiladelphiaV',
                            'PittsburghV',
                            'SanFranciscoV',
                            'SeattleV',
                            'TampaBayV',
                            'TennesseeV',
                            'WashingtonV',
                            'Arizona',
                            'Atlanta',
                            'Baltimore',
                            'Buffalo',
                            'Carolina',
                            'Chicago',
                            'Cincinnati',
                            'Cleveland',
                            'Dallas',
                            'Denver',
                            'Detroit',
                            'GreenBay',
                            'Houston',
                            'Indianapolis',
                            'Jacksonville',
                            'KansasCity',
                            'LAChargers',
                            'LARams',
                            'LVRaiders',
                            'Miami',
                            'Minnesota',
                            'NYGiants',
                            'NYJets',
                            'NewEngland',
                            'NewOrleans',
                            'Philadelphia',
                            'Pittsburgh',
                            'SanFrancisco',
                            'Seattle',
                            'TampaBay',
                            'Tennessee',
                            'Washington']
        inputs = [7,    0,    0,    0,    0,    0,    0,    0,    0,
           0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
           0,    0,    0,    0,    0,    0,    0,    0,    0,    1,    0,
           0,    0,    1,    0,    0,    0,    0,    0,    0,    0,    0,
           0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
           0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,
           0]

        testdata = pd.DataFrame([inputs],columns = colnames)

        x = rf.predict(testdata)[0]
        if x == 0:
            return "Away team covered"
        elif x == 1:
            return "Home team covered"

        #return render_template('index.html')
    if request.method == 'POST':
        url_for_post = url_for('addThem', num1=request.form['spread'])
        return redirect(url_for_post)

@app.route('/add_nums', methods = ['GET', 'POST'])
def addThem():
    return f'{1+1}'

if __name__ == '__main__':
    app.run()