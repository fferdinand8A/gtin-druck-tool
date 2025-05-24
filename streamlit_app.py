import streamlit as st
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64

# Seiteneinstellungen
st.set_page_config(page_title="GTIN-Etikett drucken", layout="centered")

# Titel
st.markdown("<h1 style='text-align: center;'>Nando´s & Samer´s Toolbox</h1>", unsafe_allow_html=True)

# Initialisiere SessionState für Reset-Logik
if "gtin_input" not in st.session_state:
    st.session_state.gtin_input = ""

# Eingabefeld
gtin = st.text_input("GTIN eingeben oder scannen:", value=st.session_state.gtin_input, key="gtin_input")

# Barcode anzeigen & Druckfenster auslösen
if gtin and len(gtin) in [8, 12, 13, 14]:
    try:
        # Barcode generieren
        ean = barcode.get('ean13', gtin.zfill(13), writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer, {
            "write_text": False,
            "module_height": 20,
            "module_width": 0.4
        })
        barcode_b64 = base64.b64encode(buffer.getvalue()).decode()

        # Druckbare HTML-Seite erzeugen
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
        </head>
        <body onload="window.print()">
            <img src="data:image/png;base64,{barcode_b64}" alt="GTIN Barcode">
            <div>GTIN: {gtin}</div>
        </body>
        </html>
        """

        # In neuem Tab öffnen
        js = f"""
        <script>
            const newWindow = window.open("", "_blank");
            newWindow.document.write(`{html}`);
            newWindow.document.close();
        </script>
        """
        st.components.v1.html(js, height=0)

        # Vorschau in App anzeigen
        st.image(buffer.getvalue(), caption=f"GTIN: {gtin}", use_column_width=False)

    except Exception as e:
        st.error(f"Fehler beim Erzeugen des Barcodes: {e}")

# 🧼 Reset Button
st.markdown("""
    <div style='display: flex; justify-content: center; margin-top: 40px;'>
        <form action="" method="post">
            <button style='
                background-color: #f0f2f6;
                border: 1px solid #d0d0d0;
                padding: 0.5em 1em;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
            ' type="submit" name="reset">🔄 Reset Eingabe</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# Logik: Reset Eingabe
if st.session_state.get("reset_triggered"):
    st.session_state.gtin_input = ""
    st.session_state.reset_triggered = False

# Formulareingabe simulieren
if "reset" in st.experimental_get_query_params():
    st.session_state.reset_triggered = True
    st.experimental_set_query_params()
    st.rerun()
