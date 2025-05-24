import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="GTIN-Toolbox", layout="centered")

# Title
st.markdown("<h1 style='text-align: center;'>Nando´s & Samer´s Toolbox</h1>", unsafe_allow_html=True)

# Session-State initialisieren
if "gtin_input" not in st.session_state:
    st.session_state.gtin_input = ""
if "printed" not in st.session_state:
    st.session_state.printed = False

# Eingabefeld
def trigger_print():
    st.session_state.printed = True

st.text_input("GTIN eingeben oder scannen:", key="gtin_input", on_change=trigger_print)

# Druckvorgang auslösen
if st.session_state.printed and st.session_state.gtin_input and len(st.session_state.gtin_input) in [8, 12, 13, 14]:
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
            <div>GTIN: {gtin}</div>
        </body>
        </html>
        """

        # Öffne in neuem Fenster (verhindert Dauerschleife im iframe!)
        js = f"""
        <script>
        const win = window.open("", "_blank");
        win.document.write(`{html}`);
        win.document.close();
        </script>
        """
        components.html(js, height=0)

        # Zustand zurücksetzen für nächste Eingabe
        st.session_state.printed = False
        st.session_state.gtin_input = ""

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
        st.session_state.printed = False

# Reset-Knopf zentriert
st.markdown("<div style='text-align: center; margin-top: 30px;'>", unsafe_allow_html=True)
if st.button("Reset Eingabe"):
    st.session_state.gtin_input = ""
    st.session_state.printed = False
st.markdown("</div>", unsafe_allow_html=True)
