# Blueprint & Desain Sistem: Project-Prediksi-Kemiskinan

## 1. Ide Besar & Deskripsi Aplikasi
Sistem digital terintegrasi yang berfungsi untuk mengelola dan menganalisis data indikator sosial-ekonomi menggunakan pendekatan *Machine Learning*. [cite_start]Aplikasi ini dirancang sebagai dokumen perancangan utama (*Design Phase*) untuk merangkum arah pengembangan proyek[cite: 517, 521, 586, 590]. Kehadiran platform ini ditujukan untuk memetakan dan memprediksi tingkat kemiskinan wilayah guna mendukung efisiensi serta akurasi pengambilan kebijakan intervensi oleh pemerintah daerah.

## 2. Panduan Visual & Aturan Antarmuka
Untuk menjamin konsistensi produk dan pengalaman pengguna yang profesional, seluruh implementasi visual antarmuka wajib mematuhi parameter arsitektur berikut:
* **Sistem Tata Letak:** Penyajian data, matriks indikator, dan visualisasi grafik hasil prediksi wajib menerapkan struktur berbasis *grid* yang rapi dan tegas demi menjaga keterbacaan metrik.
* **Estetika & Gaya:** Desain mengutamakan kesan elegan, minimalis, profesional, dan bersih (*clean look*).
* **Restriksi Visual:** Antarmuka harus berorientasi pada fungsionalitas tingkat tinggi. Dilarang keras mengimplementasikan elemen dekoratif yang tidak efisien atau usang seperti penggunaan *navbar* kapsul maupun logo gantung.

## 3. Cetak Biru Kerangka Halaman Utama
[cite_start]Sebagai panduan formal bagi pengembang antarmuka, sistem ini mengintegrasikan minimal tiga halaman utama sebagai fondasi aplikasi[cite: 528, 597]:

### A. Halaman Landing Page
* **Navbar:** Memuat logo aplikasi, menu navigasi utama (Beranda, Tentang, Kontak), serta tombol aksi "Masuk".
* **Hero Section:** Menampilkan judul utama aplikasi "Prediksi Kemiskinan", teks deskripsi singkat sistem, dan tombol ajakan bertindak (*Call to Action*) "Mulai Analisis".
* **Footer:** Memuat catatan hak cipta aplikasi dan tautan resmi media sosial.

### B. Halaman Login
* **Form Container:** Kotak form pengisian kredensial yang diletakkan secara simetris di pusat tengah layar untuk menjaga fokus pengguna.
* **Input Fields:** Kolom entri data terproteksi untuk Email dan Kata Sandi.
* **Tombol Aksi:** Tombol submit utama untuk memproses autentikasi masuk.
* **Tautan Pendukung:** Akses navigasi sekunder untuk pemulihan akun ("Lupa Password?") atau registrasi ("Daftar Akun Baru").

### C. Halaman Dashboard
* **Sidebar Navigasi:** Panel samping terstruktur untuk manajemen perpindahan fitur (Ringkasan, Data Prediksi, Pengaturan).
* **Header Atas:** Menampilkan informasi ringkas profil pengguna aktif (avatar) dan pusat notifikasi.
* **Widget Indikator:** Kotak ringkasan informasi eksekutif untuk menyajikan data metrik makro (seperti Total Data dan Tingkat Kemiskinan Saat Ini).
* **Tabel Analisis:** Komponen tabel terstruktur untuk menyajikan daftar hasil analisis prediksi kemiskinan berdasarkan tabulasi daerah.

## 4. Tautan Prototipe Desain (Mockup UI)
[cite_start]Dokumentasi desain interaktif dan spesifikasi visual lengkap yang disepakati untuk proyek ini dapat diakses secara langsung melalui tautan Figma berikut:
https://www.figma.com/design/9uhs3hK29wrGbpPYXW4b7T/workspace-nazwa?node-id=186-700&t=V4llCFgGEqAYBSbf-1
