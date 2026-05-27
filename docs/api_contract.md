1\. /api/v1/auth/login (POST)

Fungsi: Pintu Masuk (Keamanan).



Penjelasan: Frontend mengirimkan email dan password. Backend mengecek kesesuaiannya, lalu mencetak "Kunci Akses" (Token) agar pengguna bisa masuk secara sah ke dalam sistem.



2\. /api/v1/profile (GET)

Fungsi: Identitas Pengguna.



Penjelasan: Bertugas mengambil data siapa yang sedang login (seperti nama lengkap dan role "Administrator") untuk ditampilkan pada header profil aplikasi.



3\. /api/v1/dashboard/summary (GET)

Fungsi: Ringkasan Eksekutif.



Penjelasan: Khusus menarik angka-angka rekapitulasi cepat (contoh: Total Daerah Terdata, Persentase Kemiskinan Tertinggi) untuk mengisi kotak-kotak metrik (widget) di halaman awal Dashboard.



4\. /api/v1/poverty-data (GET)

Fungsi: Daftar Tabel Lengkap.



Penjelasan: Bertugas menarik memborong semua data riwayat wilayah beserta rincian metrik ekonominya, yang nantinya dijejerkan rapi di dalam komponen Tabel Data.



5\. /api/v1/poverty-data/analyze (POST)

Fungsi: Otak Prediksi (Machine Learning).



Penjelasan: Frontend menyetorkan data ekonomi daerah yang baru. Backend akan mengolahnya menggunakan model Machine Learning, lalu langsung mengembalikan status hasil prediksinya ke layar pengguna.

