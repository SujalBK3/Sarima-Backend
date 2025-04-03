import matplotlib
matplotlib.use('Agg')  # Prevents GUI issues

from flask import Blueprint, request, jsonify
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

plot_bp = Blueprint('plot', __name__)

# Load dataset
input_file = "01_2018_to_09_2018_Merged.csv"
df = pd.read_csv(input_file)

crop_list = df.columns[1:-1].tolist()  # Crop names (price types)
price_list = df["States/UTs"].unique().tolist()  # States


# Function to generate predictions using SARIMA
def generate_predictions(selected_crop, selected_price):
    filtered_df = df[df["States/UTs"] == selected_price]
    avg_df = filtered_df[["Date", selected_crop]].copy()
    avg_df.columns = ["Date", "Price"]
    
    avg_df['Date'] = pd.to_datetime(avg_df['Date'], dayfirst=True)
    avg_df.set_index('Date', inplace=True)
    avg_df = avg_df.sort_index()
    avg_df = avg_df.asfreq('D')  # Set daily frequency

    train_data = avg_df.loc['2018-01-01':'2018-06-30', "Price"]
    test_data = avg_df.loc['2018-07-01':'2018-09-30', "Price"]
    pred_steps = len(test_data)

    model = SARIMAX(train_data, order=(5, 1, 0), seasonal_order=(1, 1, 1, 7))  # Adjusted seasonality
    model_fit = model.fit()
    predictions = model_fit.forecast(steps=pred_steps)

    # Convert predictions to a dictionary {date: predicted_price}
    predicted_prices = {date.strftime('%Y-%m-%d'): value for date, value in zip(test_data.index, predictions)}

    return test_data.index.strftime('%Y-%m-%d').tolist(), predicted_prices  # Test dates and predicted prices


# Route to return the available price types and crop types
@plot_bp.route('/select-options', methods=['GET'])
def select_options():
    """Returns available price types (states) and crop types."""
    if not crop_list or not price_list:
        return jsonify({"error": "No available data"}), 400

    return jsonify({
        "price_types": price_list,  # States list (Price types)
        "crop_types": crop_list     # Crop types
    })


# Route to return the predicted data for a selected crop and price type (state) as a pie chart
@plot_bp.route('/predicted-piechart', methods=['GET'])
def predicted_piechart():
    """Generates predicted data for a specific crop and price type and returns it as pie chart data for all test dates."""
    selected_crop = request.args.get("crop")
    selected_price = request.args.get("state")

    if selected_crop not in crop_list or selected_price not in price_list:
        return jsonify({"error": "Invalid selection"}), 400

    # Generate predictions using SARIMA
    test_dates, predicted_prices = generate_predictions(selected_crop, selected_price)

    # Prepare pie chart data
    pie_chart_data = {
        "labels": test_dates,  # Test dates as labels
        "values": list(predicted_prices.values())  # Predicted prices as values
    }

    return jsonify(pie_chart_data)
