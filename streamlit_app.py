import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import streamlit.components.v1 as components

# Seiteneinstellungen
st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

# Titel
st.markdown("<h1 style='text-align: center;'>Nando´s & Samer´s Toolbox</h1>", unsafe_allow_html=True)

# Session-State initialisieren
if "gtin_input" not in st.session_state:
    st.session_state.gtin_input = ""
if "printed" not in st.session_state:
    st.session_state.printed = False
if "reset_triggered" not in st.session_state:
    st.session_state.reset_triggered = False

# Reset Funktion
if st.session_state.reset_triggered:
    st.session_state.gtin_input = ""
    st.session_state.printed = False
    st.session_state.reset_triggered = False
    st.rerun()

# Eingabe
gtin = st.text_input("GTIN eingeben oder scannen:", value=st.session_state.gtin_input, key="gtin_input")

# Barcode-Erstellung
if gtin and len(gtin) in [8, 12, 13, 14] and not st.session_state.printed:
    try:
        ean = barcode.get('ean13', gtin.zfill(13), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer, {
            "write_text": True,
            "module_height": 20,
            "module_width": 0.4
        })
        b64 = base64.b64encode(buffer.getvalue()).decode()

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
        </head>
        <body onload="window.print()">
            <img src="data:image/png;base64,{b64}" alt="Barcode">
            <div>GTIN: {gtin}</div>
        </body>
        </html>
        """

        components.html(html, height=400)
        st.session_state.printed = True

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")

# Reset Button
st.markdown("<div style='text-align: center; margin-top: 2em;'>", unsafe_allow_html=True)
if st.button("🔄 Reset Eingabe"):
    st.session_state.reset_triggered = True
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
