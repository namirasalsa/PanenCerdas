import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def barchart_hasil_panen_per_tahun_provinsi_x(provinsi):
    # Load data
    df = pd.read_csv('https://storage.googleapis.com/panen-cerdas-bucket/dataset/data.csv')
    df['Total Panen'] = df['Produksi'] * df['Luas Panen']

    # Filter data berdasarkan provinsi dan tahun
    df_provinsi = df[df['Provinsi'] == provinsi].groupby('Tahun')['Total Panen'].sum().reset_index()
    df_provinsi = df_provinsi[(df_provinsi['Tahun'] >= 2011) & (df_provinsi['Tahun'] <= 2020)]

    plt.figure(figsize=(14, 8))

    # Palet warna tunggal (warna yang ditentukan)
    bar_color = '#a7d09f'
    
    sns.barplot(
        x='Tahun', 
        y='Total Panen', 
        data=df_provinsi,
        color=bar_color,
        alpha=0.85
    )
    
    for i, val in enumerate(df_provinsi['Total Panen']):
        plt.text(i, val + val * 0.02, f'{val:,}', ha='center', va='bottom', fontsize=10, color='black')

    # Tambahkan detail plot
    plt.title(f'Total Panen di Provinsi {provinsi} per Tahun', fontsize=16, fontweight='bold')
    plt.xlabel('Tahun', fontsize=12)
    plt.ylabel('Total Panen', fontsize=12)
    plt.xticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Simpan hasil plot ke dalam folder static/savefig
    save_dir = os.path.join("static", "savefig")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    output_path = os.path.join(save_dir, "hasil_panen_per_tahun_provinsi.png")
    
    plt.savefig(output_path)
    plt.close()
    
    return output_path