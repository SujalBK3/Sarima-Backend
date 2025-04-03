# # # from flask import Blueprint, request, jsonify
# # # import pandas as pd
# # # import plotly.express as px
# # # import os

# # # # Create Flask Blueprint
# # # pie_chart_bp = Blueprint('pie_chart', __name__)

# # # def load_and_process_data(file_path, selected_date=None, state=None):
# # #     if not os.path.exists(file_path):
# # #         raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
# # #     df = pd.read_csv(file_path)
# # #     df = df[~df['States/UTs'].isin(["Average Price", "Maximum Price", "Minimum Price", "Modal Price"])]
# # #     df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')

# # #     if selected_date:
# # #         selected_date = pd.to_datetime(selected_date, format='%d/%m/%Y', errors='coerce')
# # #         df = df[df['Date'] == selected_date]
    
# # #     if state:
# # #         df = df[df['States/UTs'] == state]  # Filter by state if provided

# # #     df_melted = df.melt(id_vars=['States/UTs', 'Date'], var_name='Commodity', value_name='Price')
# # #     df_melted.rename(columns={'States/UTs': 'State'}, inplace=True)
# # #     df_melted['Price'] = pd.to_numeric(df_melted['Price'], errors='coerce')
# # #     df_melted.dropna(subset=['Price'], inplace=True)

# # #     return df_melted

# # # df = pd.read_csv("01_2018_to_09_2018_Merged.csv")

# # # @pie_chart_bp.route("/get_options", methods=["GET"])
# # # def get_options():
# # #     price_list = df["States/UTs"].unique().tolist()
# # #     return jsonify({"prices": price_list})

# # # @pie_chart_bp.route('/plot_pie_chart', methods=['GET'])
# # # def plot_pie_chart():
# # #     file_path = "01_2018_to_09_2018_Merged.csv"
# # #     selected_date = request.args.get('date')
# # #     selected_state = request.args.get('state')  # Get the state from request

# # #     try:
# # #         df_melted = load_and_process_data(file_path, selected_date, selected_state)
# # #         grouped = df_melted.groupby(['Commodity'])['Price'].sum().reset_index()

# # #         if grouped.empty:
# # #             return jsonify({"message": "No data available for the selected date or state."}), 404

# # #         # Convert data into the expected format for the frontend
# # #         response_data = {
# # #             "labels": grouped["Commodity"].tolist(),
# # #             "values": grouped["Price"].tolist(),
# # #         }

# # #         return jsonify(response_data)

# # #     except Exception as e:
# # #         return jsonify({"error": str(e)}), 500

# # from flask import Blueprint, request, jsonify
# # import pandas as pd
# # import os

# # pie_chart_bp = Blueprint('pie_chart', __name__)

# # # Load dataset once
# # file_path = "01_2018_to_09_2018_Merged.csv"
# # if os.path.exists(file_path):
# #     df = pd.read_csv(file_path)
# # else:
# #     df = None  # Handle missing file later

# # # Get unique states and dates
# # unique_states = df["States/UTs"].unique().tolist() if df is not None else []
# # unique_dates = df["Date"].unique().tolist() if df is not None else []


# # def load_and_process_data(selected_date_index=None, selected_state_index=None):
# #     if df is None:
# #         return None, "Data file not found."

# #     # Ensure the index is within bounds
# #     if selected_date_index is not None:
# #         try:
# #             selected_date = unique_dates[int(selected_date_index)]  # Get actual date
# #         except (ValueError, IndexError):
# #             return None, "Invalid date selection."
# #     else:
# #         selected_date = None

# #     if selected_state_index is not None:
# #         try:
# #             selected_state = unique_states[int(selected_state_index)]  # Get actual state
# #         except (ValueError, IndexError):
# #             return None, "Invalid state selection."
# #     else:
# #         selected_state = None

# #     # Process dataset
# #     df_filtered = df.copy()
# #     df_filtered = df_filtered[~df_filtered['States/UTs'].isin(["Average Price", "Maximum Price", "Minimum Price", "Modal Price"])]
# #     df_filtered['Date'] = pd.to_datetime(df_filtered['Date'], format='%d/%m/%Y', errors='coerce')

# #     # Apply filters
# #     if selected_date:
# #         df_filtered = df_filtered[df_filtered['Date'] == pd.to_datetime(selected_date, errors='coerce')]

# #     if selected_state:
# #         df_filtered = df_filtered[df_filtered['States/UTs'] == selected_state]

# #     if df_filtered.empty:
# #         return None, "No data available for the selected date or state."

# #     # Transform data for pie chart
# #     df_melted = df_filtered.melt(id_vars=['States/UTs', 'Date'], var_name='Commodity', value_name='Price')
# #     df_melted.rename(columns={'States/UTs': 'State'}, inplace=True)
# #     df_melted['Price'] = pd.to_numeric(df_melted['Price'], errors='coerce')
# #     df_melted.dropna(subset=['Price'], inplace=True)

# #     return df_melted, None


# # # API to get options (indexes for frontend)
# # @pie_chart_bp.route("/get_options", methods=["GET"])
# # def get_options():
# #     return jsonify({
# #         "states": [{"index": i, "name": state} for i, state in enumerate(unique_states)],
# #         "dates": [{"index": i, "date": date} for i, date in enumerate(unique_dates)]
# #     })


# # # API to return pie chart data
# # @pie_chart_bp.route('/plot_pie_chart', methods=['GET'])
# # def plot_pie_chart():
# #     selected_date_index = request.args.get('date_index')
# #     selected_state_index = request.args.get('state_index')

# #     df_melted, error_message = load_and_process_data(selected_date_index, selected_state_index)

# #     if error_message:
# #         return jsonify({"message": error_message}), 404

# #     grouped = df_melted.groupby(['Commodity'])['Price'].sum().reset_index()

# #     return jsonify({
# #         "labels": grouped["Commodity"].tolist(),
# #         "values": grouped["Price"].tolist(),
# #     })


# from flask import Blueprint, request, jsonify
# import pandas as pd
# import os

# pie_chart_bp = Blueprint('pie_chart', __name__)

# # Load dataset once
# file_path = "01_2018_to_09_2018_Merged.csv"
# if os.path.exists(file_path):
#     df = pd.read_csv(file_path)
#     df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')  # Fixing Date conversion
# else:
#     df = None  # Handle missing file later

# # Get unique states and dates safely
# unique_states = df["States/UTs"].dropna().unique().tolist() if df is not None else []
# unique_dates = df["Date"].dropna().dt.strftime('%d/%m/%Y').unique().tolist() if df is not None else []


# def load_and_process_data(selected_date_index=None, selected_state_index=None):
#     if df is None:
#         return None, "Data file not found."

#     try:
#         selected_date = unique_dates[int(selected_date_index)] if selected_date_index is not None else None
#         selected_state = unique_states[int(selected_state_index)] if selected_state_index is not None else None
#     except (ValueError, IndexError):
#         return None, "Invalid date or state selection."

#     # Process dataset
#     df_filtered = df.copy()
#     # df_filtered = df_filtered[~df_filtered['States/UTs'].isin(["Average Price", "Maximum Price", "Minimum Price", "Modal Price"])]

#     # Apply filters
#     if selected_date:
#         selected_date_dt = pd.to_datetime(selected_date, format='%d/%m/%Y', errors='coerce')
#         if not pd.isna(selected_date_dt):
#             df_filtered = df_filtered[df_filtered['Date'] == selected_date_dt]

#     if selected_state:
#         df_filtered = df_filtered[df_filtered['States/UTs'] == selected_state]

#     if df_filtered.empty:
#         return None, "No data available for the selected date or state."

#     # Transform data for pie chart
#     df_melted = df_filtered.melt(id_vars=['States/UTs', 'Date'], var_name='Commodity', value_name='Price')
#     df_melted.rename(columns={'States/UTs': 'State'}, inplace=True)
#     df_melted['Price'] = pd.to_numeric(df_melted['Price'], errors='coerce')
#     df_melted.dropna(subset=['Price'], inplace=True)

#     return df_melted, None


# # API to get options (indexes for frontend)
# @pie_chart_bp.route("/get_options", methods=["GET"])
# def get_options():
#     return jsonify({
#         "states": [{"index": i, "name": state} for i, state in enumerate(unique_states)],
#         "dates": [{"index": i, "date": date} for i, date in enumerate(unique_dates)]
#     })


# # API to return pie chart data
# @pie_chart_bp.route('/plot_pie_chart', methods=['GET'])
# def plot_pie_chart():
#     selected_date_index = request.args.get('date_index')
#     selected_state_index = request.args.get('state_index')

#     df_melted, error_message = load_and_process_data(selected_date_index, selected_state_index)

#     if error_message:
#         return jsonify({"message": error_message}), 404

#     grouped = df_melted.groupby(['Commodity'])['Price'].sum().reset_index()

#     if grouped.empty:
#         return jsonify({"message": "No data available for the selected filters."}), 404

#     return jsonify({
#         "labels": grouped["Commodity"].tolist(),
#         "values": grouped["Price"].tolist(),
#     })

import pandas as pd
from flask import Blueprint, request, jsonify

pie_chart_bp = Blueprint('pie_chart', __name__)

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

data_file = "01_2018_to_09_2018_Merged.csv"
df = load_data(data_file)

# Extract unique dates and price types
unique_dates = df['Date'].unique().tolist()
unique_price_types = df['States/UTs'].unique().tolist()

@pie_chart_bp.route('/get_pie_data', methods=['GET'])
def get_pie_data():
    date = request.args.get('date')
    price_type = request.args.get('price_type')
    
    # Filter by date
    df_date = df[df['Date'] == date]
    
    # Filter by price type (Average Price, Maximum Price, etc.)
    df_filtered = df_date[df_date['States/UTs'] == price_type]
    
    if df_filtered.empty:
        return jsonify({"error": "No data found for the selected date and price type."}), 404
    
    # Extract item prices
    items = df_filtered.columns[1:-1].tolist()  # Exclude 'States/UTs' and 'Date'
    prices = df_filtered.iloc[0, 1:-1].tolist()  # Get price values
    
    return jsonify({"items": items, "prices": prices})

@pie_chart_bp.route("/get_options", methods=["GET"])
def get_options():
    return jsonify({
        "dates": [{"index": i, "date": date} for i, date in enumerate(unique_dates)],
        "price_types": [{"index": i, "type": price_type} for i, price_type in enumerate(unique_price_types)]
    })
