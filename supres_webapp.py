import sys
import subprocess
import os
from binance.client import Client
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import db_pandas
import pandas as pd

client = Client("", "")
app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def index():
    return render_template('hello.html')


@app.route('/deneme/')
def deneme():
    return render_template('deneme.html')


@app.route('/run_script/', methods=['POST'])
def run_script():
    ticker = request.form['ticker']
    time_frame = request.form['timeframe']
    subprocess.run(f"python ../binance-alarm/analyze_script.py {ticker.upper()} "
                   f"{time_frame.upper()}", cwd="../binance-alarm", shell=True)
    return redirect(url_for('index'))


@app.route('/alarm/', methods=['POST'])
def add_remove():
    ticker = request.form['ticker']
    alarm_price = request.form['alarm-price']
    if request.form['action'] == 'Add':
        db_pandas.add_alarm_data(ticker.upper(), float(alarm_price))
    elif request.form['action'] == 'Remove':
        db_pandas.remove_alarm_cell(ticker.upper(), float(alarm_price))
    return redirect(url_for('index'))




@app.route('/usage')
def usage():
    return 'Usage about bot'


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)