from flask import Blueprint, jsonify, request
import pandas as pd

commodities_bp = Blueprint("commodities", __name__)  # Define Blueprint

df = pd.read_csv("01_2018_to_09_2018_Merged.csv")

@commodities_bp.route("/get_options", methods=["GET"])
def get_options():
    # Extract available dates and price types (States/UTs)
    dates = df["Date"].unique().tolist()
    price_types = df["States/UTs"].unique().tolist()
    return jsonify({"dates": dates, "prices": price_types})

@commodities_bp.route("/get_data", methods=["GET"])
def get_data():
    try:
        # Get the selected date and price type from query parameters
        selected_date = request.args.get("date")
        selected_price = request.args.get("price")

        # Validate the inputs
        if not selected_date or not selected_price:
            return jsonify({"error": "Missing date or price"}), 400

        # Filter the DataFrame based on selected date and price type (States/UTs)
        filtered_df = df[(df["Date"] == selected_date) & (df["States/UTs"] == selected_price)]

        # Extract the first 6 crops (excluding Date and States/UTs columns)
        crop_columns = df.columns[1:-1]  # All columns except 'Date' and 'States/UTs'
        selected_crops = crop_columns[:6]  # Select the first 6 crops

        # Create a list to store the prices of the first 6 crops for the selected date and price type
        crop_prices = []
        for crop in selected_crops:
            crop_prices.append({crop: filtered_df[crop].values.tolist()})

        # Return the prices of the first 6 crops
        return jsonify({"data": crop_prices})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
