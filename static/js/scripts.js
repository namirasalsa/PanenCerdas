function updateChart() {
    // Ambil tahun dari dropdown
    const year = document.getElementById("year").value;

    // Kirim POST request ke backend untuk generate chart
    fetch("/generate_chart", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `tahun=${year}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // Update src gambar dengan path baru
            const chartImage = document.getElementById("chart-image");
            chartImage.src = `/${data.image_path}?timestamp=${new Date().getTime()}`; // Tambahkan timestamp untuk mencegah caching
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => console.error("Error:", error));
}

// Fungsi untuk memperbarui scatter plot
function updateScatterPlot() {
    // Ambil input dari dropdown
    const provinsi = document.getElementById("provinsi").value;
    const fiturB = document.getElementById("fitur-b").value;
    const fiturA = "Produksi"; // Fitur A tetap "Produksi"

    // Kirim POST request ke backend
    fetch("/generate_scatterplot", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `provinsi=${provinsi}&fitur_a=${fiturA}&fitur_b=${fiturB}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // Update src gambar dengan yang baru
            const scatterPlotImage = document.getElementById("scatter-plot-image");
            scatterPlotImage.src = `/${data.image_path}?t=${new Date().getTime()}`; // Hindari caching
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => console.error("Error:", error));
}

// Tambahkan event listener ke dropdown
document.getElementById("provinsi").addEventListener("change", updateScatterPlot);
document.getElementById("fitur-b").addEventListener("change", updateScatterPlot);

// Fungsi untuk memperbarui line plot data iklim
function updateClimatePlot() {
    // Ambil input dari dropdown
    const provinsi = document.getElementById("provinsi-iklim").value;

    // Kirim POST request ke backend
    fetch("/generate_climate_plot", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `provinsi=${provinsi}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // Update src gambar dengan yang baru
            const climatePlotImage = document.getElementById("climate-plot-image");
            climatePlotImage.src = `/${data.image_path}?t=${new Date().getTime()}`; // Hindari caching
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => console.error("Error:", error));
}

// Tambahkan event listener ke dropdown
document.getElementById("provinsi-iklim").addEventListener("change", updateClimatePlot);

// Fungsi untuk memperbarui barchart hasil panen berdasarkan provinsi
function updateHarvestChartByProvince() {
    // Ambil input provinsi dari dropdown
    const provinsi = document.getElementById("harvest-province").value;

    // Kirim POST request ke backend
    fetch("/generate_harvest_chart_by_province", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `provinsi=${provinsi}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // Update src gambar dengan path baru
            const harvestChartImage = document.getElementById("harvest-chart-image");
            harvestChartImage.src = `/${data.image_path}?timestamp=${new Date().getTime()}`; // Hindari caching
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => console.error("Error:", error));
}

// Tambahkan event listener ke dropdown
document.getElementById("harvest-province").addEventListener("change", updateHarvestChartByProvince);

// Fungsi untuk memperbarui ringkasan data berdasarkan provinsi
function updateSummaryByProvince() {
    const provinsi = document.getElementById("provinsi").value;

    // Kirim POST request ke backend
    fetch("/get_summary_by_province", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `provinsi=${provinsi}`
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.status === "success") {
            const summary = data;

            // Perbarui elemen HTML Ringkasan Data
            document.querySelector(".list-unstyled li:nth-child(1) span").innerText = summary.provinsi;
            document.querySelector(".list-unstyled li:nth-child(2) span").innerText = `Tahun terbaik: ${summary.tahun_terbaik}, total: ${summary.panen_terbaik.toLocaleString()}`;
            document.querySelector(".list-unstyled li:nth-child(3) span").innerText = `${summary.total_panen_2010_2020.toLocaleString()} (2010-2020)`;
            document.querySelector(".list-unstyled li:nth-child(4) span").innerText = `${summary.panen_rata_rata.toLocaleString()} ha`;
            document.querySelector(".list-unstyled li:nth-child(5) span").innerText = `${summary.curah_hujan_rata_rata.toLocaleString()} mm`;
            document.querySelector(".list-unstyled li:nth-child(6) span").innerText = `${summary.kelembapan_rata_rata} %`;
            document.querySelector(".list-unstyled li:nth-child(7) span").innerText = `${summary.suhu_rata_rata} °C`;
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => console.error("Error:", error));
}

document.getElementById("provinsi").addEventListener("change", updateSummaryByProvince);