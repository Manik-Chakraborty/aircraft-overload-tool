import streamlit as st
import pandas as pd
import numpy as np

# Simulated dataset based on earlier uploaded Excel for A-2-4 soil (used for all types here)
def load_simulated_data():
    return pd.DataFrame({
        "Soil Type": ["A-2-4"] * 5,
        "Aircraft Name": ["Saab 340B", "DHC‐7", "B757‐200", "EMB‐190 STD", "B717‐200 HGW"],
        "ACR": [60.9, 113.4, 336.5, 238.1, 328.5],
        "PCR_70": [300, 300, 300, 300, 300],
        "PCR_75": [280, 280, 280, 280, 280],
        "PCR_80": [250, 250, 250, 250, 250],
        "PCR_85": [230, 230, 230, 230, 230]
    })

# Interpolate PCR based on degree of saturation
def interpolate_pcr(row, sat):
    saturation_levels = np.array([70, 75, 80, 85])
    pcr_values = np.array([row["PCR_70"], row["PCR_75"], row["PCR_80"], row["PCR_85"]])
    return np.interp(sat, saturation_levels, pcr_values)

# Streamlit UI
st.set_page_config(page_title="Aircraft Overload Demo Tool", layout="wide")
st.title("Prototype: Aircraft Overload Checker Based on Soil Type and Saturation")

st.sidebar.header("User Input")
soil_types = ["A-1-a", "A-1-b", "A-2-4", "A-2-6", "A-2-7", "A-3", "A-4", "A-5", "A-6", "A-7-5", "A-7-6"]
soil_type = st.sidebar.selectbox("Select AASHTO Soil Type", soil_types)

sat_input = st.sidebar.number_input("Enter Degree of Saturation (%)", min_value=0.0, max_value=100.0, value=75.0, step=0.1)

data = load_simulated_data()
aircraft_list = data["Aircraft Name"].tolist()
selected_aircraft = st.sidebar.multiselect("Select Aircraft from Traffic Mix", aircraft_list, default=aircraft_list[:3])

# Filter selected aircraft
filtered_data = data[data["Aircraft Name"].isin(selected_aircraft)].copy()

# Evaluate overload condition
results = []
for _, row in filtered_data.iterrows():
    interpolated_pcr = interpolate_pcr(row, sat_input)
    status = "Overloaded" if row["ACR"] > interpolated_pcr else "Safe"
    results.append({
        "Aircraft": row["Aircraft Name"],
        "ACR": row["ACR"],
        "Interpolated PCR": round(interpolated_pcr, 2),
        "Status": status
    })

# Display results
if results:
    result_df = pd.DataFrame(results)
    st.subheader(f"Aircraft Operational Status at {sat_input}% Saturation on {soil_type} Soil")
    st.dataframe(result_df, use_container_width=True)
else:
    st.warning("Please select at least one aircraft.")
