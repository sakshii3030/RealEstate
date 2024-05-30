from flask import Flask, request, jsonify
import util
from waitress import serve  # Import serve from Waitress

app = Flask(__name__)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    if request.method == 'POST':
        try:
            total_sqft = float(request.form['total_sqft'])
            location = request.form['location']
            bhk = int(request.form['bhk'])
            bath = int(request.form['bath'])

            estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

            response = jsonify({
                'estimated_price': estimated_price
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except Exception as e:
            response = jsonify({
                'error': str(e)
            })
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
    elif request.method == 'GET':
        # Handle GET request if needed
        pass




if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    serve(app, host='0.0.0.0', port=5000)
    app.run()