import streamlit as st
import barcode
from barcode.writer import ImageWriter
from PIL import Image
import io
import base64

st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

st.title("**GTIN-Etikett drucken**")
st.markdown("Gib eine GTIN/EAN ein und drucke sofort dein Barcode-Etikett.")

# Textfeld
gtin = st.text_input("GTIN eingeben oder scannen:", max_chars=14)

# Wenn GTIN gültig ist
if gtin.isdigit() and 12 <= len(gtin) <= 14:
    # Barcode generieren
    barcode_class = barcode.get_barcode_class('ean13') if len(gtin) == 13 else barcode.get_barcode_class('ean14')
    buffer = io.BytesIO()
    barcode_class(gtin, writer=ImageWriter()).write(buffer)
    buffer.seek(0)

    # base64 kodieren
    base64_img = base64.b64encode(buffer.read()).decode()

    # Vorschau anzeigen
    st.image(f"data:image/png;base64,{base64_img}", caption=f"GTIN: {gtin}", use_column_width=False)

    # HTML und JS: neues Fenster mit Druck
    print_html = f"""
    <script>
        function printBarcode() {{
            var win = window.open("", "_blank");
            win.document.write(`
                <html>
                    <head><title>Etikett</title></head>
                    <body style="margin:0;padding:0;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;">
                        <img src="data:image/png;base64,{base64_img}" style="width:240px;height:auto;"/>
                        <p style="font-size:18px;margin:10px 0;">GTIN: {gtin}</p>
                        <script>window.onload = function() {{
                            window.print();
                            window.onafterprint = function() {{ window.close(); }};
                        }};<\/script>
                    </body>
                </html>
            `);
            win.document.close();
        }}
    </script>
    <button onclick="printBarcode()">Etikett drucken</button>
    """

    # Button anzeigen
    st.components.v1.html(print_html, height=100)

    # Hinweis für Leeren: (manuell nach Klick)
    st.caption("Das Feld leert sich nach dem nächsten Seiten-Neuladen oder Scan.")
