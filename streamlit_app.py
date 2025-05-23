import streamlit as st
import barcode
from barcode.writer import ImageWriter
from fpdf import FPDF
import io
from PIL import Image

st.set_page_config(page_title="GTIN Etikett PDF", layout="centered")

st.title("📄 GTIN-Etikett als PDF herunterladen")
st.caption("Gib eine GTIN/EAN ein, lade das Etikett als PDF herunter und drucke es exakt im Format 60×30 mm.")

gtin = st.text_input("GTIN eingeben oder scannen:", max_chars=14)

if gtin and len(gtin) >= 8:
    try:
        # Barcode generieren
        ean = barcode.get("ean13", gtin.zfill(13), writer=ImageWriter())
        image_buffer = io.BytesIO()
        ean.write(image_buffer, options={"module_height": 15.0, "font_size": 10})
        image_buffer.seek(0)
        image = Image.open(image_buffer)

        # Temporäre PNG-Datei erzeugen
        temp_png = "/tmp/barcode.png"
        image.save(temp_png)

        # PDF mit exakter Etikettengröße erstellen (60×30 mm)
        pdf = FPDF(unit="mm", format=(60, 30))
        pdf.add_page()
        pdf.image(temp_png, x=5, y=5, w=50)
        pdf.set_font("Arial", size=10)
        pdf.set_y(27)
        pdf.cell(0, 10, f"GTIN: {gtin}", align="C")

        # PDF in BytesIO schreiben
        pdf_buffer = io.BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)

        # Download-Button anzeigen
        st.download_button(
            label="📥 PDF herunterladen",
            data=pdf_buffer,
            file_name=f"etikett_{gtin}.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")
elif gtin:
    st.warning("Bitte mindestens 8 Ziffern eingeben.")
