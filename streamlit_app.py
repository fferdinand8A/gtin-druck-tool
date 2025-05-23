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
                top: 0;
                left: 0;
                width: 60mm;
                height: 30mm;
                padding: 5mm;
                text-align: center;
            }
            html, body {
                margin: 0;
                padding: 0;
            }
        }
        #etikett img {
            max-width: 100%;
            height: auto;
        }
        .druck-button {
            margin-top: 20px;
            padding: 8px 16px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📦 GTIN-Etikett drucken")
st.caption("Gib eine GTIN/EAN ein und drucke sofort dein Barcode-Etikett.")

gtin = st.text_input("GTIN eingeben oder scannen:", max_chars=14)

if gtin and len(gtin) >= 8:
    try:
        ean = barcode.get("ean13", gtin.zfill(13), writer=ImageWriter())
        buffer = io.BytesIO()
        ean.write(buffer, options={"module_height": 15.0, "font_size": 10})
        buffer.seek(0)
        img_data = base64.b64encode(buffer.getvalue()).decode()

        etikett_html = f"""
            <div id='etikett'>
                <img src='data:image/png;base64,{img_data}' />
                <p style='font-size:14px;'>GTIN: {gtin}</p>
            </div>
            <button class='druck-button' onclick='window.print()'>Etikett drucken</button>
        """
        st.markdown(etikett_html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
elif gtin:
    st.warning("Bitte mindestens 8 Ziffern eingeben.")
