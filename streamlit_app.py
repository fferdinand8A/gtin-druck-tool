import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import streamlit.components.v1 as components

# Seiteneinstellungen
st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

# Überschrift
st.markdown("<h1 style='text-align: center;'>Nando´s & Samer´s Toolbox</h1>", unsafe_allow_html=True)

# Session State initialisieren
if "gtin_input" not in st.session_state:
    st.session_state["gtin_input"] = ""
if "printed" not in st.session_state:
    st.session_state["printed"] = False

# Reset-Funktion
def reset_input():
    st.session_state["gtin_input"] = ""
    st.session_state["printed"] = False

# Eingabe
gtin = st.text_input("GTIN eingeben oder scannen:", key="gtin_input")

# Wenn gültige GTIN und noch nicht gedruckt
if gtin and len(gtin) in [8, 12, 13, 14] and not st.session_state.printed:
    try:
        # Barcode generieren
        ean = barcode.get('ean13', gtin.zfill(13), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer, {
            "write_text": True,
            "module_height": 20,
            "module_width": 0.4
        })
        barcode_b64 = base64.b64encode(buffer.getvalue()).decode()

        # HTML mit Druckfunktion
        html = f"""
        <html>
        <head>
        <style>
            @media print {{
                @page {{
                    size: 60mm 30mm;
                    margin: 0;
                }}
                body {{
                    margin: 0;
                }}
            }}
            body {{
                width: 60mm;
                height: 30mm;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
                font-size: 10pt;
            }}
            img {{
                max-height: 20mm;
            }}
        </style>
        <script>
            window.onload = function() {{
                window.print();
                fetch("/", {{method: "POST"}});  // Triggert Streamlit zum Reset
            }};
        </script>
        </head>
        <body>
            <img src="data:image/png;base64,{barcode_b64}" alt="GTIN Barcode">
            <div>GTIN: {gtin}</div>
        </body>
        </html>
        """

        # Barcode anzeigen und Druck auslösen
        components.html(html, height=400)
        st.session_state.printed = True

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")

# Wenn bereits gedruckt → zurücksetzen
elif st.session_state.printed:
    reset_input()

# Reset Button manuell
st.markdown("<br><br>", unsafe_allow_html=True)
st.button("🔄 Reset Eingabe", on_click=reset_input)
