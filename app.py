"""Flask application entry point for Crypto Investigation Toolkit"""

from flask import Flask, render_template
from modules.tron.routes import tron_bp
from modules.eth.routes import eth_bp
from modules.trace.routes import trace_bp
from modules.cross.routes import cross_bp
from modules.case.routes import case_bp
from modules.docs.routes import docs_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(tron_bp)
app.register_blueprint(eth_bp)
app.register_blueprint(trace_bp)
app.register_blueprint(cross_bp)
app.register_blueprint(case_bp)
app.register_blueprint(docs_bp)


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