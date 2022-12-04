# Development Guidelines

## Chapter 1 - Initial Setup

1. Pastikan komputer telah terinstall **Docker** (dengan **docker-compose**) dan **DBeaver** (atau sejenisnya untuk melihat database)
2. Clone repository ini (menggunakan flag **--recursive**), misal ke folder **FashionCampus**
3. Jalankan perintah untuk memasang database pada **chapter 3 langkah 1**

## Chapter 2 - Development

1. Selalu kerjakan pada branch **dev-{username}**
2. Seluruh handler untuk tiap API endpoint terdapat pada folder **api/**
3. Seluruh model untuk mengakses database terdapat pada folder **model/**
4. Apabila ingin menggunakan module yang ada di project, bisa gunakan sebagai contoh:
    - `import FashionCampus.database`
    - `from FashionCampus.model import User, Buyer, Seller`
5. Apabila sudah selesai, bisa langsung build dan test dengan menjalankan **chapter 3 langkah 1** dan seterusnya (apabila service masih berjalan, shutdown terlebih dahulu sebagaimana pada **chapter 3 langkah 7**)
6. Apabila semuanya sudah bekerja, commit dan push ke GitHub (pastikan commit message jelas dan tidak ambigu supaya mudah dilacak apabila terdapat kebutuhan)

## Chapter 3 - Build & Testing

1. Build (jika ada perubahan pada source code / jika baru pertama kali) dengan perintah
    - Database: `docker-compose build fashion-campus-db`
    - Backend: `docker-compose build fashion-campus-api`
    - Frontend: `docker-compose build fashion-campus-app`
2. Jalankan service database, backend, dan frontend dengan perintah `docker-compose up -d`
3. Isi database dengan dummy data, dengan perintah `docker-compose exec fashion-campus-api python -m FashionCampus.database.seeder`
4. API bisa diakses melalui **http://localhost:8000**. Gunakan **Postman**, **Insomnia**, atau sejenisnya untuk melakukan testing. Dan frontend pada **http://localhost:3000**
5. Log (apabila terdapat error, debug, dan lain-lain) bisa dilihat dengan perintah `docker-compose logs fashion-campus-api`
6. Database bisa dilihat pada DBeaver (atau sejenisnya) dengan kredensial sebagai berikut:
    - Host: **localhost**
    - Port: **5432** (pastikan port ini tidak terpakai sebelumnya)
    - Database: **fashion_campus**
    - Username: **fashion_campus_user**
    - Password: **fashion_campus_password**
7. Apabila sudah selesai, service dapat di-shutdown dengan perintah `docker-compose down` (perintah ini juga harus dijalankan apabila ingin me-restart service khususnya apabila terdapat perubahan dalam source code)

# Deployment

1. Download required files yang ada di https://drive.google.com/drive/folders/1NpYG0jWZkT2r3kgRFHUp4_1f2NCSD021?usp=share_link terlebih dahulu dan letakkan sesuai lokasinya di project
2. Jalankan `docker-compose up -d`
3. Buka `http://localhost:3000` pada browser

# Shortcuts

**Notes.** Perintah-perintah di bawah hanya dapat berjalan pada sistem operasi Linux atau sejenisnya

- Apabila terdapat perubahan kode pada backend, jalankan saja perintah `make reload`
- Apabila terdapat perubahan kode pada frontend, jalankan saja perintah `make reload-app`
- Untuk melakukan seeding, jalankan `make seed`
- Untuk melihat log (khususnya pada API), jalankan `make log`
- Untuk melakukan testing AI prediction, jalankan `make test` dan inputkan nama file yang terdapat di folder **nn/data/external_fashion_dataset/**
