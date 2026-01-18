import pandas as pd

df = pd.read_json("data/data_sekolah.json")
jumlah_awal = len(df)

df = df.dropna(subset=['akreditasi'])
df = df[(df['latitude'] != 0.0) & (df['longitude'] != 0.0)]

jumlah_akhir = len(df)

df.to_json("data/data_sekolah_clean.json", orient="records", indent=4)  

print(f"\nTotal data awal: {jumlah_awal}")
print(f"Total data akhir: {jumlah_akhir}")