from flask import Blueprint, render_template, request

carbon_bp = Blueprint('carbon', __name__, url_prefix='/carbon')

@carbon_bp.route('/', methods=['GET', 'POST'])
def carbon_home():
    result = None
    if request.method == 'POST':
        try:
            mode = request.form['mode']
            distance = float(request.form['distance'])
            weight = float(request.form['weight'])

            # Emission factors in kg CO2 per ton-km (example values)
            emission_factors = {
                'truck': 0.1,
                'train': 0.04,
                'ship': 0.02,
                'air': 0.5
            }

            if mode in emission_factors:
                result = round(emission_factors[mode] * distance * (weight / 1000), 2)
        except Exception as e:
            result = f"Error in calculation: {str(e)}"

    return render_template('carbon.html', result=result)

# Additional emission factors (example values)
produce_emissions = {
    'vegetable': 0.3,  # kg CO2 per kg
    'meat': 27.0,
    'dairy': 13.0
}

farming_emissions = {
    'organic': 0.8,
    'conventional': 1.0,
    'greenhouse': 2.5
}

packaging_emissions = {
    'plastic': 0.2,  # kg CO2 per kg of packaging
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

            # CO2 equivalence examples
            car_km_eq = round(total_emission / 0.21, 2)  # 0.21 kg CO2/km for average car
            trees_needed = round(total_emission / 21.77, 2)  # 1 tree offsets ~21.77 kg CO2/year

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
