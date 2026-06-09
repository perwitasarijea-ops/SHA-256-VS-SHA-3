import hashlib
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def hitung_hash(file_path, algoritma):
    if algoritma == "sha256":
        hasher = hashlib.sha256()
    elif algoritma == "sha3_256":
        hasher = hashlib.sha3_256()
    else:
        raise ValueError("Algoritma tidak valid")

    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)
            if not data:
                break
            hasher.update(data)

    return hasher.hexdigest()


def hitung_avalanche(hash1, hash2):
    beda = 0

    for a, b in zip(hash1, hash2):
        if a != b:
            beda += 1

    persentase = (beda / len(hash1)) * 100
    return beda, persentase


def isi_text(widget, value):
    widget.config(state="normal")
    widget.delete("1.0", tk.END)
    widget.insert(tk.END, value)
    widget.config(state="disabled")


def pilih_file_asli():
    global file_asli
    file_asli = filedialog.askopenfilename(title="Pilih File Asli")

    if file_asli:
        label_file_asli.config(text=os.path.basename(file_asli))


def pilih_file_modifikasi():
    global file_modifikasi
    file_modifikasi = filedialog.askopenfilename(title="Pilih File Modifikasi")

    if file_modifikasi:
        label_file_modifikasi.config(text=os.path.basename(file_modifikasi))


def analisis_file():
    if not file_asli or not file_modifikasi:
        messagebox.showwarning(
            "Peringatan",
            "Pilih file asli dan file modifikasi terlebih dahulu."
        )
        return

    try:
        hash256_asli = hitung_hash(file_asli, "sha256")
        hash256_modif = hitung_hash(file_modifikasi, "sha256")

        hash3_asli = hitung_hash(file_asli, "sha3_256")
        hash3_modif = hitung_hash(file_modifikasi, "sha3_256")

        beda256, persen256 = hitung_avalanche(hash256_asli, hash256_modif)
        beda3, persen3 = hitung_avalanche(hash3_asli, hash3_modif)

        isi_text(text_sha256_asli, hash256_asli)
        isi_text(text_sha256_modif, hash256_modif)
        isi_text(text_sha3_asli, hash3_asli)
        isi_text(text_sha3_modif, hash3_modif)

        label_avalanche_sha256.config(
            text=f"{beda256} karakter berbeda | {persen256:.2f}%"
        )

        label_avalanche_sha3.config(
            text=f"{beda3} karakter berbeda | {persen3:.2f}%"
        )

        if hash256_asli == hash256_modif and hash3_asli == hash3_modif:
            label_hasil.config(
                text="Integritas file tetap. File asli dan file modifikasi identik.",
                fg="#16A34A"
            )
        else:
            label_hasil.config(
                text="Integritas file berubah. Terdapat perubahan pada file.",
                fg="#DC2626"
            )

    except Exception as e:
        messagebox.showerror("Error", str(e))


file_asli = ""
file_modifikasi = ""

root = tk.Tk()
root.title("Integrity and Avalanche Analysis")
root.geometry("1100x720")
root.configure(bg="#F8FAFC")
root.resizable(True, True)


# =========================
# SCROLL AREA
# =========================
canvas = tk.Canvas(root, bg="#F8FAFC", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg="#F8FAFC")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas_window = canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw"
)

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


def resize_frame(event):
    canvas.itemconfig(canvas_window, width=event.width)


canvas.bind("<Configure>", resize_frame)


def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


canvas.bind_all("<MouseWheel>", on_mousewheel)


# =========================
# HEADER
# =========================
header = tk.Frame(scrollable_frame, bg="#0F172A", height=100)
header.pack(fill="x")

judul = tk.Label(
    header,
    text="File Integrity & Avalanche Effect Analysis",
    font=("Segoe UI", 23, "bold"),
    bg="#0F172A",
    fg="white"
)
judul.pack(pady=(22, 2))

subjudul = tk.Label(
    header,
    text="SHA-256 and SHA3-256 Comparison",
    font=("Segoe UI", 11),
    bg="#0F172A",
    fg="#CBD5E1"
)
subjudul.pack()


# =========================
# MAIN CONTAINER
# =========================
container = tk.Frame(scrollable_frame, bg="#F8FAFC")
container.pack(fill="both", expand=True, padx=40, pady=25)


# =========================
# FILE SELECTION CARD
# =========================
file_card = tk.Frame(
    container,
    bg="white",
    highlightbackground="#E2E8F0",
    highlightthickness=1
)
file_card.pack(fill="x", pady=(0, 20))

file_title = tk.Label(
    file_card,
    text="File Selection",
    font=("Segoe UI", 13, "bold"),
    bg="white",
    fg="#0F172A"
)
file_title.pack(anchor="w", padx=20, pady=(15, 10))

button_frame = tk.Frame(file_card, bg="white")
button_frame.pack(fill="x", padx=20, pady=(0, 15))

btn_asli = tk.Button(
    button_frame,
    text="Select Original File",
    font=("Segoe UI", 10, "bold"),
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    relief="flat",
    padx=20,
    pady=9,
    command=pilih_file_asli
)
btn_asli.pack(side="left")

label_file_asli = tk.Label(
    button_frame,
    text="-",
    font=("Segoe UI", 10),
    bg="white",
    fg="#334155"
)
label_file_asli.pack(side="left", padx=15)

btn_modif = tk.Button(
    button_frame,
    text="Select Modified File",
    font=("Segoe UI", 10, "bold"),
    bg="#334155",
    fg="white",
    activebackground="#1E293B",
    activeforeground="white",
    relief="flat",
    padx=20,
    pady=9,
    command=pilih_file_modifikasi
)
btn_modif.pack(side="left", padx=(35, 0))

label_file_modifikasi = tk.Label(
    button_frame,
    text="-",
    font=("Segoe UI", 10),
    bg="white",
    fg="#334155"
)
label_file_modifikasi.pack(side="left", padx=15)

btn_analisis = tk.Button(
    file_card,
    text="Run Analysis",
    font=("Segoe UI", 11, "bold"),
    bg="#16A34A",
    fg="white",
    activebackground="#15803D",
    activeforeground="white",
    relief="flat",
    padx=25,
    pady=10,
    command=analisis_file
)
btn_analisis.pack(anchor="w", padx=20, pady=(0, 18))


# =========================
# RESULT HASH CARDS
# =========================
compare_frame = tk.Frame(container, bg="#F8FAFC")
compare_frame.pack(fill="both", expand=True)


def buat_card(parent, title):
    frame = tk.Frame(
        parent,
        bg="white",
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )
    frame.pack(side="left", fill="both", expand=True, padx=10)

    title_label = tk.Label(
        frame,
        text=title,
        font=("Segoe UI", 15, "bold"),
        bg="white",
        fg="#0F172A"
    )
    title_label.pack(anchor="w", padx=20, pady=(16, 10))

    label_asli = tk.Label(
        frame,
        text="Original File Hash",
        font=("Segoe UI", 9, "bold"),
        bg="white",
        fg="#64748B"
    )
    label_asli.pack(anchor="w", padx=20)

    text_asli = tk.Text(
        frame,
        height=4,
        wrap="word",
        font=("Consolas", 9),
        bg="#F8FAFC",
        fg="#0F172A",
        relief="flat",
        padx=10,
        pady=8
    )
    text_asli.pack(fill="x", padx=20, pady=(5, 12))
    text_asli.insert(tk.END, "Hash result will appear here.")
    text_asli.config(state="disabled")

    label_modif = tk.Label(
        frame,
        text="Modified File Hash",
        font=("Segoe UI", 9, "bold"),
        bg="white",
        fg="#64748B"
    )
    label_modif.pack(anchor="w", padx=20)

    text_modif = tk.Text(
        frame,
        height=4,
        wrap="word",
        font=("Consolas", 9),
        bg="#F8FAFC",
        fg="#0F172A",
        relief="flat",
        padx=10,
        pady=8
    )
    text_modif.pack(fill="x", padx=20, pady=(5, 12))
    text_modif.insert(tk.END, "Hash result will appear here.")
    text_modif.config(state="disabled")

    avalanche_title = tk.Label(
        frame,
        text="Avalanche Effect",
        font=("Segoe UI", 9, "bold"),
        bg="white",
        fg="#64748B"
    )
    avalanche_title.pack(anchor="w", padx=20)

    avalanche_label = tk.Label(
        frame,
        text="-",
        font=("Segoe UI", 12, "bold"),
        bg="white",
        fg="#2563EB"
    )
    avalanche_label.pack(anchor="w", padx=20, pady=(0, 18))

    return text_asli, text_modif, avalanche_label


text_sha256_asli, text_sha256_modif, label_avalanche_sha256 = buat_card(
    compare_frame,
    "SHA-256"
)

text_sha3_asli, text_sha3_modif, label_avalanche_sha3 = buat_card(
    compare_frame,
    "SHA3-256"
)


# =========================
# FINAL RESULT CARD
# =========================
result_card = tk.Frame(
    container,
    bg="white",
    highlightbackground="#E2E8F0",
    highlightthickness=1
)
result_card.pack(fill="x", pady=(20, 40))

result_title = tk.Label(
    result_card,
    text="Integrity Result",
    font=("Segoe UI", 12, "bold"),
    bg="white",
    fg="#0F172A"
)
result_title.pack(anchor="w", padx=20, pady=(14, 5))

label_hasil = tk.Label(
    result_card,
    text="Please select original and modified files to start the analysis.",
    font=("Segoe UI", 11),
    bg="white",
    fg="#64748B"
)
label_hasil.pack(anchor="w", padx=20, pady=(0, 15))


root.mainloop()