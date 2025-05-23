import streamlit as st
import barcode
from barcode.writer import ImageWriter
import io
import base64
from PIL import Image

st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

st.title("🖨️ GTIN-Etikett direkt drucken")
st.caption("Gib eine GTIN/EAN ein, sieh den Barcode und drucke ihn direkt aus dem Browser.")

gtin = st.text_input("GTIN eingeben oder scannen:", max_chars=14)

if gtin and len(gtin) >= 8:
    try:
        # Barcode erzeugen
        ean = barcode.get("ean13", gtin.zfill(13), writer=ImageWriter())
        buffer = io.BytesIO()
        ean.write(buffer, options={"module_height": 15.0, "font_size": 10})
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()

        # HTML für Druckvorschau mit auto print()
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Etikett drucken</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    text-align: center;
                }}
                img {{
                    margin-top: 20px;
                    max-width: 100%;
                    height: auto;
                }}
                @media print {{
                    body {{
                        margin: 0;
                    }}
                }}
            </style>
        </head>
        <body>
            <img src="data:image/png;base64,{img_base64}" alt="GTIN Barcode" />
            <p>GTIN: {gtin}</p>
            <script>
                window.onload = function() {{
                    window.print();
                }}
            </script>
        </body>
        </html>
        '''

        html_bytes = html.encode("utf-8")
        b64_html = base64.b64encode(html_bytes).decode("utf-8")
        data_url = f"data:text/html;base64,{b64_html}"

        # Button anzeigen
        st.markdown(f"<a href='{data_url}' target='_blank'>🖨️ Etikett in neuem Tab drucken</a>", unsafe_allow_html=True)

        # Barcode auch direkt in Streamlit anzeigen
        st.image(buffer, caption=f"GTIN: {gtin}", use_column_width=False)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
elif gtin:
    st.warning("Bitte mindestens 8 Ziffern eingeben.")
