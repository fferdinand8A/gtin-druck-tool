import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

# Titel
st.markdown("<h1 style='text-align: center;'>Nando´s & Samer´s Toolbox</h1>", unsafe_allow_html=True)

# Query-Parameter auslesen (für automatischen Reset)
query_params = st.query_params
if "reset" in query_params:
    st.session_state["gtin_input"] = ""

# Session-Variablen initialisieren
if "gtin_input" not in st.session_state:
    st.session_state["gtin_input"] = ""

# Reset-Funktion
def reset_input():
    st.session_state["gtin_input"] = ""
    st.rerun()

# Eingabe-Feld
gtin = st.text_input("GTIN eingeben oder scannen:", key="gtin_input")

# GTIN prüfen
if gtin and len(gtin) in [8, 12, 13, 14]:
    try:
        # Barcode generieren
        ean = barcode.get('ean13', gtin.zfill(13), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer, {
            "write_text": True,
            "module_height": 20,
            "module_width": 0.4
        })
        barcode_b64 = base64.b64encode(buffer.getvalue()).decode()

        # HTML mit Druck und Auto-Reset
        html = f"""
        <html>
        <head>
        <meta charset="utf-8">
        <script>
            function triggerPrintAndReset() {{
                window.print();
                setTimeout(function() {{
                    window.location.href = window.location.origin + window.location.pathname + "?reset=1";
                }}, 2000);
            }}
        </script>
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
        <body onload="triggerPrintAndReset()">
            <img src="data:image/png;base64,{barcode_b64}" alt="GTIN Barcode">
            <div>GTIN: {gtin}</div>
        </body>
        </html>
        """

        # Druckseite anzeigen
        components.html(html, height=400)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")

# Reset-Button
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 Reset Eingabe"):
    reset_input()
