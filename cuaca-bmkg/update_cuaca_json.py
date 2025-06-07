import requests
import datetime

URL = "https://ibnux.github.io/BMKG-importer/cuaca/kab/Kabupaten_Blora.json"
LOKASI = "Kedungtuban"

def ambil_data_cuaca():
    try:
        response = requests.get(URL, timeout=10)
        data = response.json()
        return [item for item in data if item["kota"].lower() == LOKASI.lower()]
    except Exception as e:
        print("Gagal ambil data:", e)
        return []

def ringkas_cuaca_esp(data):
    if not data:
        return "Gagal ambil cuaca"

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    cuaca_today = next((d for d in data if d["jamCuaca"].startswith(str(today))), None)
    cuaca_tomorrow = next((d for d in data if d["jamCuaca"].startswith(str(tomorrow))), None)

    teks = f"{LOKASI}: "
    teks += cuaca_today["cuaca"] if cuaca_today else "?"
    teks += ", Besok: "
    teks += cuaca_tomorrow["cuaca"] if cuaca_tomorrow else "?"

    return teks

def simpan_ke_file(teks):
    with open("cuaca.txt", "w", encoding="utf-8") as f:
        f.write(teks)
    print("Berhasil simpan cuaca.txt:", teks)

def main():
    data = ambil_data_cuaca()
    teks = ringkas_cuaca_esp(data)
    simpan_ke_file(teks)

if __name__ == "__main__":
    main()
