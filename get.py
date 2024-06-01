from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

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
        return {'error': f'Error fetching price: {e}'}, 500

    response_data = response.json()

    try:
        price = response_data['global']['binance']['not']
        return {'price': price}, 200
    except KeyError:
        return {'error': 'Error fetching price'}, 500

@app.route('/fetch_price', methods=['GET'])
def fetch_price_endpoint():
    return jsonify(fetch_price())

if __name__ == '__main__':
    app.run()
