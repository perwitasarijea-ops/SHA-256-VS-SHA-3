import hashlib
import time
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

    mulai = time.perf_counter()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            hasher.update(data)

    selesai = time.perf_counter()

    return hasher.hexdigest(), selesai - mulai


def isi_text(widget, value):
    widget.config(state="normal")
    widget.delete("1.0", tk.END)
    widget.insert(tk.END, value)
    widget.config(state="disabled")


def pilih_file():
    file_path = filedialog.askopenfilename(
        title="Pilih File",
        filetypes=[
            ("Semua File", "*.*"),
            ("Dokumen", "*.pdf *.docx *.xlsx *.pptx *.txt"),
            ("Gambar", "*.jpg *.jpeg *.png *.svg")
        ]
    )

    if not file_path:
        return

    try:
        hash_sha256, waktu_sha256 = hitung_hash(file_path, "sha256")
        hash_sha3, waktu_sha3 = hitung_hash(file_path, "sha3_256")

        ukuran_kb = os.path.getsize(file_path) / 1024
        ukuran_mb = ukuran_kb / 1024

        label_file.config(text=os.path.basename(file_path))
        label_ukuran.config(text=f"{ukuran_kb:.2f} KB / {ukuran_mb:.4f} MB")

        label_waktu_sha256.config(text=f"{waktu_sha256:.8f} detik")
        label_waktu_sha3.config(text=f"{waktu_sha3:.8f} detik")

        isi_text(text_sha256, hash_sha256)
        isi_text(text_sha3, hash_sha3)

        if waktu_sha256 < waktu_sha3:
            selisih = waktu_sha3 - waktu_sha256
            hasil = f"SHA-256 lebih cepat sebesar {selisih:.8f} detik"
        elif waktu_sha3 < waktu_sha256:
            selisih = waktu_sha256 - waktu_sha3
            hasil = f"SHA3-256 lebih cepat sebesar {selisih:.8f} detik"
        else:
            hasil = "SHA-256 dan SHA3-256 memiliki waktu yang sama"

        label_hasil.config(text=hasil, fg="#16A34A")

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("SHA-256 vs SHA3-256 Comparison")
root.geometry("1050x720")
root.minsize(900, 600)
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
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas_window = canvas.create_window(
    (0, 0),
    window=scrollable_frame,
    anchor="nw"
)

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


def resize_scrollable_frame(event):
    canvas.itemconfig(canvas_window, width=event.width)


canvas.bind("<Configure>", resize_scrollable_frame)


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
    text="SHA-256 vs SHA3-256 Comparison",
    font=("Segoe UI", 24, "bold"),
    bg="#0F172A",
    fg="white"
)
judul.pack(pady=(22, 2))

subjudul = tk.Label(
    header,
    text="File Integrity Verification and Performance Analysis",
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
# BUTTON
# =========================
btn_pilih = tk.Button(
    container,
    text="Select File",
    font=("Segoe UI", 11, "bold"),
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    relief="flat",
    padx=30,
    pady=10,
    command=pilih_file
)
btn_pilih.pack(pady=(0, 20))


# =========================
# FILE INFO CARD
# =========================
info_card = tk.Frame(
    container,
    bg="white",
    highlightbackground="#E2E8F0",
    highlightthickness=1
)
info_card.pack(fill="x", pady=(0, 20))

info_title = tk.Label(
    info_card,
    text="File Information",
    font=("Segoe UI", 13, "bold"),
    bg="white",
    fg="#0F172A"
)
info_title.pack(anchor="w", padx=20, pady=(15, 5))

label_file_title = tk.Label(
    info_card,
    text="File Name",
    font=("Segoe UI", 9, "bold"),
    bg="white",
    fg="#64748B"
)
label_file_title.pack(anchor="w", padx=20)

label_file = tk.Label(
    info_card,
    text="-",
    font=("Segoe UI", 11),
    bg="white",
    fg="#0F172A",
    wraplength=850,
    justify="left"
)
label_file.pack(anchor="w", padx=20, pady=(0, 10))

label_ukuran_title = tk.Label(
    info_card,
    text="File Size",
    font=("Segoe UI", 9, "bold"),
    bg="white",
    fg="#64748B"
)
label_ukuran_title.pack(anchor="w", padx=20)

label_ukuran = tk.Label(
    info_card,
    text="-",
    font=("Segoe UI", 11),
    bg="white",
    fg="#0F172A"
)
label_ukuran.pack(anchor="w", padx=20, pady=(0, 15))


# =========================
# COMPARISON FRAME
# =========================
compare_frame = tk.Frame(container, bg="#F8FAFC")
compare_frame.pack(fill="both", expand=True)


def buat_hash_card(parent, title):
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
    title_label.pack(anchor="w", padx=20, pady=(18, 8))

    time_title = tk.Label(
        frame,
        text="Computation Time",
        font=("Segoe UI", 9, "bold"),
        bg="white",
        fg="#64748B"
    )
    time_title.pack(anchor="w", padx=20)

    time_label = tk.Label(
        frame,
        text="-",
        font=("Segoe UI", 12, "bold"),
        bg="white",
        fg="#2563EB"
    )
    time_label.pack(anchor="w", padx=20, pady=(0, 15))

    hash_title = tk.Label(
        frame,
        text="Hash Result",
        font=("Segoe UI", 9, "bold"),
        bg="white",
        fg="#64748B"
    )
    hash_title.pack(anchor="w", padx=20)

    hash_text = tk.Text(
        frame,
        height=7,
        wrap="word",
        font=("Consolas", 9),
        bg="#F8FAFC",
        fg="#0F172A",
        relief="flat",
        padx=10,
        pady=10
    )
    hash_text.pack(fill="x", padx=20, pady=(5, 18))
    hash_text.insert(tk.END, "Hash result will appear here.")
    hash_text.config(state="disabled")

    return time_label, hash_text


label_waktu_sha256, text_sha256 = buat_hash_card(compare_frame, "SHA-256")
label_waktu_sha3, text_sha3 = buat_hash_card(compare_frame, "SHA3-256")


# =========================
# RESULT CARD
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
    text="Comparison Result",
    font=("Segoe UI", 12, "bold"),
    bg="white",
    fg="#0F172A"
)
result_title.pack(anchor="w", padx=20, pady=(14, 5))

label_hasil = tk.Label(
    result_card,
    text="Please select a file to start the analysis.",
    font=("Segoe UI", 11),
    bg="white",
    fg="#64748B",
    wraplength=900,
    justify="left"
)
label_hasil.pack(anchor="w", padx=20, pady=(0, 15))


root.mainloop()