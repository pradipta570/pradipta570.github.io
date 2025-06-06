import requests
import xml.etree.ElementTree as ET

URL = "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaTengah.xml"

def parse_cuaca_kedungtuban():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        xml_data = response.content

        root = ET.fromstring(xml_data)

        # Cari area Kedungtuban
        area = None
        for a in root.findall(".//area"):
            if a.attrib.get('description', '').lower() == 'kedungtuban':
                area = a
                break
        if area is None:
            return "Area Kedungtuban tidak ditemukan"

        # Ambil parameter cuaca (weather) hari ini dan besok
        weather_params = area.findall("parameter[@id='weather']")
        cuaca_list = []
        for param in weather_params:
            values = param.findall("timerange[@h='00']/value")
            if not values:
                values = param.findall("value")
            for i, val in enumerate(values[:2]):
                kode_cuaca = val.text
                deskripsi = cuaca_kode_to_deskripsi(kode_cuaca)
                cuaca_list.append(deskripsi)

        if len(cuaca_list) < 2:
            return "Data cuaca tidak lengkap"

        hasil = f"Hari ini: {cuaca_list[0]}\nBesok: {cuaca_list[1]}"
        return hasil

    except Exception as e:
        return f"Error: {e}"

def cuaca_kode_to_deskripsi(kode):
    mapping = {
        '0': 'Cerah',
        '1': 'Cerah Berawan',
        '2': 'Cerah Berawan',
        '3': 'Berawan',
        '4': 'Mendung',
        '5': 'Mendung Tebal',
        '10': 'Asap',
        '45': 'Kabut',
        '60': 'Hujan Ringan',
        '61': 'Hujan Sedang',
        '63': 'Hujan Lebat',
        '70': 'Salju',
        '80': 'Hujan Lokal',
        '95': 'Hujan Petir',
    }
    return mapping.get(kode, 'Cuaca Tidak Diketahui')

def simpan_ke_file(nama_file="cuaca.txt"):
    hasil_cuaca = parse_cuaca_kedungtuban()
    with open(nama_file, "w", encoding="utf-8") as f:
        f.write(hasil_cuaca)
    print(f"File '{nama_file}' berhasil diperbarui.")

if __name__ == "__main__":
    simpan_ke_file()
