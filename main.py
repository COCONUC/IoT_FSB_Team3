from flask import Flask, jsonify, request

app = Flask(__name__)

tempValidator = 'temp > 0 and temp < 50'
humidValidator = 'humid > 40 or humid < 80'

@app.route('/api/temp-fomular', methods=['GET'])
def getTempFormular():
    return jsonify({'result': tempValidator})

@app.route('/api/temp-fomular', methods=['POST'])
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
def getHumidFormular():
    return jsonify({'result': humidValidator})

@app.route('/api/humid-fomular', methods=['POST'])
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
def validateTempAndHumid():
    # Get query parameters from the request
    temp = int(request.args.get('temp'))
    humid = int(request.args.get('humid'))

    isValidTemp = eval(tempValidator)
    isValidHumid = eval(humidValidator)

    # Return a JSON response
    return jsonify({'message': isValidHumid and isValidTemp}), 200

if __name__ == '__main__':
    app.run(debug=True)
