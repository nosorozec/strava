import requests
import pandas as pd
import numpy as np
import io

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

def get_eur_chart() -> io.BufferedIOBase:
    last=100
    url = f"http://api.nbp.pl/api/exchangerates/rates/A/EUR/last/{last}"
    payload = {}
    response = requests.request("GET", url, data=payload)

    df = pd.DataFrame.from_dict(response.json()['rates'])
    df['effectiveDate'] = pd.to_datetime(df['effectiveDate'], format="%Y-%m-%d")

    plt.plot(np.linspace(-last+1, 0, last), df['mid'], color='blue')
    plt.title("EUR/PLN")
    plt.xlabel("Days")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf
