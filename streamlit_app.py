import streamlit as st
import barcode
from barcode.writer import ImageWriter
import io
import base64

# Seiteneinstellungen
st.set_page_config(page_title="GTIN Etikett drucken", layout="centered")

st.title("🖨️ GTIN-Etikett drucken")
st.caption("Gib eine GTIN/EAN ein und drucke direkt aus dem Browser – ohne PDF, ohne neue Seite.")

# GTIN Eingabefeld
gtin = st.text_input("GTIN eingeben oder scannen:", max_chars=14)

# Wenn GTIN eingegeben wurde
if gtin and len(gtin) >= 8:
    try:
        # Barcode generieren
        ean = barcode.get("ean13", gtin.zfill(13), writer=ImageWriter())
        buffer = io.BytesIO()
        ean.write(buffer, options={"module_height": 15.0, "font_size": 10})
        buffer.seek(0)
        img_data = buffer.getvalue()
        img_base64 = base64.b64encode(img_data).decode("utf-8")

        # Barcode-Bild anzeigen
        st.image(img_data, caption=f"GTIN: {gtin}", use_column_width=False)

        # HTML/JS Button zum direkten Druck
        print_button = f'''
        <script>
        function printImage() {{
            const win = window.open();
            win.document.write('<html><head><title>Etikett drucken</title></head><body style="margin:0;text-align:center;">');
            win.document.write('<img src="data:image/png;base64,{img_base64}" style="width:100%;margin-top:20px;" onload="window.print();window.close();" />');
            win.document.write('</body></html>');
            win.document.close();
        }}
        </script>
        <button onclick="printImage()">🖨️ Etikett drucken</button>
        '''

        # Button einfügen
        st.markdown(print_button, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")

elif gtin:
    st.warning("Bitte mindestens 8 Ziffern eingeben.")
