from flask import render_template, make_response, current_app, request
from . import main_bp


@main_bp.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')