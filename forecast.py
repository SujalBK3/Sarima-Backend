from flask import Blueprint, jsonify, request
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

def menu(selected_crop, selected_price):
    filtered_df = df[df['States/UTs'] == selected_price].copy()
    return filtered_df, selected_crop

price_forecast_bp = Blueprint('price_forecast', __name__)

df = pd.read_csv("01_2018_to_09_2018_Merged.csv")
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
crop_list = [col for col in df.columns if col not in ['Date', 'States/UTs']]
price_list = df['States/UTs'].unique().tolist()

@price_forecast_bp.route('/options', methods=['GET'])
def get_options():
    return jsonify({'crops': crop_list, 'price_types': price_list})

@price_forecast_bp.route('/get-forecast', methods=['POST'])
def get_forecast():
    data = request.json
    selected_crop = data['crop']
    selected_price = data['price_type']

    if selected_crop not in crop_list or selected_price not in price_list:
        return jsonify({"error": "Invalid selection"}), 400

    df_filtered, selected_crop = menu(selected_crop, selected_price)
    df_filtered['Date'] = pd.to_datetime(df_filtered['Date'], dayfirst=True)
    df_filtered.set_index('Date', inplace=True)
    df_filtered = df_filtered.sort_index()
    df_filtered = df_filtered.asfreq('D')

    train_data = df_filtered.loc['2018-01-01':'2018-06-30', selected_crop]
    test_data = df_filtered.loc['2018-07-01':'2018-09-30', selected_crop]
    pred_steps = len(test_data)

    model = SARIMAX(train_data, order=(5,1,0), seasonal_order=(1,1,1,7))
    model_fit = model.fit()
    predictions = model_fit.forecast(steps=pred_steps)

    def safe_json_convert(data):
        return [(date, None if pd.isna(value) else round(value, 2)) for date, value in data]

    msp = np.nanmedian(train_data)
    std = np.nanstd(train_data)
    
    msp = round(msp, 2) if not np.isnan(msp) else 0
    std = round(std, 2) if not np.isnan(std) else 0

    return jsonify({
        "train": safe_json_convert(zip(train_data.index.strftime('%Y-%m-%d'), train_data.tolist())),
        "test": safe_json_convert(zip(test_data.index.strftime('%Y-%m-%d'), test_data.tolist())),
        "predictions": safe_json_convert(zip(test_data.index.strftime('%Y-%m-%d'), predictions.tolist())),
        "reference_lines": {
            "msp": msp,
            "sell_threshold": round(msp + std, 2),
            "stockpile_threshold": round(msp - std, 2)
        }
    })
