# Project-Prediksi-Kemiskinan

## Deskripsi Singkat Aplikasi
Project-Prediksi-Kemiskinan adalah sebuah sistem berbasis web yang memanfaatkan model Machine Learning untuk menganalisis data metrik dan memprediksi tingkat kemiskinan suatu daerah. Sistem ini dirancang untuk mendukung pengambilan keputusan dan intervensi kebijakan secara cepat dan tepat.

## Anggota Tim & Peran
* Dyah Avri Kartika Hapsari - Product Lead / UI & UX Designer
* Laila Nabila Rahmanisa - Backend Developer
* Nazwa Hardiana Gisanov - Frontend Developer

## Cara Menjalankan Aplikasi
Pastikan Anda telah menginstal Docker dan Docker Compose di sistem Anda.

1. Clone repositori ini:
   git clone https://github.com/lievlya/Project-Prediksi-Kemiskinan.git
   cd Project-Prediksi-Kemiskinan

2. Konfigurasi Variabel Lingkungan:
   Salin file template.env menjadi .env dan sesuaikan nilainya:
   cp template.env .env

3. Jalankan dengan Docker Compose:
   docker-compose up -d

4. Akses Aplikasi:
   Buka browser dan akses http://localhost:5000

## Daftar Endpoint API
| Metode | Endpoint | Deskripsi |
| :--- | :--- | :--- |
| GET | /api/status | Mengecek status server |
| POST | /api/prediksi | Mengirim data untuk mendapatkan hasil prediksi |

## Informasi Teknis
* Arsitektur: Menggunakan Docker Compose untuk orkestrasi multi-kontainer yang memastikan portabilitas antar sistem operasi[cite: 2].
* Persistensi Data: Menggunakan Named Volume untuk database agar data tetap tersimpan secara permanen[cite: 2].
* Pengembangan: Menggunakan Bind Mount untuk akses log yang mudah selama tahap debugging[cite: 2].
