import re
import json
import os
from typing import List, Optional, Dict

# ================================
# KELAS PERSON (INDUK)
# ================================
class Person:
    def __init__(self, nama: str, email: str):
        self._nama = nama
        self._email = email

    @property
    def nama(self):
        return self._nama

    @nama.setter
    def nama(self, value):
        if not value or not value.strip():
            raise ValueError("Nama tidak boleh kosong")
        self._nama = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        # Regex validasi email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise ValueError("Email tidak valid")
        self._email = value

    def tampilkan_info(self) -> str:
        return f"{self.nama} - {self.email}"


# ================================
# KELAS MAHASISWA (TURUNAN)
# ================================
class Mahasiswa(Person):
    def __init__(self, nim: str, nama: str, email: str, jurusan: str):
        super().__init__(nama, email)
        self._nim = nim
        self._jurusan = jurusan

    @property
    def nim(self):
        return self._nim

    @nim.setter
    def nim(self, value):
        # Regex validasi NIM: minimal 8 digit angka
        if not re.match(r'^\d{8,12}$', value):
            raise ValueError("NIM harus 8-12 digit angka")
        self._nim = value

    @property
    def jurusan(self):
        return self._jurusan

    @jurusan.setter
    def jurusan(self, value):
        if not value or not value.strip():
            raise ValueError("Jurusan tidak boleh kosong")
        self._jurusan = value

    def to_dict(self) -> dict:
        return {
            "nim": self.nim,
            "nama": self.nama,
            "email": self.email,
            "jurusan": self.jurusan
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Mahasiswa':
        return cls(data["nim"], data["nama"], data["email"], data["jurusan"])


# ================================
# KELAS MANAJEMEN (CRUD + FILE I/O)
# ================================
class ManajemenMahasiswa:
    def __init__(self, file_path: str = "data_mahasiswa.json"):
        self.file_path = file_path
        self._load_data()

    def _load_data(self):
        """Load data dari file JSON"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.data = [Mahasiswa.from_dict(item) for item in data]
            else:
                self.data = []
        except (json.JSONDecodeError, Exception):
            self.data = []

    def _save_data(self):
        """Simpan data ke file JSON"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([mhs.to_dict() for mhs in self.data], f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    # ========== CRUD ==========
    def tambah(self, nim: str, nama: str, email: str, jurusan: str) -> tuple[bool, str]:
        try:
            # Cek duplikat NIM
            if self.cari_by_nim(nim):
                return False, f"NIM {nim} sudah terdaftar"

            mahasiswa = Mahasiswa(nim, nama, email, jurusan)
            self.data.append(mahasiswa)
            self._save_data()
            return True, "Data berhasil ditambahkan"
        except ValueError as e:
            return False, str(e)

    def edit(self, nim: str, nama: str, email: str, jurusan: str) -> tuple[bool, str]:
        try:
            mhs = self.cari_by_nim(nim)
            if not mhs:
                return False, f"NIM {nim} tidak ditemukan"

            mhs.nama = nama
            mhs.email = email
            mhs.jurusan = jurusan
            self._save_data()
            return True, "Data berhasil diupdate"
        except ValueError as e:
            return False, str(e)

    def hapus(self, nim: str) -> tuple[bool, str]:
        mhs = self.cari_by_nim(nim)
        if not mhs:
            return False, f"NIM {nim} tidak ditemukan"

        self.data.remove(mhs)
        self._save_data()
        return True, "Data berhasil dihapus"

    def get_all(self) -> List[Mahasiswa]:
        return self.data

    # ========== SEARCHING ==========
    def cari_by_nim(self, nim: str) -> Optional[Mahasiswa]:
        """Linear Search by NIM"""
        for mhs in self.data:
            if mhs.nim == nim:
                return mhs
        return None

    def cari_by_nama(self, keyword: str) -> List[Mahasiswa]:
        """Sequential Search by Nama (partial match)"""
        keyword_lower = keyword.lower()
        return [mhs for mhs in self.data if keyword_lower in mhs.nama.lower()]

    def cari_by_jurusan(self, jurusan: str) -> List[Mahasiswa]:
        """Linear Search by Jurusan"""
        jurusan_lower = jurusan.lower()
        return [mhs for mhs in self.data if jurusan_lower in mhs.jurusan.lower()]

    def binary_search_by_nim(self, nim: str) -> Optional[Mahasiswa]:
        """Binary Search - harus data terurut dulu"""
        sorted_data = sorted(self.data, key=lambda x: x.nim)
        low, high = 0, len(sorted_data) - 1
        while low <= high:
            mid = (low + high) // 2
            if sorted_data[mid].nim == nim:
                return sorted_data[mid]
            elif sorted_data[mid].nim < nim:
                low = mid + 1
            else:
                high = mid - 1
        return None

    # ========== SORTING ==========
    def bubble_sort_by_nama(self):
        """Bubble Sort berdasarkan nama"""
        n = len(self.data)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if self.data[j].nama.lower() > self.data[j + 1].nama.lower():
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
        self._save_data()

    def selection_sort_by_nim(self):
        """Selection Sort berdasarkan NIM"""
        n = len(self.data)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self.data[j].nim < self.data[min_idx].nim:
                    min_idx = j
            self.data[i], self.data[min_idx] = self.data[min_idx], self.data[i]
        self._save_data()

    def merge_sort_by_nim(self):
        """Merge Sort berdasarkan NIM"""
        self.data = self._merge_sort(self.data)
        self._save_data()

    def _merge_sort(self, arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid])
        right = self._merge_sort(arr[mid:])
        return self._merge(left, right)

    def _merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i].nim < right[j].nim:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result