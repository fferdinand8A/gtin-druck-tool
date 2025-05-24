import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

# Headline
st.markdown("<h1 style='text-align: center;'>Nando´s & Samer´s Toolbox</h1>", unsafe_allow_html=True)

# Session-Initialisierung
if "gtin_input" not in st.session_state:
    st.session_state["gtin_input"] = ""
if "printed" not in st.session_state:
    st.session_state["printed"] = False
if "reset_triggered" not in st.session_state:
    st.session_state["reset_triggered"] = False

# Reset-Logik ausführen vor Anzeige
if st.session_state["reset_triggered"]:
    st.session_state["gtin_input"] = ""
    st.session_state["printed"] = False
    st.session_state["reset_triggered"] = False
    st.experimental_rerun()

# Eingabe-Feld
gtin = st.text_input("GTIN eingeben oder scannen:", key="gtin_input")

# GTIN prüfen
if gtin and len(gtin) in [8, 12, 13, 14] and not st.session_state["printed"]:
    try:
        ean = barcode.get('ean13', gtin.zfill(13), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer, {
            "write_text": True,
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
        </head>
        <body onload="window.print()">
            <img src="data:image/png;base64,{barcode_b64}" alt="GTIN Barcode">
            <div>GTIN: {gtin}</div>
        </body>
        </html>
        """
        components.html(html, height=400)
        st.session_state["printed"] = True

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")

# Reset-Knopf
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("🔄 Reset Eingabe"):
    st.session_state["reset_triggered"] = True
    st.experimental_rerun()
