import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

def get_eur_chart() -> io.BufferedIOBase:
    last=100
    url = f"http://api.nbp.pl/api/exchangerates/rates/A/EUR/last/{last}"
    payload = {}
    response = requests.request("GET", url, data=payload)

    print(response.status_code)

    df = pd.DataFrame.from_dict(response.json()['rates'])
    df['effectiveDate'] = pd.to_datetime(df['effectiveDate'], format="%Y-%m-%d")

    plt.plot(np.linspace(-last+1, 0, last), df['mid'])
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    return buf
