import streamlit as st
import barcode
from barcode.writer import ImageWriter
import io
import base64
from PIL import Image

st.set_page_config(page_title="GTIN Etikett PNG", layout="centered")

st.title("🖼️ GTIN-Etikett als PNG")
st.caption("Gib eine GTIN ein, zeige den Barcode an und lade ihn als PNG herunter – direkt druckbar aus dem Bildfenster.")

gtin = st.text_input("GTIN eingeben oder scannen:", max_chars=14)

if gtin and len(gtin) >= 8:
    try:
        # Barcode generieren
        ean = barcode.get("ean13", gtin.zfill(13), writer=ImageWriter())
        buffer = io.BytesIO()
        ean.write(buffer, options={"module_height": 15.0, "font_size": 10})
        buffer.seek(0)
        img = Image.open(buffer)

        # Barcode anzeigen
        st.image(img, caption=f"GTIN: {gtin}", use_column_width=False)

        # PNG herunterladen
        st.download_button(
            label="📥 PNG herunterladen",
            data=buffer,
            file_name=f"etikett_{gtin}.png",
            mime="image/png"
        )

        # Öffnen in neuem Tab zum direkten Drucken
        b64 = base64.b64encode(buffer.getvalue()).decode()
        link = f"<a href='data:image/png;base64,{b64}' target='_blank'>🔗 Öffnen in neuem Tab zum Drucken</a>"
        st.markdown(link, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
elif gtin:
    st.warning("Bitte mindestens 8 Ziffern eingeben.")
