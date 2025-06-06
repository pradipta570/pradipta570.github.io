import requests
import xml.etree.ElementTree as ET

url = "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-KabupatenBlora.xml"

def kode_cuaca_ke_text(kode):
    mapping = {
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
    return mapping.get(kode, "Cuaca Tidak Diketahui")

def ambil_cuaca():
    response = requests.get(url)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    lokasi_target = "Kedungtuban"
    cuaca_hari_ini = None
    cuaca_besok = None

    for area in root.findall(".//area"):
        desc = area.get("description", "")
        if lokasi_target.lower() in desc.lower():
            weather_param = area.find("parameter[@id='weather']")
            if weather_param is not None:
                timerange_list = weather_param.findall("timerange")
                if len(timerange_list) >= 2:
                    cuaca_hari_ini = timerange_list[0].find("value").text
                    cuaca_besok = timerange_list[1].find("value").text
            break

    if cuaca_hari_ini is None or cuaca_besok is None:
        return "Data cuaca tidak lengkap"

    hasil = f"Kedungtuban, Blora\nHari ini: {kode_cuaca_ke_text(cuaca_hari_ini)}\nBesok: {kode_cuaca_ke_text(cuaca_besok)}"
    return hasil

if __name__ == "__main__":
    try:
        cuaca_text = ambil_cuaca()
        with open("cuaca.txt", "w", encoding="utf-8") as f:
            f.write(cuaca_text)
        print("File cuaca.txt berhasil diperbarui:")
        print(cuaca_text)
    except Exception as e:
        print("Error:", e)
