from flask import Flask, render_template, request, redirect, jsonify, url_for
from models import db
from inventory import inventory_bp  # Only importing the blueprint now
from transactions import transactions_bp
from analytics import analytics_bp
from carbon import carbon_bp
from certification import certification_bp
from iot import iot_bp
from qr import qr_bp

import json
import os
import qrcode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farm2fork.db'
db.init_app(app)

DATA_DIR = 'data'

def load_data(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r') as file:
            return json.load(file)
    return []

def save_data(filename, data):
    with open(os.path.join(DATA_DIR, filename), 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/farmer', methods=['GET', 'POST'])
def farmer():
    if request.method == 'POST':
        entry = {
            "name": request.form['name'],
            "produce": request.form['produce'],
            "energy_used_kwh": float(request.form['energy']),
            "emissions_kgco2": round(float(request.form['energy']) * 0.4, 2)
        }
        data = load_data('farmers.json')
        data.append(entry)
        save_data('farmers.json', data)

        qr_data = f"Farmer: {entry['name']}, Produce: {entry['produce']}, Emissions: {entry['emissions_kgco2']} kg CO2"
        img = qrcode.make(qr_data)
        qr_path = os.path.join('static', 'qr.png')
        img.save(qr_path)

        return redirect('/farmer')

    qr_exists = os.path.exists(os.path.join('static', 'qr.png'))
    return render_template('farmer.html', qr_exists=qr_exists)

@app.route('/intermediary', methods=['GET', 'POST'])
def intermediary():
    if request.method == 'POST':
        entry = {
            "name": request.form['name'],
            "storage_energy_kwh": float(request.form['energy']),
            "transport_energy_kwh": float(request.form['transport']),
            "emissions_kgco2": round((float(request.form['energy']) + float(request.form['transport'])) * 0.5, 2)
        }
        data = load_data('intermediaries.json')
        data.append(entry)
        save_data('intermediaries.json', data)
        return redirect('/intermediary')
    return render_template('intermediary.html')

@app.route('/consumer')
def consumer():
    farmers = load_data('farmers.json')
    intermediaries = load_data('intermediaries.json')
    return render_template('consumer.html', farmers=farmers, intermediaries=intermediaries)

@app.route('/farmer_data')
def farmer_data():
    data = load_data('farmers.json')
    return jsonify(data)

# Register feature blueprints
app.register_blueprint(inventory_bp)
app.register_blueprint(transactions_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(carbon_bp, url_prefix='/carbon')
app.register_blueprint(certification_bp)
app.register_blueprint(iot_bp)
app.register_blueprint(qr_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
