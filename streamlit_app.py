import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO

# -------------------- Seitenkonfiguration --------------------
st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

# -------------------- App-Titel --------------------
st.markdown("<h1 style='text-align: center;'>Nando´s & Samer´s Toolbox</h1>", unsafe_allow_html=True)

# -------------------- Initialisierung des Session State --------------------
if "gtin_input" not in st.session_state:
    st.session_state.gtin_input = ""

if "reset_triggered" not in st.session_state:
    st.session_state.reset_triggered = False

# -------------------- Reset über Query Parameter --------------------
if "reset" in st.query_params:
    st.session_state.reset_triggered = True
    st.query_params.clear()
    st.rerun()

# -------------------- GTIN-Eingabefeld --------------------
gtin = st.text_input("GTIN eingeben oder scannen:", value=st.session_state.gtin_input, key="gtin_input")

# -------------------- Barcode erzeugen --------------------
if gtin and len(gtin) in [8, 12, 13, 14]:
    try:
        ean = barcode.get('ean13', gtin.zfill(13), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer, {
            "write_text": True,
            "module_height": 15,
            "module_width": 0.4
        })
        st.image(buffer.getvalue(), caption=f"GTIN: {gtin}", use_container_width=True)
    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")

# -------------------- Reset-Button --------------------
st.markdown("<div style='text-align: center; padding-top: 20px;'>", unsafe_allow_html=True)
if st.button("🔁 Reset Eingabe"):
    st.session_state.gtin_input = ""
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
