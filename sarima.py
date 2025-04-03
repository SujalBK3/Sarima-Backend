# # import matplotlib
# # matplotlib.use('Agg')  # Prevents GUI issues with Matplotlib

# # from flask import Blueprint, request, send_file
# # import pandas as pd
# # import matplotlib.pyplot as plt
# # import seaborn as sns
# # from statsmodels.tsa.statespace.sarimax import SARIMAX
# # from sklearn.metrics import mean_absolute_error
# # from io import BytesIO

# # sarima_bp = Blueprint('sarima', __name__)

# # # Load dataset
# # input_file = "01_2018_to_09_2018_Merged.csv"
# # df = pd.read_csv(input_file)

# # crop_list = df.columns[1:-1].tolist()
# # price_list = df["States/UTs"].unique().tolist()

# # def menu(crop_num, price_num):
# #     selected_crop = crop_list[crop_num]
# #     selected_price = price_list[price_num]
    
# #     filtered_df = df[df["States/UTs"] == selected_price]
# #     avg_df = filtered_df[["Date", selected_crop]].copy()
# #     avg_df.columns = ["Date", f"{selected_crop} {selected_price}"]
    
# #     return avg_df, f"{selected_crop} {selected_price}"

# # @sarima_bp.route('/predict', methods=['GET'])
# # def predict():
# #     crop_num = int(request.args.get("crop_num"))
# #     price_num = int(request.args.get("price_num"))

# #     df_filtered, selected_crop = menu(crop_num, price_num)

# #     df_filtered['Date'] = pd.to_datetime(df_filtered['Date'], dayfirst=True)
# #     df_filtered.set_index('Date', inplace=True)
# #     df_filtered = df_filtered.sort_index()

# #     # Fix the frequency issue
# #     df_filtered = df_filtered.asfreq('D')  # Set daily frequency

# #     train_data = df_filtered.loc['2018-01-01':'2018-06-30', selected_crop]
# #     test_data = df_filtered.loc['2018-07-01':'2018-09-30', selected_crop]
# #     pred_steps = len(test_data)

# #     model = SARIMAX(train_data, order=(5,1,0), seasonal_order=(1,1,1,30))
# #     model_fit = model.fit()
# #     predictions = model_fit.forecast(steps=pred_steps)

# #     # Plot results
# #     plt.figure(figsize=(12, 6))
# #     sns.lineplot(data=train_data, label="Training Data (Jan-June)", color='blue')
# #     sns.lineplot(x=test_data.index, y=test_data, label="Actual Data (July-Sept)", color='green')
# #     sns.lineplot(x=test_data.index, y=predictions, label="Predicted Data", color='red')
# #     plt.xlabel("Date")
# #     plt.ylabel(selected_crop)
# #     plt.title("SARIMA Model Prediction")
# #     plt.legend()
# #     plt.xticks(rotation=45)

# #     img = BytesIO()
# #     plt.savefig(img, format='png')
# #     img.seek(0)

# #     return send_file(img, mimetype='image/png')

# import matplotlib
# matplotlib.use('Agg')  # Prevents GUI issues

# from flask import Blueprint, request, send_file, jsonify
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from statsmodels.tsa.statespace.sarimax import SARIMAX
# from io import BytesIO

# sarima_bp = Blueprint('sarima', __name__)

# # Load dataset
# input_file = "01_2018_to_09_2018_Merged.csv"
# df = pd.read_csv(input_file)

# crop_list = df.columns[1:-1].tolist()
# price_list = df["States/UTs"].unique().tolist()

# def menu(selected_crop, selected_price):
#     filtered_df = df[df["States/UTs"] == selected_price]
#     avg_df = filtered_df[["Date", selected_crop]].copy()
#     avg_df.columns = ["Date", f"{selected_crop} {selected_price}"]
#     return avg_df, f"{selected_crop} {selected_price}"

# @sarima_bp.route('/options', methods=['GET'])
# def get_options():
#     return jsonify({"crops": crop_list, "states": price_list})

# @sarima_bp.route('/predict', methods=['GET'])
# def predict():
#     selected_crop = request.args.get("crop")
#     selected_price = request.args.get("state")

#     if selected_crop not in crop_list or selected_price not in price_list:
#         return jsonify({"error": "Invalid selection"}), 400

#     df_filtered, selected_crop = menu(selected_crop, selected_price)

#     df_filtered['Date'] = pd.to_datetime(df_filtered['Date'], dayfirst=True)
#     df_filtered.set_index('Date', inplace=True)
#     df_filtered = df_filtered.sort_index()

#     # Fix frequency issue
#     df_filtered = df_filtered.asfreq('D')

#     train_data = df_filtered.loc['2018-01-01':'2018-06-30', selected_crop]
#     test_data = df_filtered.loc['2018-07-01':'2018-09-30', selected_crop]
#     pred_steps = len(test_data)

#     model = SARIMAX(train_data, order=(5,1,0), seasonal_order=(1,1,1,30))
#     model_fit = model.fit()
#     predictions = model_fit.forecast(steps=pred_steps)

#     # Plot results
#     plt.figure(figsize=(12, 6))
#     sns.lineplot(data=train_data, label="Training Data (Jan-June)", color='blue')
#     sns.lineplot(x=test_data.index, y=test_data, label="Actual Data (July-Sept)", color='green')
#     sns.lineplot(x=test_data.index, y=predictions, label="Predicted Data", color='red')
#     plt.xlabel("Date")
#     plt.ylabel(selected_crop)
#     plt.title("SARIMA Model Prediction")
#     plt.legend()
#     plt.xticks(rotation=45)

#     img = BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)

#     return send_file(img, mimetype='image/png')


import matplotlib
matplotlib.use('Agg')  # Prevents GUI issues

from flask import Blueprint, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

sarima_bp = Blueprint('sarima', __name__)

# Load dataset
input_file = "01_2018_to_09_2018_Merged.csv"
df = pd.read_csv(input_file)

crop_list = df.columns[1:-1].tolist()
price_list = df["States/UTs"].unique().tolist()

def menu(selected_crop, selected_price):
    filtered_df = df[df["States/UTs"] == selected_price]
    avg_df = filtered_df[["Date", selected_crop]].copy()
    avg_df.columns = ["Date", f"{selected_crop} {selected_price}"]
    return avg_df, f"{selected_crop} {selected_price}"

@sarima_bp.route('/options', methods=['GET'])
def get_options():
    return jsonify({"crops": crop_list, "states": price_list})

@sarima_bp.route('/predict', methods=['GET'])
def predict():
    selected_crop = request.args.get("crop")
    selected_price = request.args.get("state")

    if selected_crop not in crop_list or selected_price not in price_list:
        return jsonify({"error": "Invalid selection"}), 400

    df_filtered, selected_crop = menu(selected_crop, selected_price)

    df_filtered['Date'] = pd.to_datetime(df_filtered['Date'], dayfirst=True)
    df_filtered.set_index('Date', inplace=True)
    df_filtered = df_filtered.sort_index()
    df_filtered = df_filtered.asfreq('D')  # Fix frequency issue

    train_data = df_filtered.loc['2018-01-01':'2018-06-30', selected_crop]
    test_data = df_filtered.loc['2018-07-01':'2018-09-30', selected_crop]
    pred_steps = len(test_data)

    # model = SARIMAX(train_data, order=(5,1,0), seasonal_order=(1,1,1,30))
    model = SARIMAX(train_data, order=(5,1,0), seasonal_order=(1,1,1,7))  # Adjusted seasonality

    model_fit = model.fit()
    predictions = model_fit.forecast(steps=pred_steps)

    

    def safe_json_convert(data):
        return [(date, None if pd.isna(value) else value) for date, value in data]

    return jsonify({
        "train": safe_json_convert(zip(train_data.index.strftime('%Y-%m-%d'), train_data.tolist())),
        "test": safe_json_convert(zip(test_data.index.strftime('%Y-%m-%d'), test_data.tolist())),
        "predictions": safe_json_convert(zip(test_data.index.strftime('%Y-%m-%d'), predictions.tolist()))
    })

@sarima_bp.route('/price_and_date_options', methods=['GET'])
def get_price_and_date_options():
    selected_price = request.args.get("state")  # Get selected state from request

    # If no state is provided, we return options for all states
    if not selected_price:
        price_types = price_list
        # Get unique dates from the test data
        test_data_dates = df['Date'].dt.strftime('%Y-%m-%d').unique().tolist()
    else:
        # Filter by the selected price type
        df_filtered = df[df["States/UTs"] == selected_price]
        test_data_dates = df_filtered.loc['2018-07-01':'2018-09-30', 'Date'].dt.strftime('%Y-%m-%d').unique().tolist()

    return jsonify({
        "price_types": price_list,
        "dates": test_data_dates
    })




@sarima_bp.route('/predicted_data', methods=['GET'])
def get_predicted_data():
    selected_price = request.args.get("state")  # Get selected state from request
    selected_date = request.args.get("date")  # Get selected date from request

    # Validate input
    if selected_price not in price_list:
        return jsonify({"error": "Invalid price type (state)"}), 400
    if selected_date not in df['Date'].dt.strftime('%Y-%m-%d').unique().tolist():
        return jsonify({"error": "Invalid date"}), 400

    # Filter the dataframe based on the selected price type (state)
    df_filtered = df[df["States/UTs"] == selected_price]
    df_filtered['Date'] = pd.to_datetime(df_filtered['Date'], dayfirst=True)
    df_filtered.set_index('Date', inplace=True)
    df_filtered = df_filtered.sort_index()
    df_filtered = df_filtered.asfreq('D')  # Fix frequency issue

    # Specify the crop (you can adjust this based on your selection logic)
    selected_crop = df.columns[1]  # You can choose any crop for the example, adjust if necessary

    # Train SARIMA model
    train_data = df_filtered.loc['2018-01-01':'2018-06-30', selected_crop]
    test_data = df_filtered.loc['2018-07-01':'2018-09-30', selected_crop]
    pred_steps = len(test_data)

    model = SARIMAX(train_data, order=(5,1,0), seasonal_order=(1,1,1,7))
    model_fit = model.fit()
    predictions = model_fit.forecast(steps=pred_steps)

    # Find the prediction for the selected date
    predicted_value = predictions[df_filtered.loc['2018-07-01':'2018-09-30', 'Date'].strftime('%Y-%m-%d') == selected_date].tolist()
    
    # Ensure that we get a valid predicted value for the date
    if not predicted_value:
        return jsonify({"error": "No prediction found for the selected date"}), 400

    return jsonify({
        "selected_date": selected_date,
        "predicted_value": predicted_value[0]  # Send the predicted value for the selected date
    })


