import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import streamlit.components.v1 as components

st.set_page_config(page_title="GTIN-Etikett drucken")

st.title("🧾 GTIN-Etikett drucken")
st.markdown("Gib eine GTIN/EAN ein und drucke direkt im Browser (60×30 mm Etikett).")

gtin = st.text_input("GTIN eingeben oder scannen:")

if gtin and len(gtin) in [8, 12, 13, 14]:
    try:
        # Barcode als PNG erzeugen
        ean = barcode.get('ean13', gtin.zfill(13), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        img_b64 = base64.b64encode(buffer.getvalue()).decode()

        # HTML mit eingebettetem Barcode und Druck-Button
        html = f"""
        <div style="text-align: center; margin-top: 2rem;">
            <img src="data:image/png;base64,{img_b64}" width="200"><br>
            <p style="margin: 0;">GTIN: {gtin}</p><br>
            <button onclick="window.print()" style="padding: 10px 20px; font-size: 16px;">🖨️ Etikett drucken</button>
        </div>
        """

        components.html(html, height=400)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
