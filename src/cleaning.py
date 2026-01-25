import pandas as pd
import time
from geopy.geocoders import ArcGIS
from geopy.exc import GeopyError
import os

file_utama = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_file = os.path.join(file_utama, "data", "data_sekolah.json")
output_file = os.path.join(file_utama, "data", "data_sekolah_clean.json")

if not os.path.exists(input_file):
    print(f"Eror: File {input_file} tidak ditemukan!")
    exit()

df = pd.read_json(input_file)
print(f"Memproses {len(df)} data...")

df['akreditasi'] = df['akreditasi'].fillna('Tidak Terdata').replace(['', '-', ' '], 'Tidak Terdata')

mask = (df['latitude'] == 0.0) | (df['longitude'] == 0.0)

koordinat_hilang = df[mask]

if not koordinat_hilang.empty:
    jumlah_hilang = len(koordinat_hilang)
    print(f"Ditemukan {len(koordinat_hilang)} koordinat hilang, sedang mencari koordinat...")

    geolocator = ArcGIS(user_agent="si-ganteng-kalem")

    for i in range(jumlah_hilang):
        idx = koordinat_hilang.index[i]

        nama = koordinat_hilang.iloc[i]['nama_sekolah']
        alamat = koordinat_hilang.iloc[i]['alamat']
        wilayah = koordinat_hilang.iloc[i]['wilayah']

        penggabungan = f"{alamat}, {wilayah}, Jawa Barat"
        print(f"Mencari lokasi Sekolah {nama}")

        try:
            lokasi = lokasi = geolocator.geocode(penggabungan, timeout=10)

            if lokasi:
                # Masukkan koordinat baru ke dataframe utama (df)
                df.at[idx, 'latitude'] = lokasi.latitude
                df.at[idx, 'longitude'] = lokasi.longitude
                print(f"Berhasil ditemukan!")
            else:
                print(f"Alamat tidak ditemukan di peta.")

            time.sleep(0.2)
        
        except GeopyError as e:
                print(f"Terjadi gangguan koneksi: {e}")

else:
     print("Semua koordinat sekolah sudah lengkap")

df.to_json(output_file, orient="records", indent=4)
print(f'\nProses Selesai. Data disimpan di {output_file}')