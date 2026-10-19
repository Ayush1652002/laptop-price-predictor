import pickle
import numpy as np
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pipe = pickle.load(open(os.path.join(BASE_DIR, "pipe.pkl"), "rb"))

def predict_price(data: dict) -> int:
    company = data["company"]
    type_name = data["type"]
    ram = int(data["ram"])
    weight = float(data["weight"])
    touchscreen = 1 if data["touchscreen"] == "Yes" else 0
    ips = 1 if data["ips"] == "Yes" else 0
    screen_size = float(data["screen_size"])
    resolution = data["resolution"]
    cpu = data["cpu"]
    hdd = int(data.get("hdd", 0))
    ssd = int(data.get("ssd", 512))
    gpu = data["gpu"]
    os_name = data["os"]

    x_res = int(resolution.split("x")[0])
    y_res = int(resolution.split("x")[1])
    ppi = ((x_res ** 2) + (y_res ** 2)) ** 0.5 / screen_size

    query = pd.DataFrame([[
        company,
        type_name,
        ram,
        weight,
        touchscreen,
        ips,
        ppi,
        cpu,
        hdd,
        ssd,
        gpu,
        os_name
    ]], columns=[
        "Company",
        "TypeName",
        "Ram",
        "Weight",
        "Touchscreen",
        "Ips",
        "PPI",
        "Cpu_brand",
        "HDD",
        "SSD",
        "Gpu_Brand",
        "os"
    ])

    predicted_log = pipe.predict(query)[0]
    return int(np.exp(predicted_log))