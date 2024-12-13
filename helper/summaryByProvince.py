# Fungsi untuk membuat ringkasan provinsi tertentu
def summary_provinsi_x(df, provinsi):
    # Filter data berdasarkan provinsi
    df_provinsi = df[df['Provinsi'] == provinsi]

    # Periksa apakah data provinsi tersedia
    if df_provinsi.empty:
        return {"status": "error", "message": f"Tidak ada data untuk provinsi {provinsi}"}

    # Hitung ringkasan
    summary = {
        "status": "success",
        "provinsi": provinsi,
        "tahun_terbaik": int(df_provinsi.loc[df_provinsi['Total Panen'].idxmax(), 'Tahun']),
        "panen_terbaik": int(df_provinsi['Total Panen'].max()),
        "total_panen_2010_2020": int(df_provinsi[(df_provinsi['Tahun'] >= 2010) & (df_provinsi['Tahun'] <= 2020)]['Total Panen'].sum()),
        "panen_rata_rata": round(df_provinsi['Total Panen'].mean(), 2),
        "luas_panen_rata_rata": round(df_provinsi['Luas Panen'].mean(), 2),
        "produksi_rata_rata": round(df_provinsi['Produksi'].mean(), 2),
        "curah_hujan_rata_rata": round(df_provinsi['Curah hujan'].mean(), 2),
        "kelembapan_rata_rata": round(df_provinsi['Kelembapan'].mean(), 2),
        "suhu_rata_rata": round(df_provinsi['Suhu rata-rata'].mean(), 2),
    }
    return summary