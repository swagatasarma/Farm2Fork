
from flask import Blueprint, render_template, jsonify
import random

iot_bp = Blueprint('iot_simulation', __name__)

@iot_bp.route('/iot_simulation')
def iot_page():
    return render_template('iot_simulation.html')

@iot_bp.route('/iot_data')
def iot_data():
    data = {
        'temperature': round(random.uniform(15.0, 35.0), 2),
        'humidity': round(random.uniform(30.0, 90.0), 2),
        'soil_moisture': round(random.uniform(200, 800), 2)
    }
    return jsonify(data)
