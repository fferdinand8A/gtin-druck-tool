import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import streamlit.components.v1 as components

# Seiteneinstellungen
st.set_page_config(page_title="GTIN-Toolbox", layout="centered")

# Titel
st.markdown("<h1 style='text-align: center;'>Nando´s & Samer´s Toolbox</h1>", unsafe_allow_html=True)

# Session-State initialisieren
if "gtin_input" not in st.session_state:
    st.session_state["gtin_input"] = ""
if "trigger_print" not in st.session_state:
    st.session_state["trigger_print"] = False

# Funktion zum Zurücksetzen
def reset():
    st.session_state["gtin_input"] = ""
    st.session_state["trigger_print"] = False

# Eingabefeld
gtin = st.text_input("GTIN eingeben oder scannen:", key="gtin_input", on_change=lambda: st.session_state.update({"trigger_print": True}))

# Barcode und Druck anzeigen, wenn trigger gesetzt
if st.session_state["trigger_print"] and gtin and len(gtin) in [8, 12, 13, 14]:
    try:
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
                    fetch("/_stcore/streamlit_app?reset=true");
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

# Reset-Knopf
if st.button("Reset Eingabe"):
    reset()
    st.experimental_rerun()
