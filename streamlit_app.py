import streamlit as st
import requests
import json

# Load conversion types and units dynamically
with open('conversions.json') as f:
    conversions = json.load(f)

# Apply custom CSS for a better look
st.markdown("""
    <style>
    .title {
        font-size: 2.5em;
        color: #4CAF50;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .convert-button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        margin-top: 10px;
        border-radius: 5px;
        cursor: pointer;
    }
    .convert-button:hover {
        background-color: #45a049;
    }
    .result-box {
        margin-top: 20px;
        padding: 20px;
        border-radius: 10px;
        background-color: #dff0d8;
        color: #3c763d;
        font-size: 1.5em;
        font-weight: bold;
        text-align: center;
        border: 2px solid #4CAF50;
    }
    .error-box {
        margin-top: 20px;
        padding: 20px;
        border-radius: 10px;
        background-color: #f2dede;
        color: #a94442;
        font-size: 1.2em;
        font-weight: bold;
        text-align: center;
        border: 2px solid #e74c3c;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🌟 Dynamic Unit Converter 🌟</div>', unsafe_allow_html=True)

# Sidebar for conversion type selection
st.sidebar.header("Conversion Type")
conversion_type = st.sidebar.selectbox("Select Conversion Type", list(conversions.keys()))

if conversion_type:
    units = list(conversions[conversion_type].keys())
    col1, col2 = st.columns(2)

    with col1:
        unit_from = st.selectbox("From Unit", units)

    with col2:
        unit_to = st.selectbox("To Unit", units)

    value = st.number_input("Enter Value to Convert:", min_value=0.0, step=1.0)

    if st.button("Convert", key="convert_button"):
        with st.spinner("Converting..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/convert",
                    json={"type": conversion_type, "unit_from": unit_from, "unit_to": unit_to, "value": value},
                )
                if response.status_code == 200:
                    result = response.json()["result"]
                    st.markdown(f'<div class="result-box">✅ Converted Value: <strong>{result}</strong></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-box">❌ Conversion failed! Please try again.</div>', unsafe_allow_html=True)
            except requests.ConnectionError:
                st.markdown('<div class="error-box">🚫 Server not running. Please start the Flask server.</div>', unsafe_allow_html=True)
