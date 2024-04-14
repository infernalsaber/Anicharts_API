from flask import Flask, jsonify, request, Response
import requests
import json

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Welcome to the Anicharts API, this is meant give you the (close to) latest updated Anitrendz/AnimeCorner chart images. Use /docs to explore the API.'

@app.route('/docs')
def documentation():
    return 'WIP'

@app.route('/charts')
def get_charts():
    with open("anime_images.json", "r") as f:
        data = json.load(f)
    
    return jsonify(data[max(data.keys())])

@app.route('/history')
def get_historical_data():
    with open("anime_images.json", "r") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)