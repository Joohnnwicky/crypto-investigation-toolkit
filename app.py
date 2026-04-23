"""Flask application entry point for Crypto Investigation Toolkit"""

from flask import Flask, render_template
from modules.tron.routes import tron_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(tron_bp)


@app.route('/')
def index():
    """Homepage with tool overview and categories"""
    return render_template('index.html')


@app.route('/tron/suspicious-analyzer')
def tron_suspicious_analyzer():
    """TRON suspicious feature analysis tool page"""
    return render_template('tron/suspicious_analyzer.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)