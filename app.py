from flask import Flask, jsonify, request
from flask_cors import CORS
import ee

app = Flask(__name__)
CORS(app)

# Initialize Earth Engine with project ID
ee.Initialize(project='chat-426009')  # Added your project ID here

@app.route('/ndvi', methods=['GET'])
def get_ndvi():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    
    point = ee.Geometry.Point(lon, lat)
    
    image = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
        .filterDate('2023-01-01', '2023-01-31') \
        .filterBounds(point) \
        .first()
    
    ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
    sample = ndvi.sample(point, 30).first().get('NDVI')
    
    return jsonify({
        'latitude': lat,
        'longitude': lon,
        'ndvi': sample.getInfo()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)