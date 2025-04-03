import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = "01_2018_to_09_2018_Merged.csv"
df = pd.read_csv(file_path)

# List of essential commodities
essential_commodities = ["Rice", "Wheat", "Sugar", "Salt", "Milk", "Pulses", "Oil", "Onions", 
                         "Potatoes", "Tomatoes", "Eggs", "Tea", "Coffee", "Fish", "Meat", 
                         "Butter", "Cheese", "Fruits", "Vegetables", "Spices", "Lentils", "Flour"]

# Select a state (Change this to any state from the dataset)
selected_state = "Andhra Pradesh"

# Filter data for the selected state
state_data = df[df["States/UTs"] == selected_state]

# Filter only essential commodities
state_data = state_data[state_data["Commodity"].isin(essential_commodities)]

# Convert Price column to numeric
state_data["Price"] = pd.to_numeric(state_data["Price"], errors="coerce")
state_data.dropna(subset=["Price"], inplace=True)

# Aggregate price data per commodity
price_data = state_data.groupby("Commodity")["Price"].sum()

# Check if data is available
if price_data.empty:
    print("No data available for the selected state.")
else:
    # Plot the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(price_data, labels=price_data.index, autopct='%1.1f%%', startangle=140)
    plt.title(f"Commodity Prices in {selected_state}")
    plt.show()
