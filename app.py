from flask import Flask
from flask_cors import CORS
from graphs import graphs_bp  # Import Blueprint
from sarima import sarima_bp  # Import Blueprint
from piechart import pie_chart_bp
from commodities import commodities_bp
from plot import plot_bp
from select_1 import select_bp
from forecast import price_forecast_bp

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(graphs_bp, url_prefix="/graphs")
app.register_blueprint(sarima_bp, url_prefix="/sarima")
app.register_blueprint(pie_chart_bp, url_prefix="/pie_chart")
app.register_blueprint(commodities_bp, url_prefix="/commodities")
app.register_blueprint(plot_bp, url_prefix="/plot")
app.register_blueprint(select_bp, url_prefix="/select")
app.register_blueprint(price_forecast_bp, url_prefix="/price_forecast")

if __name__ == "__main__":
    app.run(debug=True)
