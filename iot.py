from flask import Blueprint, render_template

iot_bp = Blueprint('iot', __name__, url_prefix='/iot_simulation')

@iot_bp.route('/')
def iot_home():
    return render_template('iot_simulation.html')
