import streamlit as st
import barcode
from barcode.writer import ImageWriter
from PIL import Image
import io
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="GTIN Etikett", layout="centered")

# Drucklayout für 60x30 mm Etikett
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
        }
        #etikett img {
            max-width: 100%;
            height: auto;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📦 GTIN-Etikett drucken")
st.caption("Gib eine GTIN/EAN ein und drucke sofort dein Barcode-Etikett.")

gtin = st.text_input("GTIN eingeben oder scannen:", max_chars=14)

if gtin and len(gtin) >= 8:
    try:
        # Barcode generieren
        ean = barcode.get("ean13", gtin.zfill(13), writer=ImageWriter())
        buffer = io.BytesIO()
        ean.write(buffer, options={"module_height": 15.0, "font_size": 10})
        buffer.seek(0)
        img_data = base64.b64encode(buffer.getvalue()).decode()

        # Etikett-HTML anzeigen
        etikett_html = f"""
            <div id='etikett'>
                <img src='data:image/png;base64,{img_data}' />
                <p style='font-size:14px;'>GTIN: {gtin}</p>
            </div>
        """
        st.markdown(etikett_html, unsafe_allow_html=True)

        # Funktionierender Button mit JS-Druck
        if st.button("Etikett drucken"):
            components.html("<script>window.print()</script>", height=0)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
elif gtin:
    st.warning("Bitte mindestens 8 Ziffern eingeben.")
