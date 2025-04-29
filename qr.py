from flask import Blueprint, render_template

qr_bp = Blueprint('qr', __name__, url_prefix='/qr_scanner')

@qr_bp.route('/')
def qr_home():
    return render_template('qr_scanner.html')
