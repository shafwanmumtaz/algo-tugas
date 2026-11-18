# Aplikasi Web Manajemen Data Mahasiswa (Python & Flask)

🌐 **Demo Aplikasi:** [https://algo-tugas.vercel.app/](https://algo-tugas.vercel.app/)  
👤 **Penyusun:** Shafwan Mumtaz (NIM: 241011450529 — S1 Teknik Informatika, Universitas Pamulang)

Proyek ini merupakan aplikasi web **Manajemen Data Mahasiswa** berbasis **Python (Flask)** yang mengimplementasikan konsep Pemrograman Berorientasi Objek (*Object-Oriented Programming*), validasi input menggunakan *Regular Expression* (`re`), penyimpanan data persisten berbasis JSON, serta algoritma pencarian (*Searching*) dan pengurutan (*Sorting*).

---

## Fitur Utama

1. **Manajemen Data (CRUD Lengkap):**
   - **Tambah Mahasiswa:** Validasi otomatis NIM (8–12 digit angka) dan format email menggunakan Regex, serta pengecekan duplikasi NIM.
   - **Lihat & Edit Data:** Menampilkan daftar seluruh mahasiswa dan memperbarui informasi Nama, Email, serta Jurusan.
   - **Hapus Data:** Menghapus data mahasiswa berdasarkan NIM dan memperbarui file penyimpanan `data_mahasiswa.json`.

2. **Pencarian Data (*Searching Algorithms*):**
   - **Linear / Sequential Search:** Pencarian berdasarkan NIM, Nama (*partial match*), atau Jurusan.
   - **Binary Search:** Pencarian cepat berdasarkan NIM setelah data diurutkan terlebih dahulu.

3. **Pengurutan Data (*Sorting Algorithms*):**
   - **Bubble Sort:** Mengurutkan data mahasiswa berdasarkan Nama (A–Z).
   - **Selection Sort:** Mengurutkan data mahasiswa berdasarkan NIM secara menaik (*ascending*).
   - **Merge Sort:** Mengurutkan data mahasiswa berdasarkan NIM dengan pendekatan *divide and conquer*.

4. **Konsep OOP (*Object-Oriented Programming*):**
   - Pewarisan kelas (*Inheritance*) dari kelas induk `Person` ke kelas turunan `Mahasiswa` di `models.py`.
   - Enkapsulasi atribut (`_nim`, `_nama`, `_email`, `_jurusan`) menggunakan `@property` dan `@setter`.

---

## Struktur File

```text
├── app.py                 # Routing utama aplikasi web Flask
├── models.py              # Kelas Person, Mahasiswa, dan ManajemenMahasiswa (CRUD, Search, Sort)
├── data_mahasiswa.json    # Penyimpanan data mahasiswa dalam format JSON
├── requirements.txt       # Daftar pustaka Python (Flask)
└── templates/             # Template antarmuka HTML (base, index, tambah, edit, cari)
```

---

## Cara Menjalankan di Lokal

1. Pastikan Python 3 sudah terpasang, lalu instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```
2. Jalankan server Flask:
   ```bash
   python app.py
   ```
3. Buka browser dan akses `http://localhost:5000`.
