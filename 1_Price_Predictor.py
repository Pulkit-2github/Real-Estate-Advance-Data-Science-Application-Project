import requests
import streamlit as st
import pickle
import pandas as pd
import numpy as np
import gdown

st.set_page_config(page_title="Viz Demo")

file_id = '1XrGkS-g8G3tOYSIqJFMcERulDGvumkaS'
url = f"https://drive.google.com/uc?id={file_id}"

gdown.download(url, 'pipeline.pkl', quiet=False)

# REPLACE with your own Google Drive file ID
file_id = '1XrGkS-g8G3tOYSIqJFMcERulDGvumkaS'

# Load the pickle file
with open('pipeline.pkl', 'rb') as f:
    pipeline = pickle.load(f)


with open('df.pkl','rb') as file:
    df = pickle.load(file)

st.header('Enter your inputs')

# property_type
property_type = st.selectbox('Property Type',['flat','house'])

# sector
sector = st.selectbox('Sector',sorted(df['sector'].unique().tolist()))

bedrooms = float(st.selectbox('Number of Bedroom',sorted(df['bedRoom'].unique().tolist())))

bathroom = float(st.selectbox('Number of Bathrooms',sorted(df['bathroom'].unique().tolist())))

balcony = st.selectbox('Balconies',sorted(df['balcony'].unique().tolist()))

property_age = st.selectbox('Property Age',sorted(df['agePossession'].unique().tolist()))

built_up_area = float(st.number_input('Built Up Area'))

servant_room = float(st.selectbox('Servant Room',[0.0, 1.0]))
store_room = float(st.selectbox('Store Room',[0.0, 1.0]))

furnishing_type = st.selectbox('Furnishing Type',sorted(df['furnishing_type'].unique().tolist()))
luxury_category = st.selectbox('Luxury Category',sorted(df['luxury_category'].unique().tolist()))
floor_category = st.selectbox('Floor Category',sorted(df['floor_category'].unique().tolist()))

if st.button('Predict'):

    # form a dataframe
    data = [[property_type, sector, bedrooms, bathroom, balcony, property_age, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)

    #st.dataframe(one_df)

    # predict
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22

    # display
    st.text("The price of the flat is between {} Cr and {} Cr".format(round(low,2),round(high,2)))


st.markdown(
    "<div style='text-align: center; font-size: 16px; margin-top: 50px;'>"
    "🚀Created By : <b>Pulkit Mehrotra</b>"
    "</div>", unsafe_allow_html=True
)
