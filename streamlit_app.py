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
if gtin and len(gtin) in [8, 12, 13, 14] and not st.session_state.printed:
    try:
        # Barcode generieren ohne extra GTIN-Zeile
        ean = barcode.get('ean13', gtin.zfill(13), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer, {
            "write_text": True,
            "module_height": 25,
            "module_width": 0.5,
            "font_size": 10,
            "quiet_zone": 2
        })
        barcode_b64 = base64.b64encode(buffer.getvalue()).decode()

        # HTML für Druckseite – nur Barcode
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
                padding: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
                font-size: 8pt;
            }}
            img {{
                width: 90%;
                height: auto;
                margin: 0;
            }}
        </style>
        </head>
        <body onload="window.print()">
            <img src="data:image/png;base64,{barcode_b64}" alt="GTIN Barcode">
        </body>
        </html>
        """

        # Anzeige & Druck
        components.html(html, height=400)
        st.session_state.printed = True

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
