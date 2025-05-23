import streamlit as st
import barcode
from barcode.writer import ImageWriter
from PIL import Image
import io

st.set_page_config(
    page_title="GTIN-Etikett drucken",
    page_icon="🖨️",
    layout="centered",
)

st.title("**GTIN-Etikett drucken**")
st.markdown("Gib eine GTIN/EAN ein und drucke sofort dein Barcode-Etikett.")

# Session state initialisieren
if "gtin" not in st.session_state:
    st.session_state.gtin = ""

# Eingabe
gtin_input = st.text_input("GTIN eingeben oder scannen:", value=st.session_state.gtin, max_chars=14)

# Nur rendern, wenn gültiger Input (12–14 Ziffern)
if gtin_input.isdigit() and 12 <= len(gtin_input) <= 14:
    st.session_state.gtin = gtin_input

    # Barcode generieren
    barcode_class = barcode.get_barcode_class('ean13') if len(gtin_input) == 13 else barcode.get_barcode_class('ean14')
    buffer = io.BytesIO()
    barcode_class(gtin_input, writer=ImageWriter()).write(buffer)
    buffer.seek(0)
    image = Image.open(buffer)

    # Barcode anzeigen
    st.image(image, caption=f"GTIN: {gtin_input}")

    # Drucken-Knopf
    js = f"""
    <script>
    function printBarcode() {{
        var w = window.open();
        w.document.write('<img src="{buffer.getvalue().decode("latin1")}" style="width:60mm;height:30mm;"><p style="font-size:14pt;text-align:center;">{gtin_input}</p>');
        w.document.close();
        w.focus();
        w.print();
        w.close();
        setTimeout(() => {{
            window.location.reload();
        }}, 1000);
    }}
    </script>
    <button onclick="printBarcode()">Etikett drucken</button>
    """
    st.components.v1.html(js, height=80)

    # GTIN-Feld zurücksetzen
    st.session_state.gtin = ""

elif gtin_input:
    st.error("Bitte gib eine gültige GTIN mit 12 bis 14 Ziffern ein.")
