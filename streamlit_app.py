import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

st.title("🧾 GTIN-Etikett drucken")

gtin = st.text_input("GTIN eingeben oder scannen:")

if gtin and len(gtin) in [8, 12, 13, 14]:
    try:
        # Barcode generieren mit Text
        ean = barcode.get('ean13', gtin.zfill(13), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer, {"write_text": True, "font_size": 16, "text_distance": 2, "module_height": 25})
        b64 = base64.b64encode(buffer.getvalue()).decode()

        # HTML für exakt formatierte Druckansicht
        html = f"""
        <html>
        <head>
            <style>
                @media print {{
                    body {{
                        margin: 0;
                        padding: 0;
                    }}
                    .label {{
                        width: 60mm;
                        height: 30mm;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        page-break-after: always;
                    }}
                }}
                body {{
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                }}
                .label img {{
                    max-width: 100%;
                    height: auto;
                }}
            </style>
        </head>
        <body>
            <div class="label">
                <img src="data:image/png;base64,{b64}" alt="GTIN Barcode">
            </div>
            <script>window.print();</script>
        </body>
        </html>
        """

        # In Streamlit anzeigen
        components.html(html, height=400)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
