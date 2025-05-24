import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import streamlit.components.v1 as components

# Seite konfigurieren
st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

# Headline
st.markdown("<h1 style='text-align: center;'>Nando´s & Samer´s Toolbox</h1>", unsafe_allow_html=True)

# Session-Init
if "gtin_input" not in st.session_state:
    st.session_state.gtin_input = ""

# Eingabefeld
gtin = st.text_input("GTIN eingeben oder scannen:", key="gtin_input")

# Button zum manuellen Zurücksetzen
if st.button("🔄 Reset Eingabe"):
    st.session_state.gtin_input = ""
    st.experimental_rerun()

# Wenn gültige GTIN eingegeben
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

        # HTML-Druckseite mit 2 Sek Pause & Reset
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
                    window.location.href = window.location.href.split("?")[0];
                }}, 2000);  // 2 Sek Puffer
            }};
        </script>
        </head>
        <body>
            <img src="data:image/png;base64,{barcode_b64}" alt="GTIN Barcode">
            <div>GTIN: {gtin}</div>
        </body>
        </html>
        """

        # Barcode anzeigen & drucken
        components.html(html, height=400)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
