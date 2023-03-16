import pandas as pd
import plotly.express as px
import streamlit as st
import warnings
warnings.filterwarnings("ignore")
# Display title and text
st.title("Week 1 - Data and visualization")
# st.markdown("Here we can see the dataframe created during this weeks project.")

# Read dataframe
dataframe = pd.read_csv(
    "WK1_Airbnb_Amsterdam_listings_proj_solution.csv",
    names=[
        "Airbnb Listing ID",
        "Price",
        "Latitude",
        "Longitude",
        "Meters from chosen location",
        "Location",
    ],
)
@st.cache_data
def convert_df(dataframe):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return dataframe.to_csv().encode('utf-8')

csv = convert_df(dataframe)

dataframe = dataframe[dataframe["Price"] <= 200]

# Convert to integers
dataframe["Airbnb Listing ID"] = dataframe["Airbnb Listing ID"].astype(int)

# Round of values
# Replace pound symbol with euro symbol
dataframe["Price"] = dataframe["Price"].apply(lambda x: str(x).replace("£", " "))

# dataframe["Price"] = dataframe["Price"].apply(lambda x: str(x).replace("€ ", ""))
dataframe["Price"] = dataframe["Price"].apply(lambda x: round(float(x), 2))


# Rename the number to a string
dataframe["Location"] = dataframe["Location"].replace(
    {1.0: "To visit", 0.0: "Airbnb listing"}
)

st.title("Map")

st.markdown("The map shows all Airbnb listings, including our chosen location. Red dots indicate listings in close proximity, while light blue dots represent those farther away. Use the sliders to filter the data. ")

def create_mapbox_figure(min_price, max_price, min_meters, max_meters):
    # filter the dataframe based on the selected price and distance range
    filtered_df = dataframe[(dataframe['Price'] >= min_price) & (dataframe['Price'] <= max_price) & (dataframe['Meters from chosen location'] >= min_meters) & (dataframe['Meters from chosen location'] <= max_meters)]
    color_scale = [
    [0, '#d7191c'],  # red '#d7191c'
    [0.5, '#1a237e'], # dark blue
    [1, '#64b5f6']  # Light blue
    ]
    # create the mapbox figure using Plotly Express
    fig = px.scatter_mapbox(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        color="Meters from chosen location",
        color_continuous_scale=color_scale,
        zoom=11,
        height=500,
        width=800,
        hover_name="Price",
        hover_data=["Meters from chosen location", "Location"],
        labels={"color": "Distance from chosen location (meters)"},
    )
    fig.update_geos(center=dict(lat=filtered_df.iloc[0][2], lon=filtered_df.iloc[0][3]))
    fig.update_layout(mapbox_style="stamen-terrain")
    return fig

# Define the meters_range slider
meters_range = st.sidebar.slider('Meters from chosen location', float(dataframe['Meters from chosen location'].min()), float(dataframe['Meters from chosen location'].max()), (float(dataframe['Meters from chosen location'].min()), float(dataframe['Meters from chosen location'].max())))

# Extract the minimum and maximum values from the meters_range slider
min_meters, max_meters = meters_range

# Define the price_range slider
price_range = st.sidebar.slider('Price range', float(dataframe['Price'].min()), float(dataframe['Price'].max()), (float(dataframe['Price'].min()), float(dataframe['Price'].max())))

# Extract the minimum and maximum values from the price_range slider
min_price, max_price = price_range


fig = create_mapbox_figure(min_price, max_price, min_meters, max_meters)
# Display the figure using st.plotly_chart()
st.plotly_chart(fig, use_container_width=True)

st.markdown("Dataframe uses the experimental_data_editor feature from Streamlit.")

if st.download_button(
   "Press to Download Dataframe",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
):
     st.write('Done!')
else:
     st.write('')
# Display dataframe and text
st.experimental_data_editor(dataframe, num_rows="dynamic")
