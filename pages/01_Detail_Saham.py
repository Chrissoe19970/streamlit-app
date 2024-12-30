import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import linregress
import streamlit as st

st.title("Detail Saham")

ticker = st.text_input("Masukkan kode saham:", "AALI.JK")

if ticker:
    data = yf.download(ticker, period="6mo", interval="1d")  # Data 6 bulan terakhir, interval daily
    if not data.empty:
        data = data.tail(90)  # Tampilkan 90 hari terakhir

        st.write(f"### Data OHLC untuk {ticker} (90 Hari Terakhir)")
        st.write(data)

        # Perhitungan Slope Eksponensial dan Adjusted Slope
        data['Log_Close'] = np.log(data['Close'])
        x = np.arange(len(data))
        slope, intercept, r_value, _, _ = linregress(x, data['Log_Close'])
        r_squared = r_value**2
        annual_slope = (np.exp(slope * 252) - 1) * 100
        adjusted_slope = annual_slope * r_squared

        # Perhitungan Price Change (%) dan Geometric Mean (%)
        price_change = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
        price_change = float(price_change)  # Ubah ke scalar float

        daily_returns = data['Close'].pct_change().dropna()
        geometric_mean = (np.prod(1 + daily_returns))**(1 / len(daily_returns)) - 1
        geometric_mean_percentage = float(geometric_mean * 100)  # Ubah ke scalar float

        # Menampilkan Hasil Perhitungan
        st.write("### Hasil Perhitungan")
        st.write(f"- **Slope Eksponensial**: {slope:.6f}")
        st.write(f"- **R²**: {r_squared:.6f}")
        st.write(f"- **Annualized Slope (%)**: {annual_slope:.2f}")
        st.write(f"- **Adjusted Slope (%)**: {adjusted_slope:.2f}")
        st.write(f"- **Price Change (%)**: {price_change:.2f}")
        st.write(f"- **Geometric Mean (%)**: {geometric_mean_percentage:.2f}")

        # Menampilkan Grafik Harga Close
        st.write("### Grafik Harga Penutupan (Close)")
        st.line_chart(data['Close'])

    else:
        st.write(f"Tidak ada data untuk {ticker}.")
