import matplotlib.pyplot as plt
import numpy as np
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
from scipy.stats import rankdata
import pandas as pd


def get_close_list(instrument="USD_JPY"):
    """
        get close values by oanda api v20
    """
    api = API(
        access_token="********",    # your access token
        environment="live") # or practice

    params = {
        "granularity": "M1",
        "count": 50,
        "price": "B",
    }

    instruments_candles = instruments.InstrumentsCandles(
        instrument=instrument, params=params)

    api.request(instruments_candles)
    response = instruments_candles.response
    close_list = np.array([x["bid"]["c"] for x in response["candles"]])
    close_list = close_list.astype(np.float64)
    return close_list


def get_logarithmic_change_rate(instrument):
    """
        get close values and convert it to logarithmic change rate
    """

    close_list = get_close_list(instrument)
    logarithmic_change_rate = np.log(close_list/close_list[0])
    
    return logarithmic_change_rate

# Get the logarithmic change rate for each currency pair
# eur
eurusd = get_logarithmic_change_rate("EUR_USD")
eurjpy = get_logarithmic_change_rate("EUR_JPY")
euraud = get_logarithmic_change_rate("EUR_AUD")
eurgbp = get_logarithmic_change_rate("EUR_GBP")

# usd
usdjpy = get_logarithmic_change_rate("USD_JPY")
audusd = get_logarithmic_change_rate("AUD_USD")
gbpusd = get_logarithmic_change_rate("GBP_USD")

# gbp
gbpjpy = get_logarithmic_change_rate("GBP_JPY")
gbpaud = get_logarithmic_change_rate("GBP_AUD")

# aud
audjpy = get_logarithmic_change_rate("AUD_JPY")


# compute ku-chart
ku_aud = (euraud * (-1)) + audusd + (gbpaud * (-1)) + audjpy
ku_eur = euraud + eurusd + eurgbp + eurjpy
ku_gbp = (eurgbp * (-1)) + gbpusd + gbpjpy + gbpaud
ku_jpy = eurjpy * (-1) + (gbpjpy * (-1)) +(audjpy * (-1)) + (usdjpy * (-1))
ku_usd = (eurusd * (-1)) + (audusd * (-1)) + (gbpusd * (-1)) + usdjpy

# plot ku-chart
fig, ax = plt.subplots()
x = np.arange(len(ku_aud))
ax.plot(x, ku_aud, label="aud")
ax.plot(x, ku_eur, label="eur")
ax.plot(x, ku_gbp, label="gbp")
ax.plot(x, ku_jpy, label="jpy")
ax.plot(x, ku_usd, label="usd")

ax.legend()
plt.savefig("ku-chart.png")
plt.show()
