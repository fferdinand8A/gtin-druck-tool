import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import time

st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

# Headline
st.markdown("<h1 style='text-align: center;'>Nando´s & Samer´s Toolbox</h1>", unsafe_allow_html=True)

# Session-Initialisierung
if "gtin_input" not in st.session_state:
    st.session_state.gtin_input = ""
if "printed" not in st.session_state:
    st.session_state.printed = False

# Eingabefeld
gtin = st.text_input("GTIN eingeben oder scannen:", key="gtin_input")

# Wenn gültige GTIN eingegeben wurde und noch nicht gedruckt wurde
if gtin and len(gtin) in [8, 12, 13, 14] and not st.session_state.printed:
    try:
        ean = barcode.get('ean13', gtin.zfill(13), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer, {
            "write_text": True,
            "module_height": 20,
            "module_width": 0.4
        })
        barcode_b64 = base64.b64encode(buffer.getvalue()).decode()

        # HTML-Code mit einmaliger Druckauslösung
        html = f"""
        <script>
            setTimeout(function() {{
                window.print();
                fetch('/?reset=true');  // Signal an Streamlit zurück
            }}, 1000);
        </script>
        <img src="data:image/png;base64,{barcode_b64}" alt="GTIN Barcode">
        <div style="font-size: 18px; margin-top: 10px;">GTIN: {gtin}</div>
        """

        st.markdown(html, unsafe_allow_html=True)
        st.session_state.printed = True

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")

# Automatischer Reset bei Reload durch fetch
query_params = st.experimental_get_query_params()
if "reset" in query_params:
    st.session_state.gtin_input = ""
    st.session_state.printed = False
    st.experimental_set_query_params()  # Reset URL zurück
    st.experimental_rerun()

# Manueller Reset-Button
if st.button("🔄 Reset Eingabe"):
    st.session_state.gtin_input = ""
    st.session_state.printed = False
    st.experimental_rerun()
