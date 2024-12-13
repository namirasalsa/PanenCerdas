import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Barchart data iklim di Provinsi X
def line_plot_data_iklim_provinsi_x(provinsi):
    try:
        # Baca data dari URL
        df = pd.read_csv('https://storage.googleapis.com/panen-cerdas-bucket/dataset/data.csv')
        df['Total Panen'] = df['Produksi'] * df['Luas Panen']

        # Filter data berdasarkan provinsi dan tahun
        df_provinsi = df[df['Provinsi'] == provinsi]
        df_provinsi = df_provinsi[(df_provinsi['Tahun'] >= 2011) & (df_provinsi['Tahun'] <= 2020)]

        # Pastikan data tidak kosong
        if df_provinsi.empty:
            raise ValueError(f"Tidak ada data untuk Provinsi {provinsi}.")

        # Pastikan kolom yang dibutuhkan ada
        required_columns = ['Tahun', 'Curah hujan', 'Suhu rata-rata', 'Kelembapan']
        missing_columns = [col for col in required_columns if col not in df_provinsi.columns]
        if missing_columns:
            raise ValueError(f"Kolom berikut hilang dari data: {', '.join(missing_columns)}")

        # Buat visualisasi
        plt.figure(figsize=(14, 8))
        sns.lineplot(
            x='Tahun', 
            y='Curah hujan', 
            data=df_provinsi, 
            label='Curah Hujan', 
            marker='o', 
            color='#2baf11'  # Warna baru untuk Curah Hujan
        )
        sns.lineplot(
            x='Tahun', 
            y='Suhu rata-rata', 
            data=df_provinsi, 
            label='Suhu Rata-rata', 
            marker='o', 
            color='#148600'  # Warna baru untuk Suhu Rata-rata
        )
        sns.lineplot(
            x='Tahun', 
            y='Kelembapan', 
            data=df_provinsi, 
            label='Kelembapan', 
            marker='o', 
            color='#ff7900'  # Warna baru untuk Kelembapan
        )

        # Atur detail plot
        plt.title(f'Perubahan Iklim di Provinsi {provinsi}', fontsize=16, fontweight='bold')
        plt.xlabel('Tahun', fontsize=12)
        plt.ylabel('Nilai Iklim (Curah Hujan, Suhu, Kelembapan)', fontsize=12)
        plt.xticks(df_provinsi['Tahun'].unique(), fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()

        # Buat folder jika belum ada
        output_folder = 'static/savefig'
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, 'line_plot_data_iklim_provinsi_x.png')

        # Simpan plot
        plt.savefig(output_path)
        plt.clf()
        plt.close()

        # Kembalikan path file
        return output_path

    except Exception as e:
        print(f"Error (line_plot_data_iklim_provinsi_x): {e}")
        raise