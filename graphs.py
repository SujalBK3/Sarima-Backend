# # from flask import Flask, request, jsonify
# # import pandas as pd

# # app = Flask(__name__)

# # # Load the CSV file once when the server starts
# # input_file = "01_2018_to_09_2018_Merged.csv"
# # df = pd.read_csv(input_file)

# # @app.route("/get_data", methods=["GET"])
# # def get_data():
# #     try:
# #         crop_num = int(request.args.get("crop_num"))
# #         price_num = int(request.args.get("price_num"))

# #         # Get list of crops and prices
# #         crop_list = df.columns[1:-1].tolist()
# #         price_list = df["States/UTs"].unique().tolist()

# #         if crop_num >= len(crop_list) or price_num >= len(price_list):
# #             return jsonify({"error": "Invalid index"}), 400

# #         selected_crop = crop_list[crop_num]
# #         selected_price = price_list[price_num]

# #         # Filter the data
# #         filtered_df = df[df["States/UTs"] == selected_price]
# #         avg_df = filtered_df[["Date", selected_crop]].copy()
# #         avg_df.columns = ["Date", f"{selected_crop} {selected_price}"]

# #         # Convert DataFrame to dictionary for JSON response
# #         result = avg_df.to_dict(orient="records")
        
# #         return jsonify({"data": result, "title": f"{selected_crop} {selected_price}"})

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # if __name__ == "__main__":
# #     app.run(debug=True)

# from flask import Flask, jsonify, request
# from flask_cors import CORS
# import pandas as pd

# app = Flask(__name__)
# CORS(app)  # Allow frontend access

# df = pd.read_csv("01_2018_to_09_2018_Merged.csv")

# @app.route("/get_options", methods=["GET"])
# def get_options():
#     crop_list = df.columns[1:-1].tolist()
#     price_list = df["States/UTs"].unique().tolist()
#     return jsonify({"crops": crop_list, "prices": price_list})

# @app.route("/get_data", methods=["GET"])
# def get_data():
#     try:
#         crop_index = int(request.args.get("crop_index", 0))
#         price_index = int(request.args.get("price_index", 0))

#         crop_list = df.columns[1:-1].tolist()
#         price_list = df["States/UTs"].unique().tolist()

#         if crop_index >= len(crop_list) or price_index >= len(price_list):
#             return jsonify({"error": "Invalid crop or price index"}), 400

#         selected_crop = crop_list[crop_index]
#         selected_price = price_list[price_index]

#         filtered_df = df[df["States/UTs"] == selected_price]
#         avg_df = filtered_df[["Date", selected_crop]].copy()
#         avg_df.columns = ["Date", "Price"]

#         data = avg_df.to_dict(orient="records")
#         return jsonify(data)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Blueprint, jsonify, request
import pandas as pd

graphs_bp = Blueprint("graphs", __name__)  # Define Blueprint

df = pd.read_csv("01_2018_to_09_2018_Merged.csv")

@graphs_bp.route("/get_options", methods=["GET"])
def get_options():
    crop_list = df.columns[1:-1].tolist()
    price_list = df["States/UTs"].unique().tolist()
    return jsonify({"crops": crop_list, "prices": price_list})

@graphs_bp.route("/get_data", methods=["GET"])
def get_data():
    try:
        crop_index = int(request.args.get("crop_index", 0))
        price_index = int(request.args.get("price_index", 0))

        crop_list = df.columns[1:-1].tolist()
        price_list = df["States/UTs"].unique().tolist()

        if crop_index >= len(crop_list) or price_index >= len(price_list):
            return jsonify({"error": "Invalid crop or price index"}), 400

        selected_crop = crop_list[crop_index]
        selected_price = price_list[price_index]

        filtered_df = df[df["States/UTs"] == selected_price]
        avg_df = filtered_df[["Date", selected_crop]].copy()
        avg_df.columns = ["Date", "Price"]

        data = avg_df.to_dict(orient="records")
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
