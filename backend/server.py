from flask import Flask, request, jsonify
import utils

app = Flask(__name__)

@app.route('/classify-image', methods=['GET', 'POST'])
def classifyImage():
    image = request.form['image_data']
    response = jsonify(utils.classifier(image))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    utils.loadSavedData()
    app.run(port=5000)