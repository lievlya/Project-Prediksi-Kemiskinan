<img width="1365" height="634" alt="image" src="https://github.com/user-attachments/assets/31903494-ad4b-4992-9bd5-02ac9aa101ae" /><img width="1365" height="634" alt="image" src="https://github.com/user-attachments/assets/0662b00c-3089-477d-ad24-33546ce2bf04" /><img width="1365" height="634" alt="image" src="https://github.com/user-attachments/assets/494125cd-ca4d-44fc-ad39-a75a2172e0f3" /># Arsitektur Proyek: Prediksi Kemiskinan Berbasis Machine Learning

Proyek ini mengimplementasikan pola arsitektur **MVC (Model-View-Controller)** untuk memisahkan tanggung jawab kode secara terstruktur, mencegah konflik, dan memudahkan kolaborasi tim.

## Struktur Direktori Utama
Kita menggunakan pemisahan langsung pada *root* folder:
* **Model (`models/`):** Layer ini secara eksklusif mengelola logika bisnis, basis data, dan interaksi dengan model *Machine Learning* untuk menghasilkan data prediksi kemiskinan. Bagian ini sepenuhnya menjadi tanggung jawab Backend Developer.
* **View (`views/`):** Layer ini mengelola antarmuka pengguna (UI). Fokus utama di sini murni pada UI/UX. Panduan implementasi visual merujuk langsung pada *layout* yang disusun di Figma, memprioritaskan tata letak berbasis *grid* untuk menyajikan hasil prediksi agar mudah dibaca. Desain harus dipertahankan sebersih mungkin—elemen usang seperti *navbar* kapsul atau logo gantung tidak boleh diimplementasikan. Bagian ini dikerjakan oleh Frontend Developer.
* **Controller (`controllers/`):** Bertindak sebagai penghubung sistem. Menerima *input* metrik dari pengguna melalui View, meneruskannya ke Model untuk diproses oleh *Machine Learning*, dan mengembalikan hasil prediksinya kembali ke View. Dikerjakan oleh Backend Developer.
