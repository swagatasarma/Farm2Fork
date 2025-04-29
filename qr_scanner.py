
from flask import Blueprint, render_template

qr_bp = Blueprint('qr_scanner', __name__)

@qr_bp.route('/qr_scanner')
def qr_scanner():
    return render_template('qr_scanner.html')
