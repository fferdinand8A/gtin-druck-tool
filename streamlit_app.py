import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
from PIL import Image

st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

st.title("🧾 GTIN-Etikett drucken")
st.markdown("Gib eine GTIN/EAN ein und drucke sofort das Etikett als Barcode – direkt im Browser.")

# Eingabefeld
gtin = st.text_input("GTIN eingeben oder scannen:", max_chars=14)

if gtin and len(gtin) in [8, 12, 13, 14] and gtin.isdigit():
    try:
        # Barcode generieren
        buffer = BytesIO()
        ean = barcode.get("ean13", gtin.zfill(13), writer=ImageWriter())
        ean.write(buffer)
        buffer.seek(0)

        # Bild in base64 konvertieren
        img_base64 = base64.b64encode(buffer.read()).decode()

        # Barcode anzeigen
        st.image(f"data:image/png;base64,{img_base64}", use_column_width=False)
        st.markdown(f"**GTIN:** {gtin}")

        # JS-Druckfunktion
        st.markdown(f"""
        <script>
        function printEtikett() {{
            const w = window.open();
            w.document.write(`<img src="data:image/png;base64,{img_base64}" onload="window.print(); window.close();" />`);
            w.document.close();
        }}
        </script>
        <button onclick="printEtikett()">🖨️ Etikett drucken</button>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
elif gtin:
    st.warning("Bitte eine gültige GTIN/EAN mit 8, 12, 13 oder 14 Ziffern eingeben.")
