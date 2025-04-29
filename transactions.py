
from flask import Blueprint, render_template, request, jsonify

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

# Mock transactions data
transactions_data = [
    {'buyer': 'Alice', 'seller': 'Bob', 'product': 'Tomatoes', 'quantity': 50},
    {'buyer': 'Charlie', 'seller': 'Dave', 'product': 'Potatoes', 'quantity': 30}
]

@transactions_bp.route('/')
def transactions_home():
    return render_template('transactions.html', transactions=transactions_data)

@transactions_bp.route('/api', methods=['GET'])
def get_transactions():
    return jsonify(transactions_data)

@transactions_bp.route('/api', methods=['POST'])
def add_transaction():
    new_txn = request.json
    transactions_data.append(new_txn)
    return jsonify({'status': 'success', 'message': 'Transaction added'}), 201
