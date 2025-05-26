import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import streamlit.components.v1 as components

# Seiteneinstellungen
st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

# Headline
st.markdown("<h1 style='text-align: center;'>Nando´s & Samer´s Toolbox</h1>", unsafe_allow_html=True)

# Session-State initialisieren
if "gtin_input" not in st.session_state:
    st.session_state.gtin_input = ""
if "printed" not in st.session_state:
    st.session_state.printed = False

# Eingabe-Feld
gtin = st.text_input("GTIN eingeben oder scannen:", key="gtin_input")

# Reset-Logik über Button
def reset_input():
    st.session_state["gtin_input"] = ""
    st.session_state["printed"] = False

st.button("🔄 Reset Eingabe", on_click=reset_input)

# GTIN verarbeiten, sobald sie eingegeben wurde
if gtin and len(gtin) in [8]()
