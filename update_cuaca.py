import requests
import xml.etree.ElementTree as ET

# URL data prakiraan cuaca BMKG untuk wilayah Jawa Tengah (misal)
url = "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KabupatenBlora.xml"

def ambil_cuaca():
    try:
        response = requests.get(url)
        response.raise_for_status()  # pastikan respon OK

        root = ET.fromstring(response.content)

        # Cari lokasi Kedungtuban (kode/stasiun sesuai di XML)
        # Di XML BMKG, nama lokasi biasanya di tag <area> dengan atribut 'description'
        lokasi_target = "Kedungtuban"

        cuaca_hari_ini = ""
        cuaca_besok = ""

        # Cari area yang sesuai lokasi
        for area in root.findall(".//area"):
            desc = area.get("description", "")
            if lokasi_target.lower() in desc.lower():
                # Ambil parameter cuaca untuk hari ini dan besok
                # Biasanya di tag <parameter> dengan atribut id="weather"
                # Dan waktu di tag <timerange>

                # Kita ambil dua timerange pertama (hari ini dan besok)
                weather_params = area.findall(".//parameter[@id='weather']/timerange")
                if len(weather_params) >= 2:
                    cuaca_hari_ini = weather_params[0].find("value").text
                    cuaca_besok = weather_params[1].find("value").text

                break

        # Map kode cuaca ke deskripsi (sederhana)
        kode_cuaca = {
            "0": "Cerah",
            "1": "Cerah Berawan",
            "2": "Cerah Berawan",
            "3": "Berawan",
            "4": "Berawan Tebal",
            "5": "Udara Kabur",
            "10": "Asap",
            "45": "Kabut",
            "60": "Hujan Ringan",
            "61": "Hujan Sedang",
            "63": "Hujan Lebat",
            "80": "Hujan Lokal",
            "95": "Hujan Petir",
        }

        hari_ini_text = kode_cuaca.get(cuaca_hari_ini, "Cuaca Tidak Diketahui")
        besok_text = kode_cuaca.get(cuaca_besok, "Cuaca Tidak Diketahui")

        hasil = f"Kedungtuban, Blora\nHari ini: {hari_ini_text}\nBesok: {besok_text}"

        # Simpan ke file cuaca.txt
        with open("cuaca.txt", "w", encoding="utf-8") as f:
            f.write(hasil)

        print("Berhasil update cuaca:")
        print(hasil)

    except Exception as e:
        print("Gagal ambil atau proses data cuaca:", e)

if __name__ == "__main__":
    ambil_cuaca()
