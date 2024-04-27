from flask import Flask, jsonify, Blueprint
from api.db import default_settings

app = Flask(__name__)

# Define a Blueprint for settings
settings_bp = Blueprint('settings', __name__)

class DefaultSettings:
    @staticmethod
    @settings_bp.route('/api/default-settings')
    def get_default_settings():
        return jsonify(default_settings.DEFAULT_SETTINGS)

# Register the Blueprint with the Flask app
app.register_blueprint(settings_bp)

if __name__ == '__main__':
    app.run(debug=True)
