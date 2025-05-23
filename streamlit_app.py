
import streamlit as st
import barcode
from barcode.writer import ImageWriter
from PIL import Image
import io

st.set_page_config(page_title="GTIN Etikettendruck", layout="centered")

st.title("📦 GTIN-Etikett drucken")
st.write("Gib eine GTIN/EAN ein und drucke sofort dein Barcode-Etikett.")

gtin = st.text_input("GTIN eingeben oder scannen:", max_chars=14)

if gtin and len(gtin) >= 8:
    try:
        ean = barcode.get("ean13", gtin.zfill(13), writer=ImageWriter())
        buffer = io.BytesIO()
        ean.write(buffer, options={"module_height": 15.0, "font_size": 10})
        buffer.seek(0)
        image = Image.open(buffer)

        st.image(image, caption=f"GTIN: {gtin}", use_column_width=True)

        # Browserdruck-Tipp
        st.markdown(
            "<p style='color:gray;'>Drücke <b>Strg+P</b> oder <b>Cmd+P</b>, um direkt zu drucken.</p>",
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
elif gtin:
    st.warning("Bitte mindestens 8 Ziffern eingeben.")
