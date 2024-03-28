import os
from flask import Flask, config, render_template, request, session, flash, redirect, url_for
import numpy as np
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from utils import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    path = "static/mzmls"
    mzmls = os.listdir(path)
    lmzmls = []
    for f in mzmls:
        lmzmls.append({'name': f})

    path = "static/spls"
    spls = os.listdir(path)
    lspls = []
    for f in spls:
        lspls.append({'name': f})


    return render_template('data-explorer.html', mzmls=lmzmls, spls=lspls)

@app.route('/save2MGF', methods=['POST', 'GET'])
def save2MGF():
    dfdict, ms2dict = getTIC(f"static/mzmls/{session['mzxml']}")
    if request.method == 'POST':
        spectrum = ms2dict[float(request.form['idx'])]
        spectrum['file'] = request.form['file']
        spectrum['scan'] = request.form['scan']
        spectrum['gnps'] = request.form['gnps']
        spectrum['chw'] = request.form['chw']
        with open(f"static/dbs/{request.form['mgffile']}", 'a+') as f:
            f.write(get_mgf_string(spectrum))
    flash('You successfully saved the spectrum')
    return redirect(url_for('mapFilter', mzxml=session['mzxml'],
                            spl=session['spl']))

@app.route('/chromatogram')
def chromatogram():
    return pg(request.args.get('data'))

def pg(dictid=''):
    dfdict, ms2dict = getTIC(f"static/mzmls/{session['mzxml']}")
    spec = ms2dict[float(dictid)]
    chrData = pd.DataFrame(zip(*spec['peaks']), columns=['mz', 'int'])

    fig = px.bar(chrData, x='mz', y='int', title=f"m/z:{spec['parent']} rt:{spec['rt']}")
    fig.update_traces(width=1)
    chrGraph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return chrGraph


@app.route("/mapFilter" , methods=['GET', 'POST'])
def mapFilter():
    if request.method == 'POST':
        session['mzxml'] = mzxml = request.form.get('mzxml')
        session['spl'] = spl = request.form.get('spl')
    else:
        session['mzxml'] = mzxml = request.args.get('mzxml')
        session['spl'] = spl = request.args.get('spl')
    dfdict, ms2dict = getTIC(f'static/mzmls/{mzxml}')
    df = pd.DataFrame(dfdict)
    fig = px.line(df, x="rt", y="int", title=f'TIC')

    lst = pd.read_csv(f'static/spls/{spl}')
    pts = getPoints(df, lst)
    fig.add_trace(go.Scatter(x=pts['rt'], y=pts['int'], mode='markers'))
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('data-explorer.html',
                           graphJSON=graphJSON, mzxml='{'+'"mzxml":"'+mzxml+'"}')

if __name__=='__main__':
    app.run(debug=True)
