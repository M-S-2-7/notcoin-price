from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

def fetch_price():
    url = 'https://api.nobitex.ir/market/stats'
    
    data = {
        'srcCurrency': 'not',
        'dstCurrency': 'rls'
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an HTTPError on bad response
    except requests.RequestException as e:
        return f'Error fetching price: {e}'

    response_data = response.json()

    try:
        price = response_data['global']['binance']['not']
        return price
    except KeyError:
        return 'Error fetching price'

@app.route('/fetch_price', methods=['GET'])
def fetch_price_endpoint():
    return jsonify(fetch_price())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
