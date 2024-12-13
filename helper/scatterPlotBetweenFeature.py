import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Scatter plot fitur A dengan B pada provinsi X
def scatterplot_fitur_a_dengan_b_provinsi_x(provinsi, fitur_b, fitur_a="Produksi"):
    try:
        # Memuat dataset
        df = pd.read_csv('https://storage.googleapis.com/panen-cerdas-bucket/dataset/data.csv')
        df['Total Panen'] = df['Produksi'] * df['Luas Panen']

        # Filter data untuk provinsi tertentu
        df_provinsi = df[df['Provinsi'] == provinsi]
        
        # Validasi data
        if df_provinsi.empty:
            raise ValueError(f"Tidak ada data untuk Provinsi {provinsi}.")
        
        if fitur_a not in df_provinsi.columns or fitur_b not in df_provinsi.columns:
            raise ValueError(f"Kolom {fitur_a} atau {fitur_b} tidak ditemukan dalam data.")

        # Membuat folder jika belum ada
        save_path = "static/savefig"
        os.makedirs(save_path, exist_ok=True)
        
        # Scatter plot
        plt.figure(figsize=(14, 8))
        sns.scatterplot(
            x=fitur_a, 
            y=fitur_b, 
            data=df_provinsi, 
            hue='Tahun',  # Gunakan hue yang sesuai
            palette='viridis', 
            alpha=0.85
        )
        
        # Menambahkan label dan judul
        plt.title(f'Scatter Plot {fitur_a} dan {fitur_b} di Provinsi {provinsi}', fontsize=16, fontweight='bold')
        plt.xlabel(fitur_a, fontsize=12)
        plt.ylabel(fitur_b, fontsize=12)
        plt.xticks(fontsize=10)
        plt.grid(axis='both', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Menyimpan gambar
        file_path = os.path.join(save_path, "scatter_plot_fitur_a_dengan_b_provinsi_x.png")
        plt.savefig(file_path)
        plt.close()
        
        return file_path
    except Exception as e:
        print(f"Error: {e}")
        raise
