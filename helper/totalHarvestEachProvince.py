import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv('https://storage.googleapis.com/panen-cerdas-bucket/dataset/data.csv')
df['Total Panen'] = df['Produksi'] * df['Luas Panen']

df_provinsi = df.groupby(['Provinsi', 'Tahun'])['Total Panen'].sum().reset_index()

def barchart_each_provinsi_based_on_tahun(df, tahun):
    # Filter data berdasarkan tahun
    df_tahun = df[df['Tahun'] == tahun].sort_values('Total Panen', ascending=False)
    plt.figure(figsize=(14, 8))
    
    # Palet warna tunggal (warna yang ditentukan)
    bar_color = '#a7d09f'
    
    sns.barplot(
        x='Provinsi',
        y='Total Panen', 
        data=df_tahun, 
        color=bar_color,  # Terapkan warna ke semua bar
        alpha=0.85
    )
    
    for i, val in enumerate(df_tahun['Total Panen']):
        plt.text(i, val + val * 0.02, f'{val:,}', ha='center', va='bottom', fontsize=10, color='black')

    # Menambahkan detail plot
    plt.title(f'Total Panen Setiap Provinsi di Tahun {tahun}', fontsize=16, fontweight='bold')
    plt.xlabel('Provinsi', fontsize=12)
    plt.ylabel('Total Panen', fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Path penyimpanan file ke dalam folder static/savefig
    save_dir = os.path.join("static", "savefig")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    output_path = os.path.join(save_dir, "barchart_each_provinsi_based_on_tahun.png")
    
    plt.savefig(output_path)
    plt.close()