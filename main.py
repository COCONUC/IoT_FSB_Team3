from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

tempValidator = 'temp > 0 and temp < 50'
humidValidator = 'humid >= 0 and humid < 80'

@app.route('/api/temp-fomular', methods=['GET'])
@cross_origin()
def getTempFormular():
    return jsonify({'result': tempValidator})

@app.route('/api/temp-fomular', methods=['POST'])
@cross_origin()
def setTempFormular():
    data = request.get_json()  # Get the JSON data from the request body
    if data is None or 'data' not in data:
        return jsonify({'error': 'Invalid request. JSON body with "data" key is required.'}), 400
    
    formular = data['data']
    # You can perform any processing you need with the message here
    global tempValidator
    tempValidator = formular
    
    return jsonify({'result': f'Formular updated: {formular}'}), 200

@app.route('/api/humid-fomular', methods=['GET'])
@cross_origin()
def getHumidFormular():
    return jsonify({'result': humidValidator})

@app.route('/api/humid-fomular', methods=['POST'])
@cross_origin()
def setHumidFormular():
    data = request.get_json()  # Get the JSON data from the request body
    if data is None or 'data' not in data:
        return jsonify({'error': 'Invalid request. JSON body with "data" key is required.'}), 400
    
    formular = data['data']
    # You can perform any processing you need with the message here
    global humidValidator
    humidValidator = formular
    
    return jsonify({'result': f'Formular updated: {formular}'}), 200

@app.route('/api/validate', methods=['GET'])
@cross_origin()
def validateTempAndHumid():
    # Get query parameters from the request
    temp = float(request.args.get('temp'))
    humid = float(request.args.get('humid'))

    isValidTemp = eval(tempValidator)
    isValidHumid = eval(humidValidator)

    # Return a JSON response
    return jsonify({'message': isValidHumid and isValidTemp}), 200

if __name__ == '__main__':
    app.run(debug=True)
