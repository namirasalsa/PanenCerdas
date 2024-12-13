import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Load One-Hot Encoder
with open('./helper/ohe.pkl', 'rb') as f:
    ohe = pickle.load(f)

def generateHistoricalDataComparison(new_data, hasil_prediksi):
    new_data['Provinsi'] = new_data.pop('provinsi')  # Ubah nama 'provinsi' menjadi 'Provinsi'
    new_data['Tahun'] = new_data.pop('tahun')  # Ambil dari payload

    # Load data historis
    df_test = pd.read_csv('https://storage.googleapis.com/panen-cerdas-bucket/dataset/data_test.csv')

    # Filter berdasarkan provinsi dan tahun
    df_test_provinsi = df_test[df_test['Provinsi'] == new_data['Provinsi']]
    df_test_provinsi = df_test_provinsi[df_test_provinsi['Tahun'].isin([2018, 2019, 2020])]

    # Tambahkan prediksi ke dalam data baru
    new_data['Prediksi Produksi'] = hasil_prediksi['estimasi_hasil_panen']
    new_data['Aktual Produksi'] = 0  # Untuk data baru, nilai aktual default adalah 0

    # Konversi new_data menjadi DataFrame
    new_data_df = pd.DataFrame([new_data])

    # Encode provinsi menggunakan One-Hot Encoder
    provinsi_encoded = ohe.transform(new_data_df[['Provinsi']])
    prov = ohe.get_feature_names_out(['Provinsi'])
    provinsi_encoded_df = pd.DataFrame(provinsi_encoded, columns=prov)
    
    # Gabungkan hasil encoding dengan DataFrame
    new_data_df = pd.concat([new_data_df, provinsi_encoded_df], axis=1)

    # Tentukan nama provinsi berdasarkan kolom hasil encoding
    new_data_df['Provinsi'] = new_data_df[prov].idxmax(axis=1).apply(lambda x: x.split('_')[1])
    new_data_df.drop(columns=prov, inplace=True)

    # Gabungkan data historis dengan data baru
    df_test_provinsi = pd.concat([df_test_provinsi, new_data_df], ignore_index=True)

    # Ubah data ke format long untuk plotting
    df_melt = df_test_provinsi.melt(
        id_vars='Tahun', 
        value_vars=['Aktual Produksi', 'Prediksi Produksi'],
        var_name='Kategori', 
        value_name='Produksi'
    )

    # Plot data historis dan prediksi
    plt.figure(figsize=(14, 8))

    # Warna khusus untuk bar
    custom_palette = {
        'Aktual Produksi': '#a7d09f',  # Warna hijau lembut
        'Prediksi Produksi': '#b2b9a6' # Warna abu kehijauan
    }

    sns.barplot(
        x='Tahun', 
        y='Produksi', 
        hue='Kategori', 
        data=df_melt,
        palette=custom_palette,
        dodge=True
    )

    # Menambahkan angka pada bar chart
    for p in plt.gca().patches:
        plt.text(
            p.get_x() + p.get_width() / 2,  # Posisi horizontal di tengah bar
            p.get_height() + 1,            # Posisi vertikal di atas bar
            f'{p.get_height():,.0f}',      # Format angka (tanpa desimal, dengan koma pemisah)
            ha='center',                   # Horizontal alignment
            va='bottom',                   # Vertical alignment
            fontsize=10, color='black'     # Ukuran dan warna teks
        )

    # Format plot
    plt.title(f'Perbandingan dengan Data Historis {new_data["Provinsi"]}', fontsize=16, fontweight='bold')
    plt.xlabel('Tahun', fontsize=12)
    plt.ylabel('Produksi (ton)', fontsize=12)
    plt.legend(title='Kategori', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Simpan gambar
    return plt.savefig('static/savefig/prediksi_produksi_padi.png')