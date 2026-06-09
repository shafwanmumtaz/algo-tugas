from flask import Flask, render_template, request, redirect, url_for, flash
from models import ManajemenMahasiswa

app = Flask(__name__)
app.secret_key = "kunci_rahasia_manajemen_mahasiswa"

# Inisialisasi manajemen data
manajemen = ManajemenMahasiswa()


@app.route('/')
def index():
    """Halaman utama - menampilkan semua data mahasiswa"""
    data_mahasiswa = manajemen.get_all()
    return render_template('index.html', mahasiswa=data_mahasiswa, total=len(data_mahasiswa))


@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    """Halaman tambah data mahasiswa"""
    if request.method == 'POST':
        nim = request.form.get('nim', '').strip()
        nama = request.form.get('nama', '').strip()
        email = request.form.get('email', '').strip()
        jurusan = request.form.get('jurusan', '').strip()

        success, message = manajemen.tambah(nim, nama, email, jurusan)

        if success:
            flash(message, 'success')
            return redirect(url_for('index'))
        else:
            flash(message, 'danger')

    return render_template('tambah.html')


@app.route('/edit/<nim>', methods=['GET', 'POST'])
def edit(nim):
    """Halaman edit data mahasiswa"""
    mahasiswa = manajemen.cari_by_nim(nim)

    if not mahasiswa:
        flash(f"Mahasiswa dengan NIM {nim} tidak ditemukan", 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nama = request.form.get('nama', '').strip()
        email = request.form.get('email', '').strip()
        jurusan = request.form.get('jurusan', '').strip()

        success, message = manajemen.edit(nim, nama, email, jurusan)

        if success:
            flash(message, 'success')
            return redirect(url_for('index'))
        else:
            flash(message, 'danger')

    return render_template('edit.html', mahasiswa=mahasiswa)


@app.route('/hapus/<nim>')
def hapus(nim):
    """Hapus data mahasiswa"""
    success, message = manajemen.hapus(nim)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('index'))


@app.route('/cari', methods=['GET', 'POST'])
def cari():
    """Halaman pencarian mahasiswa"""
    hasil = []
    keyword = ""
    metode = ""

    if request.method == 'POST':
        metode = request.form.get('metode', '')
        keyword = request.form.get('keyword', '').strip()

        if metode == 'nama':
            hasil = manajemen.cari_by_nama(keyword)
        elif metode == 'jurusan':
            hasil = manajemen.cari_by_jurusan(keyword)
        elif metode == 'nim_binary':
            # Binary search memerlukan data terurut berdasarkan NIM
            manajemen.merge_sort_by_nim()  # Urutkan dulu
            mhs = manajemen.binary_search_by_nim(keyword)
            hasil = [mhs] if mhs else []

    return render_template('cari.html', hasil=hasil, keyword=keyword, metode=metode)


@app.route('/sort/<metode>')
def sort_data(metode):
    """Mengurutkan data berdasarkan metode tertentu"""
    if metode == 'bubble_nama':
        manajemen.bubble_sort_by_nama()
        flash("Data berhasil diurutkan menggunakan Bubble Sort (berdasarkan Nama)", 'success')
    elif metode == 'selection_nim':
        manajemen.selection_sort_by_nim()
        flash("Data berhasil diurutkan menggunakan Selection Sort (berdasarkan NIM)", 'success')
    elif metode == 'merge_nim':
        manajemen.merge_sort_by_nim()
        flash("Data berhasil diurutkan menggunakan Merge Sort (berdasarkan NIM)", 'success')
    else:
        flash("Metode sorting tidak dikenal", 'danger')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)