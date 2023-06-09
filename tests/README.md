1.	Pengujian Registrasi:
•	Mengirimkan permintaan POST ke endpoint /register dengan data pengguna yang valid (email dan password sesuai dengan persyaratan).
•	Memastikan status respons adalah 200 OK dan mendapatkan ID pengguna yang unik.
•	Mengirimkan permintaan POST kembali dengan email yang sama.
•	Memastikan status respons adalah 400 Bad Request dengan pesan kesalahan yang sesuai.

2.	Pengujian Login:
•	Mengirimkan permintaan POST ke endpoint /login dengan data pengguna yang terdaftar.
•	Memastikan status respons adalah 200 OK dan mendapatkan token akses JWT.
•	Mengirimkan permintaan POST dengan email atau password yang salah.
•	Memastikan status respons adalah 401 Unauthorized dengan pesan kesalahan yang sesuai.

3.	Pengujian Peminjaman Buku:
•	Mengirimkan permintaan POST ke endpoint /peminjaman dengan data peminjaman yang valid (ID buku yang tersedia).
•	Memastikan status respons adalah 200 OK dan mendapatkan detail peminjaman buku.
•	Mengirimkan permintaan POST kembali dengan pengguna yang sama dan buku yang sedang dipinjam.
•	Memastikan status respons adalah 400 Bad Request dengan pesan kesalahan yang sesuai.

4.	Pengujian Pengembalian Buku:
•	Mengirimkan permintaan POST ke endpoint /pengembalian dengan pengguna yang telah meminjam buku.
•	Memastikan status respons adalah 200 OK dan mendapatkan detail peminjaman buku setelah pengembalian.
•	Mengirimkan permintaan POST kembali dengan pengguna yang tidak memiliki peminjaman buku.
•	Memastikan status respons adalah 404 Not Found dengan pesan kesalahan yang sesuai.

5.	Pengujian Cek Peminjaman:
•	Mengirimkan permintaan GET ke endpoint /cek-peminjaman/{buku_id} dengan ID buku yang tersedia.
•	Memastikan status respons adalah 200 OK dan mendapatkan status peminjaman buku.
•	Mengirimkan permintaan GET dengan ID buku yang tidak tersedia.
•	Memastikan status respons adalah 404 Not Found dengan pesan kesalahan yang sesuai.
