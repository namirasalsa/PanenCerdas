import requests
import os
import dotenv
dotenv.load_dotenv()
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify

import google.generativeai as genai

from helper.historicalDataComparison import generateHistoricalDataComparison
from helper.totalHarvestEachProvince import barchart_each_provinsi_based_on_tahun, df_provinsi
from helper.scatterPlotBetweenFeature import scatterplot_fitur_a_dengan_b_provinsi_x
from helper.ClimateVisualization import line_plot_data_iklim_provinsi_x
from helper.totalHarvestByProvince import barchart_hasil_panen_per_tahun_provinsi_x
from helper.summaryByProvince import summary_provinsi_x

api_key= os.environ.get("APIKEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-pro")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/prediksi")
def prediksi():
    return render_template("prediksi.html")

@app.route("/generate_chart", methods=["POST"])
def generate_chart():
    try:
        # Ambil input tahun dari request
        tahun = int(request.form.get("tahun"))

        # Generate chart berdasarkan tahun
        barchart_each_provinsi_based_on_tahun(df_provinsi, tahun)

        # Kirim path file gambar sebagai respons (sesuaikan dengan path untuk frontend)
        output_path = "static/savefig/barchart_each_provinsi_based_on_tahun.png"
        return jsonify({"status": "success", "image_path": output_path})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
@app.route("/generate_scatterplot", methods=["POST"])
def generate_scatterplot():
    try:
        # Ambil input dari request
        provinsi = request.form.get("provinsi")
        fitur_a = request.form.get("fitur_a")
        fitur_b = request.form.get("fitur_b")
        
        # Generate scatter plot
        output_path = scatterplot_fitur_a_dengan_b_provinsi_x(provinsi, fitur_a, fitur_b)
        
        # Kirim path file gambar sebagai respons
        return jsonify({"status": "success", "image_path": output_path})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
@app.route("/generate_climate_plot", methods=["POST"])
def generate_climate_plot():
    try:
        # Ambil input provinsi dari request
        provinsi = request.form.get("provinsi")

        # Generate plot data iklim berdasarkan provinsi
        output_path = "static/savefig/line_plot_data_iklim_provinsi_x.png"
        line_plot_data_iklim_provinsi_x(provinsi)

        # Kirim path file gambar sebagai respons
        return jsonify({"status": "success", "image_path": output_path})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
@app.route("/generate_harvest_chart_by_province", methods=["POST"])
def generate_harvest_chart_by_province():
    try:
        # Ambil input provinsi dari request
        provinsi = request.form.get("provinsi")

        # Generate barchart untuk provinsi tertentu
        output_path = barchart_hasil_panen_per_tahun_provinsi_x(provinsi)

        # Kirim path file gambar sebagai respons
        return jsonify({"status": "success", "image_path": output_path})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
@app.route("/get_summary_by_province", methods=["POST"])
def get_summary_by_province():
    try:
        # Ambil provinsi dari request
        provinsi = request.form.get("provinsi")

        # Load dataset
        df = pd.read_csv('https://storage.googleapis.com/panen-cerdas-bucket/dataset/data.csv')
        df['Total Panen'] = df['Produksi'] * df['Luas Panen']

        # Gunakan fungsi summary_provinsi_x dengan argumen dataset
        summary = summary_provinsi_x(df, provinsi)

        # Jika status error, kirimkan pesan error
        if summary["status"] == "error":
            return jsonify(summary)

        # Kirim ringkasan sebagai JSON
        return jsonify(summary)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/hasil", methods=["POST"])
def hasil():
    # Ambil data dari form
    tahun = int(request.form.get("tahun"))
    provinsi = request.form.get("provinsi")
    luas_panen = float(request.form.get("luas_panen"))
    curah_hujan = float(request.form.get("curah_hujan"))
    kelembapan = float(request.form.get("kelembapan"))
    suhu_rata_rata = float(request.form.get("suhu"))

    # Siapkan payload untuk API eksternal
    payload = {
        "tahun": int(tahun),
        "provinsi": provinsi,
        "luas_panen": int(luas_panen),
        "curah_hujan": int(curah_hujan),
        "kelembapan": int(kelembapan),
        "suhu_rata_rata": float(suhu_rata_rata)
    }

    # Kirim request ke API eksternal
    try:
        response = requests.post("https://asia-southeast2-panencerdas.cloudfunctions.net/panen-cerdas-predict-gcf", json=payload)
        response.raise_for_status()  # Raise error jika ada masalah pada request
        hasil_prediksi = response.json()

        generateHistoricalDataComparison(payload, hasil_prediksi)
        
        gemini_recommendation = model.generate_content(
        f'Prediksi produksi padi di {provinsi} pada tahun {tahun} adalah {hasil_prediksi} kg. Buatlah rekomendasinya singkat dan jelas dalam 1 paragraf'
        )

        # gemini_recommendation = model.generate_content(f'Prediksi produksi padi di {provinsi} pada tahun {tahun} adalah {hasil_prediksi} kg. Buatlah rekomendasinya singkat dan jelas dalam 1 paragraf.')
    except requests.exceptions.RequestException as e:
        hasil_prediksi = {"error": str(e)}

    # Kirim hasil ke template hasil.html
    return render_template("hasil.html", hasil=hasil_prediksi, data=payload, recommendation=gemini_recommendation)

if __name__ == "__main__":
    app.run(debug=True)
