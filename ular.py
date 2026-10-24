"""Permainan ular sederhana menggunakan Tkinter (tanpa library tambahan)."""

import random
import tkinter as tk


UKURAN_KOTAK = 20
JUMLAH_KOTAK = 25
LEBAR = TINGGI = UKURAN_KOTAK * JUMLAH_KOTAK
KECEPATAN_MS = 115


class PermainanUlar:
    def __init__(self, root):
        self.root = root
        self.root.title("Permainan Ular")
        self.root.resizable(False, False)
        self.root.configure(bg="#111827")

        self.skor_label = tk.Label(
            root, text="Skor: 0", font=("Arial", 16, "bold"),
            fg="#f9fafb", bg="#111827", pady=12,
        )
        self.skor_label.pack()

        self.canvas = tk.Canvas(
            root, width=LEBAR, height=TINGGI,
            bg="#1f2937", highlightthickness=0,
        )
        self.canvas.pack(padx=14)

        self.petunjuk = tk.Label(
            root, text="Panah / WASD untuk bergerak  •  Spasi untuk mulai ulang",
            font=("Arial", 10), fg="#9ca3af", bg="#111827", pady=12,
        )
        self.petunjuk.pack()

        self.root.bind("<KeyPress>", self.tekan_tombol)
        self.reset()

    def reset(self):
        tengah = JUMLAH_KOTAK // 2
        self.ular = [(tengah, tengah), (tengah - 1, tengah), (tengah - 2, tengah)]
        self.arah = (1, 0)
        self.arah_berikutnya = self.arah
        self.skor = 0
        self.selesai = False
        self.berjalan = True
        self.buat_makanan()
        self.gambar()
        self.langkah()

    def buat_makanan(self):
        kosong = [
            (x, y)
            for x in range(JUMLAH_KOTAK)
            for y in range(JUMLAH_KOTAK)
            if (x, y) not in self.ular
        ]
        self.makanan = random.choice(kosong)

    def tekan_tombol(self, event):
        tombol = event.keysym.lower()
        arah = {
            "up": (0, -1), "w": (0, -1),
            "down": (0, 1), "s": (0, 1),
            "left": (-1, 0), "a": (-1, 0),
            "right": (1, 0), "d": (1, 0),
        }

        if tombol == "space" and self.selesai:
            self.reset()
            return

        calon = arah.get(tombol)
        if calon and calon != (-self.arah[0], -self.arah[1]):
            self.arah_berikutnya = calon

    def langkah(self):
        if not self.berjalan:
            return

        self.arah = self.arah_berikutnya
        kepala_x, kepala_y = self.ular[0]
        dx, dy = self.arah
        kepala_baru = (kepala_x + dx, kepala_y + dy)

        makan = kepala_baru == self.makanan
        bagian_tubuh = self.ular if makan else self.ular[:-1]
        tabrak_dinding = not (
            0 <= kepala_baru[0] < JUMLAH_KOTAK
            and 0 <= kepala_baru[1] < JUMLAH_KOTAK
        )

        if tabrak_dinding or kepala_baru in bagian_tubuh:
            self.akhir_permainan()
            return

        self.ular.insert(0, kepala_baru)
        if makan:
            self.skor += 1
            self.skor_label.config(text=f"Skor: {self.skor}")
            self.buat_makanan()
        else:
            self.ular.pop()

        self.gambar()
        self.root.after(KECEPATAN_MS, self.langkah)

    def gambar(self):
        self.canvas.delete("all")

        # Garis tipis membantu melihat petak tanpa mengganggu permainan.
        for posisi in range(0, LEBAR + 1, UKURAN_KOTAK):
            self.canvas.create_line(posisi, 0, posisi, TINGGI, fill="#273244")
            self.canvas.create_line(0, posisi, LEBAR, posisi, fill="#273244")

        mx, my = self.makanan
        batas = 4
        self.canvas.create_oval(
            mx * UKURAN_KOTAK + batas, my * UKURAN_KOTAK + batas,
            (mx + 1) * UKURAN_KOTAK - batas, (my + 1) * UKURAN_KOTAK - batas,
            fill="#fb7185", outline="",
        )

        for indeks, (x, y) in enumerate(self.ular):
            jarak = 2
            warna = "#a3e635" if indeks == 0 else "#65a30d"
            self.canvas.create_rectangle(
                x * UKURAN_KOTAK + jarak, y * UKURAN_KOTAK + jarak,
                (x + 1) * UKURAN_KOTAK - jarak,
                (y + 1) * UKURAN_KOTAK - jarak,
                fill=warna, outline="",
            )

    def akhir_permainan(self):
        self.berjalan = False
        self.selesai = True
        self.canvas.create_rectangle(
            25, TINGGI // 2 - 48, LEBAR - 25, TINGGI // 2 + 48,
            fill="#111827", outline="#4b5563", width=2,
        )
        self.canvas.create_text(
            LEBAR // 2, TINGGI // 2 - 14,
            text="Permainan Selesai!", fill="#f9fafb",
            font=("Arial", 20, "bold"),
        )
        self.canvas.create_text(
            LEBAR // 2, TINGGI // 2 + 20,
            text=f"Skor: {self.skor}  •  Tekan Spasi untuk bermain lagi",
            fill="#cbd5e1", font=("Arial", 11),
        )


if __name__ == "__main__":
    jendela = tk.Tk()
    PermainanUlar(jendela)
    jendela.mainloop()
