import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="GTIN-Toolbox", layout="centered")

# Title
st.markdown("<h1 style='text-align: center;'>Nando´s & Samer´s Toolbox</h1>", unsafe_allow_html=True)

# Session-State vorbereiten
if "gtin_input" not in st.session_state:
    st.session_state.gtin_input = ""
if "trigger_print" not in st.session_state:
    st.session_state.trigger_print = False

# Eingabe-Callback
def trigger_barcode():
    st.session_state.trigger_print = True

# GTIN Eingabefeld
st.text_input("GTIN eingeben oder scannen:", key="gtin_input", on_change=trigger_barcode)

# Barcode anzeigen + automatisch drucken
if st.session_state.trigger_print and st.session_state.gtin_input and len(st.session_state.gtin_input) in [8, 12, 13, 14]:
    try:
        gtin = st.session_state.gtin_input
        ean = barcode.get('ean13', gtin.zfill(13), writer=ImageWriter())
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
                }}
            }}
            body {{
                width: 60mm;
                height: 30mm;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
                font-size: 10pt;
            }}
            img {{
                max-height: 20mm;
            }}
        </style>
        <script>
            window.onload = function() {{
                window.print();
                setTimeout(function() {{
                    fetch('/_stcore/reset', {{ method: 'POST' }}).then(() => window.location.reload());
                }}, 1000);
            }};
        </script>
        </head>
        <body>
            <img src="data:image/png;base64,{barcode_b64}" alt="GTIN Barcode">
            <div>GTIN: {gtin}</div>
        </body>
        </html>
        """

        components.html(html, height=400)
    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")

# Reset-Knopf korrekt platziert
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("Reset Eingabe"):
    st.session_state.gtin_input = ""
    st.session_state.trigger_print = False
st.markdown("</div>", unsafe_allow_html=True)
