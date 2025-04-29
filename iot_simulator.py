import time, random

def get_sensor_data():
    return {
        "temperature": round(random.uniform(18, 30), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "energy_kwh": round(random.uniform(1, 10), 2)
    }

if __name__ == '__main__':
    while True:
        print(get_sensor_data())
        time.sleep(2)
