import tkinter as tk
from tkinter import messagebox
import subprocess

# Druckfunktion
def drucke_etk():
    gtin = entry.get().strip()
    if not gtin:
        messagebox.showwarning("Fehler", "Bitte GTIN eingeben oder scannen.")
        return

    zpl = f"""
^XA
^FO50,50^BY2
^BCN,100,Y,N,N
^FD{gtin}^FS
^FO50,170^ADN,36,20^FD{gtin}^FS
^XZ
"""
    try:
        with open("/tmp/etikett.zpl", "w") as f:
            f.write(zpl)

        # Druckername hier anpassen!
        subprocess.run(["lp", "-d", "DEIN_DRUCKERNAME", "/tmp/etikett.zpl"])
        messagebox.showinfo("Erfolg", f"Etikett für {gtin} gedruckt.")
        entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Fehler", str(e))

# GUI-Fenster
root = tk.Tk()
root.title("GTIN Drucker")
root.geometry("300x150")

tk.Label(root, text="GTIN eingeben oder scannen:").pack(pady=10)
entry = tk.Entry(root, font=("Arial", 14), justify="center")
entry.pack(pady=5)
entry.focus()

tk.Button(root, text="Etikett drucken", command=drucke_etk).pack(pady=10)

root.mainloop()
