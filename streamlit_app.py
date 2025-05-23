import streamlit as st
import barcode
from barcode.writer import ImageWriter
from PIL import Image
import io
import base64

st.set_page_config(page_title="GTIN Etikett", layout="centered")

st.markdown("""
    <style>
        @media print {
            body * {
                visibility: hidden;
            }
            #etikett, #etikett * {
                visibility: visible;
            }
            #etikett {
                position: absolute;
                left: 0;
                top: 0;
                width: 100%;
                text-align: center;
            }
        }
        button {
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📦 GTIN-Etikett drucken")
gtin = st.text_input("GTIN eingeben oder scannen:", max_chars=14)

if gtin and len(gtin) >= 8:
    try:
        ean = barcode.get("ean13", gtin.zfill(13), writer=ImageWriter())
        buffer = io.BytesIO()
        ean.write(buffer, options={"module_height": 15.0, "font_size": 10})
        buffer.seek(0)
        img_data = base64.b64encode(buffer.getvalue()).decode()

        html = f'''
            <div id="etikett">
                <img src="data:image/png;base64,{img_data}" style="margin-top: 20px;"/>
                <p style="font-size:18px;">GTIN: {gtin}</p>
            </div>
            <button onclick="window.print()">Etikett drucken</button>
        '''
        st.markdown(html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
elif gtin:
    st.warning("Bitte mindestens 8 Ziffern eingeben.")
