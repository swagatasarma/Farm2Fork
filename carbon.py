
from flask import Blueprint, render_template, request

carbon_bp = Blueprint('carbon', __name__, template_folder='templates')

# Original emission factors
emission_factors = {
    'truck': 0.12,
    'train': 0.04,
    'ship': 0.015,
    'air': 0.5
}

@carbon_bp.route('/', methods=['GET', 'POST'])
def carbon():
    result = None
    if request.method == 'POST':
        try:
            mode = request.form['mode']
            distance = float(request.form['distance'])
            weight = float(request.form['weight'])
            emission = emission_factors.get(mode, 0) * distance * (weight / 1000)
            
            result = round(emission, 2)
            from datetime import datetime
            import json
            import os

            log_path = os.path.join(os.path.dirname(__file__), 'data', 'emissions.json')
            entry = {
                "date": datetime.today().strftime('%Y-%m-%d'),
                "mode": mode,
                "emission": result
            }
            if os.path.exists(log_path):
                with open(log_path, 'r+') as f:
                    data = json.load(f)
                    data.append(entry)
                    f.seek(0)
                    json.dump(data, f, indent=2)
            else:
                with open(log_path, 'w') as f:
                    json.dump([entry], f, indent=2)
    
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template('carbon.html', result=result)

# Additional emission factors
produce_emissions = {
    'vegetable': 0.3,
    'meat': 27.0,
    'dairy': 13.0
}

farming_emissions = {
    'organic': 0.8,
    'conventional': 1.0,
    'greenhouse': 2.5
}

packaging_emissions = {
    'plastic': 0.2,
    'biodegradable': 0.05,
    'none': 0.0
}

@carbon_bp.route('/advanced', methods=['GET', 'POST'])
def carbon_advanced():
    result = None
    breakdown = {}
    if request.method == 'POST':
        try:
            mode = request.form['mode']
            distance = float(request.form['distance'])
            weight = float(request.form['weight'])

            produce_type = request.form['produce_type']
            farming_method = request.form['farming_method']
            packaging = request.form['packaging']

            transport_emission = round(emission_factors.get(mode, 0) * distance * (weight / 1000), 2)
            production_emission = round(produce_emissions.get(produce_type, 0) * weight * farming_emissions.get(farming_method, 1), 2)
            packaging_emission = round(packaging_emissions.get(packaging, 0) * weight, 2)

            total_emission = round(transport_emission + production_emission + packaging_emission, 2)
            car_km_eq = round(total_emission / 0.21, 2)
            trees_needed = round(total_emission / 21.77, 2)

            breakdown = {
                'transport_emission': transport_emission,
                'production_emission': production_emission,
                'packaging_emission': packaging_emission,
                'total_emission': total_emission,
                'car_km_eq': car_km_eq,
                'trees_needed': trees_needed
            }
        except Exception as e:
            result = f"Error in advanced calculation: {str(e)}"

    return render_template('carbon_advanced.html', result=result, breakdown=breakdown)
