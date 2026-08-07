# Laporan Akhir: Analisis Jejaring Sosial (Social Network Analysis)
**Studi Kasus: SNAP ego-Facebook Dataset (4.039 Node, 88.234 Edge)**

**Informasi Mahasiswa:**
- **Nama:** Bayu Samudra
- **NIM:** 2211310079
- **Kelas:** Teknologi Informasi 8c
- **Mata Kuliah:** Analisis Jejaring Sosial

---

## 1. Representasi Graf Jejaring Sosial
Jejaring sosial pertemanan Facebook yang dianalisis merupakan graf tidak berarah dan tidak berbobot (**Undirected and Unweighted Graph**).

### A. Komponen Jaringan
- **Node (Titik)**: Merepresentasikan akun pengguna Facebook ($N = 4.039$).
- **Edge (Sisi)**: Merepresentasikan jalinan pertemanan timbal-balik (mutual friendship) antar-pengguna ($M = 88.234$).
- **Sifat Hubungan**: Karena pertemanan di Facebook bersumber dari persetujuan kedua belah pihak (timbal-balik), maka hubungan tidak berarah (jika A berteman dengan B, maka B pasti berteman dengan A). Hubungan juga tidak berbobot karena tidak ada pengukuran intensitas komunikasi formal di dataset ini; setiap hubungan bernilai `1` jika berteman dan `0` jika tidak berteman.

### B. Contoh Matriks Adjacency (Ketetanggaan)
Matriks adjacency berukuran $5 \times 5$ dari 5 node pertama (Node ID 0 s.d 4):

$$
A = \begin{pmatrix}
0 & 1 & 1 & 1 & 1 \\
1 & 0 & 0 & 0 & 0 \\
1 & 0 & 0 & 0 & 0 \\
1 & 0 & 0 & 0 & 0 \\
1 & 0 & 0 & 0 & 0
\end{pmatrix}
$$

**Penjelasan Matriks:**
- Matriks bersifat **simetris** terhadap diagonal utama ($A_{i,j} = A_{j,i}$) karena graf bersifat tidak berarah.
- Diagonal utama bernilai `0` ($A_{i,i} = 0$) menunjukkan bahwa tidak ada pengguna yang berteman dengan dirinya sendiri (*no self-loops*).
- Baris pertama (Node 0) memiliki nilai `1` pada kolom 1, 2, 3, dan 4 ($A_{0,1} = A_{0,2} = A_{0,3} = A_{0,4} = 1$), yang menunjukkan bahwa Node ID 0 terhubung secara langsung dengan Node ID 1, 2, 3, dan 4. Sementara itu, Node ID 1 s.d 4 tidak saling terhubung di sub-graf $5 \times 5$ ini (bernilai `0`).

---

## 2. Analisis Sentralitas (Centrality Analysis)

Aktor penting diidentifikasi menggunakan empat metrik sentralitas utama. Di bawah ini adalah rumus formal dan hasil perhitungan 5 aktor terpenting pada masing-masing metrik:

### A. Rumus Matematis
1. **Degree Centrality**:
   $$C_D(i) = \frac{k_i}{N - 1}$$
   di mana $k_i$ adalah degree (jumlah hubungan langsung) node $i$ dan $N$ adalah jumlah node ($4.039$).
2. **Betweenness Centrality**:
   $$C_B(i) = \sum_{s \neq i \neq t} \frac{\sigma_{st}(i)}{\sigma_{st}}$$
   di mana $\sigma_{st}$ adalah total lintasan terpendek dari $s$ ke $t$, dan $\sigma_{st}(i)$ adalah jumlah lintasan terpendek yang melewati node $i$.
3. **Closeness Centrality**:
   $$C_C(i) = \frac{N - 1}{\sum_{j \neq i} d(i, j)}$$
   di mana $d(i, j)$ adalah jarak lintasan terpendek dari $i$ ke $j$.
4. **Eigenvector Centrality**:
   $$C_E(i) = \frac{1}{\lambda} \sum_{j} A_{i,j} C_E(j)$$
   di mana $A$ adalah matriks adjacency dan $\lambda$ adalah eigenvalue terbesar.

### B. Hasil Tabel 5 Aktor Terpenting
| Peringkat | Degree Centrality | Betweenness Centrality | Closeness Centrality | Eigenvector Centrality |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Node 107** <br> (Skor: 0.25879) | **Node 107** <br> (Skor: 0.48052) | **Node 107** <br> (Skor: 0.45970) | **Node 1912** <br> (Skor: 0.09541) |
| **2** | **Node 1684** <br> (Skor: 0.19614) | **Node 1684** <br> (Skor: 0.33780) | **Node 58** <br> (Skor: 0.39740) | **Node 2266** <br> (Skor: 0.08698) |
| **3** | **Node 1912** <br> (Skor: 0.18697) | **Node 3437** <br> (Skor: 0.23612) | **Node 428** <br> (Skor: 0.39484) | **Node 2206** <br> (Skor: 0.08605) |
| **4** | **Node 3437** <br> (Skor: 0.13546) | **Node 1912** <br> (Skor: 0.22930) | **Node 563** <br> (Skor: 0.39391) | **Node 2233** <br> (Skor: 0.08517) |
| **5** | **Node 0** <br> (Skor: 0.08593) | **Node 1085** <br> (Skor: 0.14902) | **Node 1684** <br> (Skor: 0.39361) | **Node 2464** <br> (Skor: 0.08428) |

### C. Analisis Peran Aktor Kunci
1. **Node 107 (Aktor Sentral Utama)**:
   Node 107 mendominasi tiga metrik utama: Degree (0.258), Betweenness (0.480), dan Closeness (0.459). Hal ini menunjukkan bahwa Node 107 terhubung langsung dengan $25.8\%$ anggota jaringan (1.045 teman langsung), mengontrol $48\%$ jalur komunikasi terpendek antaranggota lain, dan memiliki jarak rata-rata terdekat ke semua pengguna. Node 107 bertindak sebagai **"Super-Hub"** dan **"Broker Terkuat"** dalam jejaring Facebook ini.
2. **Node 1684 (Broker Sekunder)**:
   Memiliki Betweenness tertinggi kedua ($33.7\%$). Node ini sangat penting dalam menghubungkan sub-komunitas besar yang berbeda, bertindak sebagai gerbang informasi utama lintas batas kelompok.
3. **Node 1912 (Hub Kelompok Berpengaruh)**:
   Memiliki Eigenvector Centrality tertinggi ($0.09541$) meskipun derajat koneksinya berada di bawah Node 107. Ini menunjukkan bahwa Node 1912 berteman dengan sekelompok pengguna yang juga memiliki pengaruh tinggi dalam sistem pertemanan, menjadikannya sangat berpengaruh secara reputasional di wilayah *circle*-nya.

---

## 3. Karakteristik Jaringan Global & Deteksi Komunitas

Analisis makro dilakukan untuk mengungkap sifat keseluruhan dari struktur pertemanan ini.

### A. Metrik Global Jaringan
- **Density (Kerapatan Graf): 0.010820 (1.08%)**
  - *Interpretasi*: Hanya $1.08\%$ dari total hubungan yang mungkin terjadi yang benar-benar ada. Ini menunjukkan jaringan sangat renggang (*sparse*), wajar untuk jejaring sosial nyata berskala ribuan node.
- **Diameter: 8**
  - *Interpretasi*: Lintasan terpendek terjauh antara dua orang di jejaring sosial Facebook ini adalah 8 langkah. Ini berarti tidak ada dua pengguna yang terpisah lebih dari 8 hubungan pertemanan.
- **Average Path Length (Rata-rata Panjang Jalur): 3.6925 langkah**
  - *Interpretasi*: Rata-rata dua pengguna acak dalam jaringan Facebook ini hanya terpisah sejauh **~3.7 langkah**. Hal ini memverifikasi teori **"Six Degrees of Separation"** (dunia kecil), menunjukkan penyebaran informasi secara struktural sangat efisien.
- **Average Clustering Coefficient: 0.6055 (60.55%)**
  - *Interpretasi*: Angka $60.55\%$ sangat tinggi (jauh lebih tinggi dibanding density 1%). Ini membuktikan fenomena clustering sosial yang kuat: teman-teman dari seorang pengguna cenderung berteman satu sama lain membentuk kelompok padat (*clique*).

### B. Deteksi Komunitas (Algoritma Louvain)
- **Modularity (Modularitas): 0.8350**
  - *Interpretasi*: Nilai modularitas mendekati 1 menandakan jaringan terbagi secara tegas ke dalam kelompok-kelompok komunitas informal yang terpisah.
- **Jumlah Komunitas: 16 komunitas**
  - Dua komunitas terbesar terdeteksi sebagai **Komunitas 9 (548 node)** dan **Komunitas 4 (535 node)**. Kelompok-kelompok ini mencerminkan pengelompokan alamiah di dunia nyata seperti grup sekolah, universitas, kota asal, atau ketertarikan yang sama.

---

## 4. Simulasi Penyebaran Informasi

Penyebaran informasi (gosip, berita, kampanye) disimulasikan menggunakan model **Susceptible-Infected (SI)**.
- **Benih Awal (Seeds)**: Node 107 (Degree, Betweenness & Closeness Hub), Node 1912 (Eigenvector Hub), dan Node 4010 (Random Node).
- **Probabilitas Infeksi dasar ($\beta$)**: 0.08 (8% kemungkinan penyebaran per siklus).
- **Jumlah Simulasi**: 50 kali pengulangan independen untuk hasil rata-rata yang stabil.

### A. Kecepatan Penyebaran Informasi
- **Benih Node 107 (Degree, Betweenness & Closeness Hub)**:
  - Mencapai **50% populasi dalam 6 langkah** dan **90% populasi dalam 12 langkah**. Kecepatan penyebaran tercepat dan eksponensial.
- **Benih Node 1912 (Eigenvector Hub)**:
  - Mencapai **50% populasi dalam 8 langkah** dan **90% populasi dalam 15 langkah**. Cepat karena terhubung erat dengan kluster berderajat tinggi.
- **Benih Random Node (Node 4010)**:
  - **Tidak mencapai 50% maupun 90% populasi** dalam batas 20 langkah simulasi. Mengalami hambatan berat karena letak geografisnya yang terisolasi di pinggiran jaringan, sehingga informasi terperangkap di lingkungan lokal dan tidak mampu menembus ke inti jaringan untuk disebarkan secara massal.

### B. Analisis Peran Node Penting
Simulasi ini membuktikan bahwa aktor dengan sentralitas tinggi (khususnya *Degree* dan *Closeness*) berperan sebagai **akselerator utama** dalam penyebaran informasi. Memulai kampanye atau penyebaran informasi melalui **Node 107** memotong waktu penyebaran secara dramatis dibandingkan memilih pengguna secara acak yang rentan mengalami keterjebakan informasi di kelompok lokal.


---

## 5. Visualisasi Jejaring & Kesimpulan Karakteristik

### A. Visualisasi Graf
1. **Visualisasi Statis (`network_static.png`)**:
   Dibuat menggunakan `NetworkX` dan `Matplotlib` dengan algoritma *spring layout*. Warna node disesuaikan dengan 16 komunitas Louvain dan ukuran node disetel proporsional terhadap skor *Degree Centrality*. Aktor kunci seperti Node 107 tampak menonjol sebagai pusat gravitasi.
2. **Visualisasi Interaktif (`network_interactive.html`)**:
   Dibuat menggunakan `PyVis` dalam mode gelap. Untuk efisiensi performa browser, visualisasi ini memuat sub-graf pertemanan terdekat dari aktor sentral utama (Node 107, 1684, dan 1912). Anda dapat menggeser node, memperbesar gambar, dan mengarahkan kursor untuk melihat kartu informasi nama, komunitas, dan skor sentralitas masing-masing pengguna.

### B. Kesimpulan Akhir
Berdasarkan seluruh hasil analisis kuantitatif SNA, jejaring sosial Facebook SNAP ini merupakan **Scale-Free Network** dengan sifat **Small-World** yang sangat kuat serta pengelompokan lokal yang padat (*high clustering*). 

Aliran informasi di dalam jaringan ini sangat tersentralisasi pada beberapa aktor utama, terutama **Node 107**. Hal ini memberikan struktur komunikasi keunggulan berupa **kecepatan penyebaran informasi tinggi jika memanfaatkan aktor kunci**, namun di sisi lain memiliki **kerentanan yang parah terhadap fragmentasi** jika aktor-aktor utama tersebut tidak aktif atau dinonaktifkan dari jejaring.
