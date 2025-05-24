import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64

st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

st.markdown("<h1 style='text-align: center;'>Nando´s & Samer´s Toolbox</h1>", unsafe_allow_html=True)

# Eingabe-Feld mit Submit-Form, damit Enter funktioniert
with st.form("barcode_form", clear_on_submit=False):
    gtin = st.text_input("GTIN eingeben oder scannen:", key="gtin_input")
    submitted = st.form_submit_button("🖨️ Etikett drucken")

# Barcode generieren, wenn gesendet
if submitted and gtin and len(gtin) in [8, 12, 13, 14]:
    try:
        ean = barcode.get('ean13', gtin.zfill(13), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer, {
            "write_text": True,
            "module_height": 15,
            "module_width": 0.4
        })

        # Vorschau anzeigen
        st.image(buffer.getvalue(), caption=f"GTIN: {gtin}", use_container_width=True)

        # Druck-HTML generieren
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        html_code = f"""
        <html>
        <head>
            <title>Etikett</title>
            <style>
                @media print {{
                    @page {{ size: 60mm 30mm; margin: 0; }}
                    body {{ margin: 0; }}
                }}
                body {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    font-family: Arial;
                }}
                img {{ max-height: 80%; }}
                div {{ margin-top: 10px; }}
            </style>
        </head>
        <body onload="window.print()">
            <img src="data:image/png;base64,{img_base64}" />
            <div>GTIN: {gtin}</div>
        </body>
        </html>
        """
        html_b64 = base64.b64encode(html_code.encode()).decode()
        print_link = f'<script>window.open("data:text/html;base64,{html_b64}", "_blank")</script>'
        st.components.v1.html(print_link, height=0)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")

# Reset-Button
if st.button("🔁 Reset Eingabe"):
    st.session_state.gtin_input = ""
    st.rerun()
