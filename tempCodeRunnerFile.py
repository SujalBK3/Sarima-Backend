from flask import Flask, request, jsonify
import plotly.graph_objects as go
import json
import math  # Import math module for log and sine functions
from flask_cors import CORS
from plotly.utils import PlotlyJSONEncoder

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Function to create a graph based on type
def create_graph(graph_type):
    x = 30
    fig = go.Figure()
    x_values = list(range(-10, 11))  # X values from -10 to 10

    if graph_type == "linear":
        y_values = [2 * x + 3 for x in x_values]
        title = "Linear Graph: y = 2x + 3"
    elif graph_type == "quadratic":
        y_values = [x**2 for x in x_values]
        title = "Quadratic Graph: y = x²"
    elif graph_type == "cubic":
        y_values = [x**3 for x in x_values]
        title = "Cubic Graph: y = x³"
    elif graph_type == "logarithmic":
        x_values = [x for x in range(1, 11)]  # Log function can't have x ≤ 0
        y_values = [2.5 * math.log(x) for x in x_values]
        title = "Logarithmic Graph: y = 2.5 log(x)"
    elif graph_type == "exponential":
        y_values = [2**x for x in x_values]
        title = "Exponential Graph: y = 2^x"
    elif graph_type == "sine":
        y_values = [math.sin(x) for x in x_values]
        title = "Sine Wave: y = sin(x)"
    else:
        return None  # Invalid graph type

    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers'))
    fig.update_layout(
        title=title,
        xaxis_title="X Axis",
        yaxis_title="Y Axis",
        width=300 ,
        height=300 ,
        margin=dict(l=0, b=x, r=x, t=x )
    )

    return json.dumps(fig, cls=PlotlyJSONEncoder)  # Serialize graph JSON

# API for menu-driven graphs (Linear, Quadratic, Cubic)
@app.route("/api/graph", methods=["POST"])
def generate_graph():
    try:
        data = request.get_json()
        if not data or "graphType" not in data:
            return jsonify({"error": "Missing graphType"}), 400  # Bad Request

        graph_type = data["graphType"]
        graph_json = create_graph(graph_type)

        if graph_json is None:
            return jsonify({"error": "Invalid graph type"}), 400  # Invalid graph type

        return jsonify({"graph": graph_json})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error

# API for default graphs (Logarithmic, Exponential, Sine) at startup
@app.route("/api/default-graphs", methods=["GET"])
def get_default_graphs():
    default_graphs = {
        "logarithmic": create_graph("logarithmic"),
        "exponential": create_graph("exponential"),
        "sine": create_graph("sine"),
    }
    return jsonify({"graphs": default_graphs})

if __name__ == "__main__":
    app.run(debug=True)