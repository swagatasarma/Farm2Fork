from flask import Blueprint, render_template

certification_bp = Blueprint('certification', __name__, url_prefix='/certification')

@certification_bp.route('/')
def certification_home():
    return render_template('certification.html')
