import requests
import random
import time

API_URL = "http://127.0.0.1:8000/api/device/report/"  # адрес вашего Django API
DEVICE_ID = "ABCDEF0123456789"  # замените на реальный 16-символьный id устройства

def send_report(remaining_percent):
    payload = {
        "device_id": DEVICE_ID,
        "remaining_percent": remaining_percent,
    }
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        print("Отправлено:", payload)
        print("Ответ сервера:", response.status_code, response.json())
    except Exception as e:
        print("Ошибка при отправке:", e)

if __name__ == "__main__":
    # эмулируем несколько отчётов
    for _ in range(5):
        percent = random.randint(5, 100)  # случайный остаток филамента
        send_report(percent)
        time.sleep(2)  # пауза между запросами
