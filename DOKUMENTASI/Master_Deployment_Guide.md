# 📘 BUKU PANDUAN MASTER (ULTIMATE GUIDE)
# DEPLOYMENT & OPERASIONAL SISTEM SaaS: CLS, SIMKOS, & SERPTECH

Selamat datang di **Buku Pintar Master Deployment**. Dokumen ini telah distrukturkan sedemikian rupa agar sangat mudah dibaca, dengan jarak antar paragraf yang lega, penyorotan, dan fokus pada detail langkah demi langkah.

Dokumen ini adalah pegangan mutlak Anda setiap kali ada klien baru atau ketika Anda memindahkan aplikasi ke Server (VPS) yang baru. Di dalam buku ini merangkum langkah mulai dari perakitan server kosongan hingga penanganan error di Linux.

---

> [!IMPORTANT]
> **ATURAN EMAS SERVER:** VPS Linux Anda sangat sensitif terhadap **huruf besar/kecil (Case Sensitive)**. Pastikan pengejaan folder seperti `SIMKOS` atau `SERPTECH` sama persis setiap saat Anda mengetik perintah.

<br>

---

## 🏗️ BAB 1: ARSITEKTUR & PERSIAPAN DOMAIN (DNS)
Sistem ini terdiri dari 3 aplikasi terpisah (Microservices) yang hidup bersama di 1 VPS (IP `76.13.17.98`). Masing-masing harus punya alamat rumah (sub-domain) sendiri.

### 1.1 Tabel Pengaturan Routing DNS (Di Hostinger / HPanel)
| Aplikasi | Jenis Record | Host / Nama | Points To / IPv4 | Hasil Akhir (URL) |
| :------- | :----------- | :---------- | :--------------- | :----------------------- |
| CLS      | A            | cls         | 76.13.17.98      | cls.serpgroup.cloud      |
| SIMKOS   | A            | simkos      | 76.13.17.98      | simkos.serpgroup.cloud   |
| SERPTECH | A            | serptech    | 76.13.17.98      | serptech.serpgroup.cloud |

> [!NOTE]
> Setelah Anda menyimpannya di panel domain, sistem internet global membutuhkan waktu sekitar **5-15 Menit** (Delay Propagasi DNS) sebelum domain tersebut aktif beroperasi.

<br>

---

## 🛠️ BAB 2: SETUP AWAL VPS (PONDASI SERVER KOSONG)
Tahap ini **HANYA** perlu Anda lakukan **1 KALI SEUMUR HIDUP** pada VPS Linux Anda yang benar-benar baru. Jangan diulang-ulang!

### 2.1. Update & Instalasi Perangkat Lunak Wajib
Buka Terminal SSH Anda dan masuk menggunakan kredensial tertinggi (`ssh root@76.13.17.98`). 

**Langkah 1: Membangunkan Sistem VPS**  
Meminta Ubuntu memperbarui seluruh katalog sistem keamanannya agar VPS siap tempur, serta membangun kompiler dasar C++ (Dibutuhkan jika Anda kelak menanamkan modul canggih seperti Face Recognition).
```bash
apt update && apt upgrade -y
apt-get install cmake gcc g++ build-essential -y
```

**Langkah 2: Menginstal Paket Raksasa Wajib**  
Menginstal Web Server pendengung (Nginx), Tukang Download (Git), Editor teks (Nano), Kunci Gembok (Certbot SSL), Pustaka Ular (Python), dan Gudang Tabel (PostgreSQL).
```bash
apt install nginx git curl nano certbot python3-certbot-nginx python3 python3-pip python3-venv python3-dev libpq-dev postgresql postgresql-contrib -y
```

<br>

### 2.2. Membuat 3 Rumah Database & Akun Tertinggi
Nyalakan sistem Database Relational Postgres secara abadi:
```bash
systemctl start postgresql
systemctl enable postgresql
sudo -u postgres psql
```

Sekarang layar Terminal Anda berubah menjadi area SQL (`postgres=#`). Ketikkan rentetan kode ini perlahan.  
*(Catatan Penting: Wajib akhiri tiap baris dengan titik koma `;`)*

```sql
-- 1. Membuat akun dewa pengatur segalanya
CREATE USER superadmin WITH PASSWORD 'PasswordKuatAnda123!';

-- 2. Memastikan karakter teks dan jam tidak berantakan
ALTER ROLE superadmin SET client_encoding TO 'utf8';
ALTER ROLE superadmin SET timezone TO 'Asia/Jakarta';

-- 3. Memberi izin pada "superadmin" untuk membuat rumah/tabel
ALTER USER superadmin CREATEDB;

-- 4. Membelah rumah menjadi 3 kamar khusus agar data PT tidak bercampur
CREATE DATABASE db_cls OWNER superadmin;
CREATE DATABASE db_simkos OWNER superadmin;
CREATE DATABASE db_serptech OWNER superadmin;

-- 5. Perintah 'Keluar' dari jiwa SQL dan kembali ke layar Linux biasa
\q
```

<br>

---

## 📂 BAB 3: SIKLUS ALUR KERJA (WORKFLOW) KODE
Rahasia deployment yang sukses adalah jangan memindah (copy-paste) file manual memakai flashdisk atau FTP. Sangat terlarang! Kita wajib menggunakan mesin cerdas **GitHub**.

### 3.1. PC ke GitHub (Upload Pertama dari Laptop Lokal)
Lakukan instruksi ini **Di Dalam Terminal VSCode Komputer Anda**, untuk **setiap folder aplikasi Anda**:

1. **"Bangunkan si Pelacak"**: Menyuruh sistem mencatat segala pergerakan file Anda.
   ```bash
   git init
   ```

2. **"Angkat Semuanya"**: Tanda titik = Masukkan jutaan baris kode ke keranjang perantaraan.
   ```bash
   git add .
   ```

3. **"Segel Keranjang & Beri Label Teks"**: Mencatat histori update Anda.
   ```bash
   git commit -m "Upload Pertama Ke Awan Server"
   ```

4. **"Buat Rel Kereta Utama"**: Penamaan rel ke sistem modern utama.
   ```bash
   git branch -M main
   ```

5. **"Incar Target Awan"**: Memberitahu file agar meluncur ke alamat spesifik penyimpanan GitHub Anda.
   ```bash
   git remote add origin https://github.com/Username/repo.git
   ```

6. **"LUNCURKAN!"**: Memompa file dari WiFi Rumah ke GitHub.
   ```bash
   git push -u origin main
   ```

<br>

### 3.2. Menyedot Kode dari GitHub ke VPS
Sekarang Anda berpindah duduk menjadi operator server. Buka **Terminal VPS Anda**.

Masuk ke teras panggung Web Global Linux `/var/www/`, dan lakukan *Kloning* (Download wujud folder fisik) secara serempak:
```bash
cd /var/www/

git clone https://github.com/UsernameAnda/repo-cls.git Central-License-Server
git clone https://github.com/UsernameAnda/repo-simkos.git SIMKOS
git clone https://github.com/UsernameAnda/repo-serptech.git SERPTECH
```

<br>

---

## 🚀 BAB 4: PROSEDUR SETUP MASING-MASING APLIKASI
Proses super krusial ini **WAJIB diulangi 3 Kali**. Sekali untuk pengerjaan CLS, sekali untuk SIMKOS, dan sekali untuk SERPTECH.

> [!TIP]
> Di bawah ini, saya mencontohkan dengan target perakitan aplikasi **SIMKOS**. Jika Anda sedang merakit aplikasi lain (CLS/SERPTECH), silakan **ganti kata tulisan SIMKOS** menjadi nama aplikasi tujuan Anda!

<br>

### 4.1. Membuat Ruangan Steril (Virtual Environment / Venv)
Agar modul kodingan milik SIMKOS tidak menusuk atau bentrok dengan modul versi lama milik SERPTECH.

**Langkah 1: Masuk TEPAT ke dalam folder aplikasi yang mau diracik**
```bash
cd /var/www/SIMKOS
```

**Langkah 2: Lahirkan gelembung isolasi bernama "env" dan Nyalakan**
```bash
python3 -m venv env
source env/bin/activate
```

**Langkah 3: Instal Pustaka Kode dan Mesin Eksekutor**
Instal seluruh ketergantungan Django dan koki penggerak web (Gunicorn) serta pengakses database.
```bash
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

<br>

### 4.2. File Keamanan Induk: `.env.prod` (Sangat Krusial!)
File `.env` sengaja tidak ditaruh di GitHub demi keamanan mutlak. Kita wajib menjahitnya manual **satu kali** di dalam VPS.

Buka teks editor sakti Nano:
```bash
nano .env.prod
```

Salin dan Tempel (Paste / Klik Kanan) teks kerangka rahasia ini:
```env
# ==== ZONA 1: SETTING TINGKAH LAKU ====
DEBUG=False
SECRET_KEY=ngawur-ketik-saja-acak-panjang-12345

# ==== ZONA 2: TAMENG KEAMANAN URL DEPAN ====
# JANGAN SALAH! Isi dengan ALAMAT SUB-DOMAIN APLIKASI INI SAJA!
ALLOWED_HOSTS=simkos.serpgroup.cloud
CSRF_TRUSTED_ORIGINS=https://simkos.serpgroup.cloud

# ==== ZONA 3: KUNCI MASUK RUANG BRANKAS DATABASE ====
# DB_NAME harus sama persis dengan nama DB yang kita buat di Bab 2!
DB_ENGINE=django.db.backends.postgresql
DB_NAME=db_simkos
DB_USER=superadmin
DB_PASSWORD=PasswordKuatAnda123!
DB_HOST=127.0.0.1
DB_PORT=5432
```
> **Cara Menyimpan Editor Nano:** Tekan bersamaan `Ctrl + O` (Huruf O), lalu tekan `Enter` (untuk memvalidasi nama filenya), lantas tekan `Ctrl + X` (Keluar).

<br>

> [!IMPORTANT]
> **DAFTAR PERBEDAAN MUTLAK `.env` KETIGA APLIKASI SAAT ANDA MENGULANGNYA NANTI:**
> - **`SECRET_KEY`**: Harus beda semua! (Bebas ketik acak apa saja di keyboard asal sangat panjang).
> - **`ALLOWED_HOSTS` & `CSRF_TRUSTED_ORIGINS`**: Sesuaikan dengan nama sub-domain masing-masing (cls / simkos / serptech).
> - **`DB_NAME`**: Harus menunjuk database spesifik: `db_cls` , `db_simkos`, atau `db_serptech`.
> - **`DB_USER` & `DB_PASSWORD`**: PASTI SAMA SEMUA karena ketiga DB di atas dimiliki komando utuh oleh 1 akun `superadmin` di VPS Anda.

<br>

### 4.3. Merakit Bangunan Tabel, Tampilan, & Akun User
Mewujudkan gambar blueprint Django yang ada di kodingan agar menjadi benda nyata operasional:

**Langkah 1: Konstruksi Mandor Database**  
Memaksa Django terjun ke dalam Postgres dan merakit wujud fisik kolom dan baris tabel (Karyawan, Presensi, Gaji, dll).
```bash
python manage.py migrate
```

**Langkah 2: Pemulung Aset Estetika**  
Menyapu bersih semua file desain (CSS Bootstrap, JS, Ikon Grafis) ke dalam karung satu folder bernama `staticfiles/`. Memangkas raksasa agar website meloading ngebut (Cepat).
```bash
python manage.py collectstatic --noinput
```

**Langkah 3: Mencetak Manajer Pemilik Akun**  
Wajib! Agar Anda nantinya bisa masuk ke halaman Login Website. Ketikan baris ini, dan sistem akan menanyakan input Username, Email (Boleh dibiarkan kosong, langsung Enter), dan Password (ketikan pelan, indikator ketikan password memang dirancang buta/tidak bergerak di layar).
```bash
python manage.py createsuperuser
```

**Langkah 4: Keluar Ruang Steril**  
Matikan nyala virtual environment Python untuk menyelesaikan sesi perakitan komponen di aplikasi ini, dan melanjutkan ke aplikasi berikutnya.
```bash
deactivate
```

<br>

---

## ⚡ BAB 5: MENGHIDUPKAN APLIKASI (GUNICORN, NGINX, SSL)
Ini adalah tahap kelistrikan tingkat tinggi; mematri urat nadi web Anda agar menyembur *Go-Live* di muka umum (Internet Public) non-stop.

### 5.1. Membuat Pekerja Mesin Pemutar 24 Jam (Daemon Gunicorn)
Jika kita sekedar memakai perintah `runserver` biasa, web Anda akan mati terkapar seketika saat jendela VPS tertutup. Solusi abadi? SystemD Latar Belakang.

Buat file kendalinya:
```bash
sudo nano /etc/systemd/system/simkos.service
```

Salin-Tempel (Pastikan jalurnya `/var/www/SIMKOS` benar-benar valid!):
```ini
[Unit]
Description=Gunicorn daemon for SIMKOS
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/SIMKOS
Environment="PATH=/var/www/SIMKOS/env/bin"
EnvironmentFile=/var/www/SIMKOS/.env.prod

# ExecStart adalah mantra sakti yang menyembelih gunicorn menjadi urat nadi lunak bernama "simkos.sock"
ExecStart=/var/www/SIMKOS/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/var/www/SIMKOS/simkos.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

Tancapkan saklar konfigurasinya ke tubuh sistem operasi Linux:
```bash
sudo systemctl daemon-reload
sudo systemctl start simkos
sudo systemctl enable simkos
```

<br>

### 5.2. Konfigurasi Mesin Tembok Satpam (NGINX)
Nginx menjamu jutaan tamu internet (Pengunjung), lalu "mengopor"-kannya paksa menyelinap melalui gorong-gorong kabel siluman `simkos.sock` yang barusan Anda hidupkan di atas.

Buka Nginx Routing:
```bash
sudo nano /etc/nginx/sites-available/simkos
```

Salin Konfigurasi ini:
```nginx
server {
    server_name simkos.serpgroup.cloud;

    # Tolong batasi daya penarikan upload foto < 20Mb (Pencegah Server Crash jika Ram Penuh)
    client_max_body_size 20M;

    location = /favicon.ico { access_log off; log_not_found off; }

    # SANGAT PENTING: Aset Desain CSS dialamatkan memotong target ke /staticfiles/ !!!
    location /static/ {
        alias /var/www/SIMKOS/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }

    # Penempatan wadah Unggah Foto Avatar/Media Laporan
    location /media/ {
        alias /var/www/SIMKOS/media/;
        expires 30d;
    }

    # Mem-proxy trafik web keramaian memutar langsung mendarat ke pangkuan aplikasi Python
    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/SIMKOS/simkos.sock;
    }
}
```

<br>

### 5.3. Hubungkan Kabel, X-Ray Diagnostik, & Pasang Gembok Hijau (SSLHTTPS)
Hanya sisa 4 langkah terakhir! Deretan tembak terminal di bawah ini meresmikan situs Anda untuk mendunia:

1. **Colokan Stopkontak (Symlink)**:  
   Menghubungkan catatan buku Nginx situs Anda yang baru dibuat tadi, ke dalam lorong pelaksana Inti Server Nginx.
   ```bash
   sudo ln -s /etc/nginx/sites-available/simkos /etc/nginx/sites-enabled/
   ```

2. **X-Ray Scanner Kelayakan (Test)**:  
   Nginx Pura-Pura mengecek apakah Anda kelupaan menyisipkan Titik Koma (`;`) atau ada yang Tipografi Error spasi. (Jika aman tertera `Syntax is OK`).
   ```bash
   sudo nginx -t
   ```

3. **Jalanan Tol Dibuka**:  
   Resmikan dan izinkan konfigurasi yang Lolos Scanner berjalan aspal.
   ```bash
   sudo systemctl restart nginx
   ```

4. **Tameng Enkripsi Dewa Keselamatan (Sertifikat SSL/HTTPS)**:  
   Meminta Sertifikat Valid global secara otomatis yang meyakinkan Google bahwa Web Anda berfitur `https://`. *(Catatan: Saat berlangsung.. Wajib Anda mengetikkan Huruf `2` jika sistem menanyakan persetujuan instruksi Force Redirect HTTP to HTTPS)*.
   ```bash
   sudo certbot --nginx -d simkos.serpgroup.cloud
   ```

<br>

---

## 🔄 BAB 6: ALUR DEPLOYMENT RUTIN (JIKA ADA UPDATE FITUR)
Bagaimana hari-hari selanjutnya? Anda tidak butuh lagi membuat setup ruwet Database dan Nginx!. Inilah keseharian yang akan Anda sentuh untuk mengubah *Kodingan Tombol* di Laptop, agar mendadak berubah ajaib di Web Situs Live!

**👉 LANGKAH 1 (Pengiriman Dari Aplikasi VSCode Laptop):**
```bash
git add .
git commit -m "Mengesekusi Perbaikan Update"
git push origin main
```

**👉 LANGKAH 2 (Penarikan Masuk ke Dalam VPS Ubuntu Anda):**
```bash
cd /var/www/SIMKOS
git pull origin main
source env/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
deactivate

# 🌟 PENGAKHIRAN KLIMAKS MAUT: 
# Wajib Restart Ingatan memori jangka pendek Gunicorn! Jika tidak ditekan, 
# Kodingan Lama (Cache) lah yang ditampilan, Tombol tak akan pernah berubah warna!
sudo systemctl restart simkos
```

<br>

---

## 🗄️ BAB 7: OPERASIONAL MANAJEMEN DATABASE LENGKAP DI VPS (PSQL & BACKUP)

Jika Anda ingin melihat data, membongkar password, manghapus tabel, atau bahkan **Men-Download Keseluruhan Database Web (Backup)**, Anda berkuasa penuh melakukannya dari jantung VPS!

### 7.1. Gerbang Masuk Menuju Brankas SQL
Pertama-tama, alihkan mode terminal Linux Anda menjadi mode pembedah Database:
```bash
sudo -u postgres psql
```
Sekarang Anda sudah masuk, dan terminal akan meminta perintah khusus berawalan Tanda Garis Miring `\`.

<br>

### 7.2. Trik Berpindah Ruangan Database & Melihat Daftar Tabel
Listrik awal PostgreSQL adalah ruang tunggu global. Anda harus mengetuk pintu dan menyebut nama aplikasi target:
```sql
-- Format: \c (Connect) nama_database_tujuan
\c db_simkos
```
*(Monitor akan nge-print: `You are now connected to database "db_simkos"`)*.

Penasaran ada tabel apa saja yang hidup merakit aplikasi Anda? Ketik:
```sql
\dt
```
**Contoh Tampilan Outputnya di Terminal Hitam:**
```text
                  List of relations
 Schema |            Name            | Type  |  Owner
--------+----------------------------+-------+----------
 public | auth_user                  | table | superadmin
 public | django_session             | table | superadmin
 public | dt_properti_namaproperti   | table | superadmin
 public | core_tenant                | table | superadmin
```

<br>

### 7.3. Melihat (Membaca) Data Manusia Asli (*Read*)
Mari kita bedah wujud kartu identitas sang pengurus Superadmin pada tabel `auth_user` menggunakan kekuatan murni `SELECT`. Jangan lupa titik koma!
```sql
SELECT id, username, email, is_active FROM auth_user;
```

**Hasil Cetakan Visual:**
```text
 id |  username  |          email          | is_active 
----+------------+-------------------------+-----------
  1 | indraadmin | adminindra@serpgroup.com| t
  2 | manajer02  | manajer@serpgroup.cloud | f
```
*(Huruf `t` = True/Aktif. Huruf `f` = False/Mati)*

<br>

### 7.4. Mengedit / Memodifikasi Baris Data (*Update*)
Klien Anda lupa Password adminnya dan ia terblokir? Anda bisa mematikannya atau menggantinya paksa dari konsol! 
```sql
-- Contoh mematikan / nge-benned akun manajer02 dari belakang layar:
UPDATE auth_user SET is_active = False WHERE username = 'manajer02';
```

<br>

### 7.5. Menghapus Data atau Menghapus Tabel (*Delete / Drop*)
**Hati-hati!** Semua aksi psql tidak ada keranjang recycle bin. Sekali Enter lenyap!
```sql
-- 1. Menghapus 1 Kolom Pengguna Nakal:
DELETE FROM auth_user WHERE username = 'darma_nakal';

-- 2. Membumihanguskan Seluruh isi Tabel Karyawan Menjadi Nol Kosong:
TRUNCATE TABLE hr_karyawan CASCADE;

-- 3. Mengebom Patah-patah Sebuah Tabel (Tabelnya Hilang!):
DROP TABLE hr_karyawan;
```

Selesai membongkar di dalam PSQL? Tekan Quit (Keluar) untuk kembali ke Terminal VPS Default!
```sql
\q
```

<br>

### 7.6. MENDOWNLOAD (BACKUP MENTAHAN) DATABASE KE PC LOKAL 
Ini perintah mutlak paling mematikan nan hebat. Anda wajib rutin men-download koper *(Backup)* data aplikasi PT klien agar selamat dari ledakan server. Perintah di bawah ini di ketik **di Luar PSQL (Di Terminal VPS Ubuntu)**!

**Langkah 1: Sedot database VPS Menjadi File `.sql` di Linux**
```bash
# pg_dump -U pemiliknya nama_database > nama_file_keluarannya.sql
pg_dump -U superadmin db_simkos > backup_mingguan_simkos.sql
```

**Langkah 2: Ambil (Download) File Tersebut Memakai CMD WINDOWS ANDA!**
Buka Terminal CMD (Command Prompt / Powershell) di  Laptop Windows Anda (Bukan di VPS!), letakkan di layar Desktop Anda dan tembak perintah Scp Pipa ini untuk menarik koper SQL yang barusan dibuat VPS meluncur jatuh ke pangkuan Laptop Anda lewat internet:
```bash
scp root@76.13.17.98:/root/backup_mingguan_simkos.sql C:\Users\darma\Desktop\
```
*TADAAA! 1 File Kodingan Mentahan Data Jutaan Rupiah SIMKOS Anda barusan mendarat cantik di Komputer Rumah Anda.*

<br>

### 7.7. MENG-IMPORT (RESTORE) DATA KE VPS
Bagaimana jika Server VPS meledak ter-wipe mati karena macet bayar bulanan, lalu Anda menyewa VPS baru, dan kini Anda ingin meng-import hasil koper Backup mingguan tadi ke VPS Baru itu?

**Langkah 1: Tembak/Lempar Kopernya memakai CMD Laptop Anda Menuju Linux**
```bash
scp C:\Users\darma\Desktop\backup_mingguan_simkos.sql root@IP_VPS_YANG_BARU:/root/
```

**Langkah 2: Seduh (Import) Data Ke Kosongan di Dalam VPS Linux Baru!**
Masuk lagi Ke SSH Putty VPS yang Baru dan ketik perintah Import Psql Bawaan:
```bash
# psql -U pemillik database_baru_yg_kosong < nama_file_suntikannya.sql
psql -U superadmin db_simkos < backup_mingguan_simkos.sql
```


<br>

---

## 🚨 BAB 8: BUKU KUNING PEMECAHAN MASALAH (TROUBLESHOOTING)

Inilah pusaka intisari dari 9 macam jenis ragam kecelakan keringat error maut yang lazim mengerayangi perakit awal Linux. Telah diciptakan solusinya secara pamungkas di bawah ini!:

### 🚩 KASUS 1: Error `bash: python: command not found`
- **Tampilan Visual:** Mesin Debian mengamuk! la menolak kalimat pancingan perintah Python seraya meludah error bodoh.
- **Akar Cikal Bakal:** Anda baru saja login menempel muka ke server VPS; lantas asal nge-gas mencoba memanggil pilar skrip python (`python manage.py`) selagi kaki telapak tangan Anda amasih berpijak kotor keluyuran berada di jalan basah direktori umum (artinya: belum masuk perisai gelembung sterilisasi VENV).
- **Solusi Mutlak:** Anda HARUS menyalakan tuas penutup dulu dengan: `source env/bin/activate`! (Ciri kesuksesan utamanya: Ada tulisan stempel bertanda kurung `(env)` di pojok sampaing bahu kiri nama `root@srv`).

### 🚩 KASUS 2: Error `ModuleNotFoundError: No module named 'rest_framework' dll`
- **Tampilan Visual:** Tiba-tiba saat asik memencet tombol proses eksekutor `python manage.py migrate`, alam semesta runtuh menampilkan jejak pelacakan error baris warna merah marun beruntun-runtut! (Stacktrace).
- **Akar Cikal Bakal:** Anda memencet Save Koding selesai membuat fitur baru pada program Anda di Laptop Lokal (Misalkan modul Pandas/DjangoRestAPI/ReportLab); mem-Push nya ke luar angkasa awan Github, narik lagi balik ke peladen VPS. TAPI... Saudara lupa men-Download (Pemasangan instalasi) bibit pustaka Pip Library paket Python di VPS tersebut!
- **Solusi Mutlak:** Aktifkan VENV Python anda, lalu sabet utuh peluru daftar mutakhir kulinya: `pip install -r requirements.txt`. Habis memutar sedot install barulah Anda lanjut migrate lagi.

### 🚩 KASUS 3: Error Pembangun Modul C++ `CMake` Tersumbat (Kasus Face Recognition)
- **Tampilan Visual:** Layar gulungan error Terminal Installer terhenti kaku macet semari mencetak gurat darah teks mematikan berbunyi `Failed building wheel... CMake not found`.
- **Akar Cikal Bakal:** Modul-modul AI Skala Raksasa level tinggi dunia (Sejenis OpenCV. Face Recognition Absensi, Tensor) butuh sandaran nyawa fondasi tulang punggung rakitan kode kompilator C++ murni yang tidak disertakan di kardus instalasi Linux Kosongan Bawaan Hostinger Default.
- **Solusi Mutlak:** Anda memaksakan peladen Terminal VPS menggulung tangan menempah Besi Perangkat keras murninya sendiri secara ajaib: ketik paksa `apt-get install cmake gcc g++ build-essential -y`.  Kemudian sesudahnya Anda silahkan tenang tembakan santai tembakan coba instalasi `pip install ...` tersebut sekali lagi!

### 🚩 KASUS 4: Bencana "502 Bad Gateway" Kosong di Permukaan Layar Chrome Pengunjung
- **Tampilan Visual:** Website di akses via HTTP `simkos...`, tapii seketika jebol mendadak hancur kemunculani tulisan "502 Bad Gateway" dengan layar background cat putih polos layaknya Kuburan Kosong! Padahal status Nginx menyala ceria tanpa rintangan menolak masuk!.
- **Akar Cikal Bakal:**  Tebakan Diagnosa 100% ini terjadi sepenuhnya diakibatkan perbuatan tangan dosa manusia adanya sytnax keliru yang terlewat *"Typo Tanda Baca Koma Kodingan"* atau cacat *"Error Spasi Menjorok Indentasi Tab"* pada penulisan file `views.py` atau `models.py` Anda.  Sialnya si koki pemroses Gunicorn LANGSUNG terjungkal MATI serangan jantung Tersenggol menjerit kejatuhan sintak cacat typo Anda tersebut. Si penjaga pintu Nginx yang sedari awal tersenyum lurus menjulurkan lengan, kebingungan lalu memilih tak acuh mengeplak wajah sang tamu pelancong internet pencarinya menggunakan pelat tulisan angka  502!
- **Solusi Detektif Terhebat:** Menyelam menyusuri alam bawaan bongkahan kuburan *Blackbox Log Sistem Mesin Tempur Nginx Gunicorn* Anda mengenakan radar pelacak tingkat akhir linux : Ketik perintah agung  `journalctl -u simkos.service -e`. Di situlan kelak akan terpajang jujur melantak tertulis berbunyi mendikte: Tepat di baris keberapa `File... .py` aslinya letak sintax maut mematikankannya.  Rubah bongkar file salahnya Pakai Nano, *Save*!, lalu paksakan kejut pacu nafas nadinya sekali tebas membangkitkannya : `systemctl restart simkos`. 

### 🚩 KASUS 5: Halaman Form Login Front-End Hancur Putih, Frame Patah-Patah, Dan Segala Desain Rusak.
- **Tampilan Visual:** UI Interface Form Input Password Login dan tampilan hamparan dasboard menu anda remuk terekspos hingga bentuk kerangka tulang putih telanjang teks polos memalukan meniadakan seluruh ornamen desain kosmetik Bootstrap CSS.
- **Akar Cikal Bakal:** Pintu gerbang Nginx mencari pakaian kosmetik pelayan file desainnya pada lemarin usang bernama path `/static/`; padahal si pengepul pemulung *Collectstatic* Django sengaja asik menjahit  serta membuang koleksinya menjauh pada kardus simpanan laci khusus penampung julukan komandan `/staticfiles/`.
- **Solusi Mutlak:** Ubah pemetaan GPS nya!: `sudo nano /etc/nginx/sites-available/simkos`. Ganti luruskan ujung pelabuhan terminal target pengalamatan pointer Nginx menjadi mutlak lurus `alias /var/www/SIMKOS/staticfiles/;`. Setelah sukses tervalidasi tekan Save, kembalikan kesadaran Pintu Gerbang Web Nginx via perintah `sudo systemctl restart nginx`.  Website 100% cantik bersolek kembali.

### 🚩 KASUS 6: Loading Melingkar Timeout Tanpa Henti Sama Sekali (Website Tak Bereaksi!)
- **Tampilan Visual:** Jari user Anda mengklik URL berformat Secure Enkripsi pelindung yakni murni tulisan hijau `https://...` namun seketika laju penziarah web tersebut hanya sekadar berputar menggulung tak berujung (Timeout Putih), ia mangkrak mendiam tak melepaskan pesan tulisan log Nomor Error (Mau itu 502/ Ataupun 504 secuilpun dari mesin Nginx).
- **Akar Cikal Bakal:** Anda terburu ngintip membuka kunci pelindung `https://` yang memaksimalkan jalur lalulintas rel Aman tingkat keras (Port nomer 443). SEDANGKAN pada celah pintu masuk Mesin Nginx Server sana.. ia **sama-sekali mentah polos** alias belum ditanamkan **Pusaka Pelindung Certbot SSL**. Oleh karenya Mesin Nginx otomatis melintir bisu bungkam menolak bertatap muka menajawab percakapan dengan pengunjung. 
- **Solusi Mutlak:** Bikin Gembok Asli Let's Enycrpt peneguh nya:  Jalankan satu mantra baris tembakan maut kebenaran penyelesainya mutlak `sudo certbot --nginx -d simkos.serpgroup.cloud`.

### 🚩 KASUS 7: Terminal Marah ERROR TULISAN MERAH: `Unit simkos.service not found!`
- **Tampilan Visual:** Berniat hati riang mengeksekusi mereset peladen gunicorn riang tapi seketika berbalik tamparan "Gagal Restart!" alias pesang cengang  `Not found`.
- **Akar Cikal Bakal:** Linux Sistem (Ubuntu) bersikap sangat apatis tak peduli karena ia buta atas kehadiran skrip guncorn systemd di balik kepergian Anda saat Anda baru usai merekat ketik di Terminal Nano editornya.
- **Solusi Mutlak:** Semprot air cipratan pengaget sel saraf pembangun deteksi Linux:  `sudo systemctl daemon-reload`. Serta Merta habisa Anda mengagetkan alam memori Linux, Linux jadi memindai tersadar; maka ketikkan ulang paksa kembali mantranya perintah penjalanan `Restart` Anda di awal. System Berjalan 100%.

### 🚩 KASUS 8: PERSIMPANGAN KABEL BENTROK : `ln: failed to create symlink / File Exists`
- **Tampilan Visual:** Ketikan pesinggungan Error keras *File Exists*.
- **Akar Cikal Bakal:** Sistem Operatur Induk Linux memukul balik takaran niat tali anyaman siluman Nginx Baru Anda karena dia menolak mempoligami celah slot hubung "Satu Nama Unik Spesial" yang di mana sejatinya tali nama "Simkos/ClS" yg sudah telanjur nyangkut tercantol bodong sejak penancapan pertama (Padahal isinya cacat/kosong) yang lalu!.
- **Solusi Mutlak:** Ambil arit putuskan dulu sambuntgan Tali Bodong lama: `sudo rm /etc/nginx/sites-enabled/simkos`. Hilang lenyap bersih tuntas tiada tersisa. Maka barulah Anda mematenkan penganyaman lurus aman kembali bebas bentrok via: (`sudo ln -s /etc/.../` )

### 🚩 KASUS 9: Label Logo Aset Merek Perusahaan Membisu Tidak Berganti 
- **Tampilan Visual:** Numpang kesal!, Logo Branding PT. Lawas yang Usang lusuh menyedihkan sekonyong-konyong tertinggal tak kunjung sirna ganti,  keterlaluan padahal Anda yakin tombol raksaa Hijau berbunyi "*Save Sukses Pengaturan Form Formullir*" terang di klik jelas.
- **Akar Cikal Bakal:** Salahkan lah sifat bawaan luhue  penyakit kotoran sumbatan di selokan ingatan sesaat otak sistem Django: *Caching Framework Memory*.
- **Solusi Mutlak:** Terabas dengan paksa memukul rubuh arsitektur kotoran tersebut via kodingan Pembumi-Hangusan Caching pada File VSCODE Windows lokal Anda!: Selipkan mantara sintaks penggerak  `cache.delete('ctx_pengaturan_perusahaan')` bertaruh lurus menempel tegak pada titik celah setelah fungsi pemanggil penyelamatan database utama  `.save()` berada, bersemayam menempati pilar skript kodingan fungsi utama pengendali tampilan `views.py`. Push Punggah Repositorinya ke Github, dan Tarik ulang di Terminal VPS. Gunicorn Restart, Logo Berubah Selamanya Indah! 

---

✅ **DOKUMEN SIAP PRODUKSI MASSAL.**
*(Terus ciptakan sistem terpadu SaaS multi-klien di hadapan Anda memedomani Kitab Sakti eksklusif ini!)*
