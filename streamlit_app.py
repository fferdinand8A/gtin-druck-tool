import streamlit as st
import barcode
from barcode.writer import ImageWriter
import io
import base64

st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")
st.title("🖨️ GTIN-Etikett drucken")
st.caption("Gib eine GTIN/EAN ein und drucke direkt aus dem Browser.")

gtin = st.text_input("GTIN eingeben oder scannen:", max_chars=14)

if gtin and len(gtin) >= 8:
    try:
        ean = barcode.get("ean13", gtin.zfill(13), writer=ImageWriter())
        buffer = io.BytesIO()
        ean.write(buffer, options={"module_height": 15.0, "font_size": 10})
        buffer.seek(0)
        img_data = buffer.getvalue()
        img_base64 = base64.b64encode(img_data).decode("utf-8")

        st.image(img_data, caption=f"GTIN: {gtin}", use_column_width=False)

        # Druckknopf mit eingebettetem PNG
        st.markdown(f"""
        <script>
        function printImage() {{
            const w = window.open();
            w.document.write('<img src="data:image/png;base64,{img_base64}" onload="window.print();window.close();" style="margin:0;max-width:100%;"/>');
            w.document.close();
        }}
        </script>
        <button onclick="printImage()">🖨️ Etikett drucken</button>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
