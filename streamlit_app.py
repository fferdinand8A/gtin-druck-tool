import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="GTIN-Toolbox", layout="centered")

# Title
st.markdown("<h1 style='text-align: center;'>Nando´s & Samer´s Toolbox</h1>", unsafe_allow_html=True)

# Initialisieren
if "printed" not in st.session_state:
    st.session_state.printed = False

# Eingabefeld
def trigger_print():
    st.session_state.printed = True

gtin_input = st.text_input("GTIN eingeben oder scannen:", key="gtin_input", on_change=trigger_print)

# Barcode erzeugen und Druck auslösen
if st.session_state.get("printed") and gtin_input and len(gtin_input) in [8, 12, 13, 14]:
    try:
        ean = barcode.get('ean13', gtin_input.zfill(13), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer, {
            "write_text": False,
            "module_height": 20,
            "module_width": 0.4
        })
        barcode_b64 = base64.b64encode(buffer.getvalue()).decode()

        html = f"""
        <html>
        <head>
        <style>
            @media print {{
                @page {{
                    size: 60mm 30mm;
                    margin: 0;
                }}
                body {{
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                    font-family: Arial, sans-serif;
                    font-size: 10pt;
                }}
                img {{
                    max-height: 20mm;
                }}
            }}
        </style>
        </head>
        <body onload="window.print(); setTimeout(() => window.close(), 500);">
            <img src="data:image/png;base64,{barcode_b64}" alt="GTIN Barcode">
            <div>GTIN: {gtin_input}</div>
        </body>
        </html>
        """

        components.html(f"<script>let w = window.open('', '_blank'); w.document.write(`{html}`); w.document.close();</script>", height=0)

        # Reset vorbereiten und Seite neu laden
        del st.session_state["gtin_input"]
        st.session_state.printed = False
        st.experimental_rerun()

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
        st.session_state.printed = False

# Reset-Knopf zentriert
st.markdown("<div style='text-align: center; margin-top: 30px;'>", unsafe_allow_html=True)
if st.button("Reset Eingabe"):
    if "gtin_input" in st.session_state:
        del st.session_state["gtin_input"]
    st.session_state.printed = False
    st.experimental_rerun()
st.markdown("</div>", unsafe_allow_html=True)
