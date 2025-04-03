from flask import Blueprint, request, jsonify
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime

select_bp = Blueprint('select', __name__)

# Load the dataset
input_file = "01_2018_to_09_2018_Merged.csv"
df = pd.read_csv(input_file)

crop_list = df.columns[1:-1].tolist()  # Crop names (excluding date and price columns)
price_list = df["States/UTs"].unique().tolist()  # States (Price types)

# Cache for trained models (to avoid re-training on each request)
model_cache = {}

# Function to train and cache models for crops
def train_and_cache_models(selected_price):
    """Train SARIMAX models and cache them for later use."""
    filtered_df = df[df["States/UTs"] == selected_price]
    models = {}

    for selected_crop in crop_list:
        avg_df = filtered_df[["Date", selected_crop]].copy()
        avg_df.columns = ["Date", "Price"]
        
        avg_df['Date'] = pd.to_datetime(avg_df['Date'], dayfirst=True)
        avg_df.set_index('Date', inplace=True)
        avg_df = avg_df.sort_index()
        avg_df = avg_df.asfreq('D')

        # Prepare training data
        train_data = avg_df.loc['2018-01-01':'2018-06-30', "Price"]

        # SARIMAX model for time series forecasting
        model = SARIMAX(train_data, order=(5, 1, 0), seasonal_order=(1, 1, 1, 7))
        model_fit = model.fit(disp=True)
        
        # Cache the trained model
        models[selected_crop] = model_fit

    model_cache[selected_price] = models

# Function to generate predictions for all crops based on a specific date and price type
def generate_predictions_for_date(selected_price, selected_date):
    """Generates predictions for all crops based on a specific date and price type."""
    if selected_price not in model_cache:
        # If no cached models, train and cache the models for the selected price type
        train_and_cache_models(selected_price)

    models = model_cache[selected_price]
    
    predicted_prices = {}

    for selected_crop, model_fit in models.items():
        # Forecast the price for the selected date
        # The model is trained until June 30th, and we want the forecast for a specific date
        forecast_steps = (selected_date - datetime(2018, 6, 30).date()).days  # Number of days from June 30th to selected_date
        
        if forecast_steps <= 0:
            return jsonify({"error": "Selected date must be after June 30th, 2018."}), 400
        
        prediction = model_fit.forecast(steps=forecast_steps).iloc[-1]  # Get forecast for the selected date
        
        predicted_prices[selected_crop] = prediction

    return predicted_prices

# Route to get available price types (states) and available dates (from 1st July to 30th Sept 2018)
@select_bp.route('/select-options', methods=['GET'])
def select_options():
    """Returns available price types (states) and available dates."""
    if not crop_list or not price_list:
        return jsonify({"error": "No available data"}), 400

    # Define the available date range (from July 1st to Sept 30th, 2018)
    available_dates = pd.date_range(start="2018-07-01", end="2018-09-30", freq='D').strftime('%Y-%m-%d').tolist()

    return jsonify({
        "price_types": price_list,  # List of states (price types)
        "available_dates": available_dates  # Date range from 1st July to 30th September 2018
    })

# Route to generate and return predicted prices for all crops for a specific date and price type (state)
@select_bp.route('/predicted-piechart', methods=['GET'])
def predicted_piechart():
    """Generates predicted data for a specific date and price type, returning it as pie chart data."""
    selected_price = request.args.get("state")
    selected_date = request.args.get("date")

    if selected_price not in price_list:
        return jsonify({"error": "Invalid price type"}), 400

    # Convert selected_date to datetime for validation
    try:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Generate predictions for all crops for the selected date and price type
    predicted_prices = generate_predictions_for_date(selected_price, selected_date)

    # Prepare pie chart data: for each crop, get the predicted price
    pie_chart_data = {
        "labels": list(predicted_prices.keys()),  # Crop names as labels
        "values": list(predicted_prices.values())  # Predicted prices as values
    }

    return jsonify(pie_chart_data)

@select_bp.route('/predicted-prices-first-6-crops', methods=['GET'])
def predicted_prices_first_6_crops():
    """Generates predicted prices for the first 6 crops based on selected price type and date."""
    selected_price = request.args.get("state")
    selected_date = request.args.get("date")

    if selected_price not in price_list:
        return jsonify({"error": "Invalid price type"}), 400

    # Convert selected_date to datetime for validation
    try:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Generate predictions for all crops for the selected date and price type
    predicted_prices = generate_predictions_for_date(selected_price, selected_date)

    # Prepare data for the first 6 crops using actual crop names
    first_6_crops = {crop: predicted_prices[crop] for crop in crop_list[:6]}

    return jsonify(first_6_crops)
