import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

st.title("GTIN-Etikett drucken")

gtin = st.text_input("GTIN eingeben oder scannen:")

if gtin and len(gtin) in [8, 12, 13, 14]:
    try:
        # Barcode generieren ohne eingebetteten Text
        ean = barcode.get('ean13', gtin.zfill(13), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer, {
            "write_text": False,
            "module_height": 20,
            "module_width": 0.4
        })
        barcode_b64 = base64.b64encode(buffer.getvalue()).decode()

        # HTML mit 60x30mm Layout
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

        # Seite direkt anzeigen und drucken
        components.html(html, height=400)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
