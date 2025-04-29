from flask import Blueprint, render_template, request, jsonify

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

# Mock inventory data
inventory_data = [
    {'item': 'Tomatoes', 'quantity': 120, 'unit': 'kg'},
    {'item': 'Potatoes', 'quantity': 80, 'unit': 'kg'}
]

@inventory_bp.route('/')
def inventory_home():
    return render_template('inventory.html', inventory=inventory_data)

@inventory_bp.route('/api', methods=['GET'])
def get_inventory():
    return jsonify(inventory_data)

@inventory_bp.route('/api', methods=['POST'])
def update_inventory():
    new_item = request.json
    inventory_data.append(new_item)
    return jsonify({'status': 'success', 'message': 'Item added'}), 201
