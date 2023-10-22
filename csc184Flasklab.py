from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

data = pd.read_csv('AAPL.csv', parse_dates=['Date'], index_col='Date')

@app.route('/')
def home():
    return jsonify("CSC184 Lab 2: Jancarlos Rodriguez") 

@app.route('/getData', methods=['GET'])
def get_data():
    return data.to_json(date_format='iso', orient='records')

@app.route('/getData/<string:date>', methods=['GET'])
def get_data_date(date):
    try:
        date_data = data.loc[pd.to_datetime(date)]
        return date_data.to_json(date_format='iso')
    except KeyError:
        return jsonify(error='Date not found'), 404

@app.route('/calculate10DayAverage/<string:date>', methods=['GET'])
def calculate_10_day_average(date):
    try:
        end_date = pd.to_datetime(date)
        start_date = end_date - pd.DateOffset(days=10)
        data_range = data.loc[start_date:end_date]
        last_10_days_avg = data_range['Close'].mean()
        return jsonify({"10_day_avg_close": last_10_days_avg})
    except KeyError:
        return jsonify(error='Date not found'), 404
    

@app.route('/getData', methods=['POST'])
def get_data_range():
    start_date = request.json['start_date']
    end_date = request.json['end_date']
    date_range_data = data.loc[start_date:end_date]
    return date_range_data.to_json(date_format='iso', orient='records')

@app.route('/addData', methods=['POST'])
def add_data():
    new_data = request.json
    data.loc[pd.to_datetime(new_data['Date'])] = new_data.values()
    return jsonify(success=True)

@app.route('/updateData', methods=['PUT'])
def update_data():
    update_data = request.json
    date = pd.to_datetime(update_data['Date'])
    data.loc[date] = update_data.values()
    return jsonify(success=True)

@app.route('/deleteDate/<string:date>', methods=['DELETE'])
def delete_date(date):
    data.drop(pd.to_datetime(date), inplace=True)
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)
