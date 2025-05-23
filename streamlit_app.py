import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64

st.set_page_config(page_title="GTIN-Etikett drucken")

st.title("🧾 GTIN-Etikett drucken")
st.markdown("Gib eine GTIN/EAN ein und drucke dein Barcode-Etikett im Browser.")

gtin = st.text_input("GTIN eingeben oder scannen:")

if gtin and len(gtin) in [8, 12, 13, 14]:
    try:
        # Barcode erzeugen
        ean = barcode.get('ean13', gtin.zfill(13), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        b64 = base64.b64encode(buffer.getvalue()).decode()

        # HTML für neue Druckseite erzeugen
        html = f"""
        <html>
        <head>
            <title>Etikett drucken</title>
            <style>
                body {{ margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }}
                img {{ width: 180px; }}
            </style>
        </head>
        <body onload="window.print()">
            <div>
                <img src="data:image/png;base64,{b64}" alt="Barcode" />
                <p style="text-align:center;">GTIN: {gtin}</p>
            </div>
        </body>
        </html>
        """

        # Als Base64-HTML-Data-URL
        encoded_html = base64.b64encode(html.encode()).decode()
        data_url = f'data:text/html;base64,{encoded_html}'

        # Zeige Barcode und Druck-Button
        st.image(buffer.getvalue(), use_container_width=True)
        st.markdown(f"**GTIN:** {gtin}")
        st.markdown(f'<a href="{data_url}" target="_blank"><button>🖨️ Etikett drucken</button></a>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Fehler: {e}")
