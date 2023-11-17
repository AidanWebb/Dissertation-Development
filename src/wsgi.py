from flask import Flask
from waitress import serve
import os

import processing.middleware as middleware
from blueprints.api import api
from blueprints.error_handlers import error_handlers
from blueprints.website import website
from processing import filters

# Define the Flask app and register blueprints
app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']
# Add blueprints
app.register_blueprint(website)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(error_handlers)

# Define auth and middleware
app.before_request(middleware.before_request)
app.after_request(middleware.apply_content_version)

# Serve the app via waitress
if __name__ == '__main__':
    serve(app)