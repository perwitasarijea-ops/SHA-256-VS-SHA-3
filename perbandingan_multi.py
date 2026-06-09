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


def pilih_file():
    file_paths = filedialog.askopenfilenames(
        title="Pilih Banyak File",
        filetypes=[
            ("Semua File", "*.*"),
            ("Dokumen", "*.pdf *.docx *.xlsx *.pptx *.txt"),
            ("Gambar", "*.jpg *.jpeg *.png *.svg")
        ]
    )

    if not file_paths:
        return

    text_hasil.config(state="normal")
    text_hasil.delete("1.0", tk.END)

    total_file = len(file_paths)

    for nomor, file_path in enumerate(file_paths, start=1):
        try:
            hash_sha256, waktu_sha256 = hitung_hash(file_path, "sha256")
            hash_sha3, waktu_sha3 = hitung_hash(file_path, "sha3_256")

            ukuran_kb = os.path.getsize(file_path) / 1024
            ukuran_mb = ukuran_kb / 1024

            if waktu_sha256 < waktu_sha3:
                selisih = waktu_sha3 - waktu_sha256
                hasil = f"SHA-256 lebih cepat sebesar {selisih:.8f} detik"
            elif waktu_sha3 < waktu_sha256:
                selisih = waktu_sha256 - waktu_sha3
                hasil = f"SHA3-256 lebih cepat sebesar {selisih:.8f} detik"
            else:
                hasil = "SHA-256 dan SHA3-256 memiliki waktu yang sama"

            text_hasil.insert(tk.END, f"FILE {nomor}\n")
            text_hasil.insert(tk.END, f"Nama File      : {os.path.basename(file_path)}\n")
            text_hasil.insert(tk.END, f"Ukuran File    : {ukuran_kb:.2f} KB / {ukuran_mb:.4f} MB\n\n")

            text_hasil.insert(tk.END, "SHA-256\n")
            text_hasil.insert(tk.END, f"Waktu          : {waktu_sha256:.8f} detik\n")
            text_hasil.insert(tk.END, f"Hash           : {hash_sha256}\n\n")

            text_hasil.insert(tk.END, "SHA3-256\n")
            text_hasil.insert(tk.END, f"Waktu          : {waktu_sha3:.8f} detik\n")
            text_hasil.insert(tk.END, f"Hash           : {hash_sha3}\n\n")

            text_hasil.insert(tk.END, f"Hasil          : {hasil}\n")
            text_hasil.insert(tk.END, "-" * 90 + "\n\n")

        except Exception as e:
            text_hasil.insert(tk.END, f"Error pada file {file_path}: {e}\n\n")

    text_hasil.config(state="disabled")
    label_hasil.config(
        text=f"Berhasil menganalisis {total_file} file.",
        fg="#16A34A"
    )


root = tk.Tk()
root.title("SHA-256 vs SHA3-256 Multiple File Comparison")
root.geometry("1050x720")
root.minsize(900, 600)
root.configure(bg="#F8FAFC")
root.resizable(True, True)


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
    text="Multiple File Integrity Verification and Performance Analysis",
    font=("Segoe UI", 11),
    bg="#0F172A",
    fg="#CBD5E1"
)
subjudul.pack()


container = tk.Frame(scrollable_frame, bg="#F8FAFC")
container.pack(fill="both", expand=True, padx=40, pady=25)


btn_pilih = tk.Button(
    container,
    text="Select Multiple Files",
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


result_card = tk.Frame(
    container,
    bg="white",
    highlightbackground="#E2E8F0",
    highlightthickness=1
)
result_card.pack(fill="both", expand=True, pady=(0, 20))

result_title = tk.Label(
    result_card,
    text="Multiple File Hash Results",
    font=("Segoe UI", 13, "bold"),
    bg="white",
    fg="#0F172A"
)
result_title.pack(anchor="w", padx=20, pady=(15, 5))

text_hasil = tk.Text(
    result_card,
    height=28,
    wrap="word",
    font=("Consolas", 9),
    bg="#F8FAFC",
    fg="#0F172A",
    relief="flat",
    padx=15,
    pady=15
)
text_hasil.pack(fill="both", expand=True, padx=20, pady=(5, 20))
text_hasil.insert(tk.END, "Hasil hash banyak file akan muncul di sini.")
text_hasil.config(state="disabled")


label_hasil = tk.Label(
    container,
    text="Please select files to start the analysis.",
    font=("Segoe UI", 11),
    bg="#F8FAFC",
    fg="#64748B",
    wraplength=900,
    justify="left"
)
label_hasil.pack(anchor="w", pady=(0, 20))


root.mainloop()