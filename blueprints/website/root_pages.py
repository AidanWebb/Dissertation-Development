from flask import render_template

from . import website


@website.route('/')
def home():
    """
    Returns the homepage for UH VPN.
    """
    return render_template('index.html')

