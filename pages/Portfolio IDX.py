import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st

st.title("Perbandingan Portofolio dengan IHSG")

tickers_input = st.text_input(
    "Masukkan kode ticker saham, dipisahkan dengan koma (contoh: AALI.JK, BBCA.JK):", "BBCA.JK, PANI.JK, GOTO.JK"
)
weights_input = st.text_input(
    "Masukkan bobot masing-masing ticker, dipisahkan dengan koma (contoh: 0.5, 0.5):", "0.33, 0.33, 0.33"
)

if st.button("Bandingkan"):
    tickers = [ticker.strip() for ticker in tickers_input.split(",")]
    try:
        weights = [float(weight.strip()) for weight in weights_input.split(",")]
    except ValueError:
        st.error("Bobot harus berupa angka dan dipisahkan dengan koma.")
        st.stop()

    if len(tickers) != len(weights):
        st.error("Jumlah ticker dan bobot harus sama.")
        st.stop()

    if not np.isclose(sum(weights), 1.0):
        st.error("Total bobot harus sama dengan 1.")
        st.stop()

    st.write("Mengunduh data...")
    portfolio_data = yf.download(tickers, period="6mo", interval="1d")["Close"]
    ihsg_data = yf.download("^JKSE", period="6mo", interval="1d")["Close"]

    if portfolio_data.empty or ihsg_data.empty:
        st.error("Data tidak valid. Pastikan ticker yang dimasukkan benar dan memiliki data.")
        st.stop()

    portfolio_data = portfolio_data.fillna(method="ffill").fillna(method="bfill")
    ihsg_data = ihsg_data.fillna(method="ffill").fillna(method="bfill")

    if len(portfolio_data) < 90 or len(ihsg_data) < 90:
        st.warning("Data kurang dari 90 hari, perhitungan dilakukan berdasarkan data yang tersedia.")

    # Perhitungan return
    portfolio_returns = portfolio_data.pct_change().dropna()
    ihsg_returns = ihsg_data.pct_change().dropna()

    # Menghitung return portofolio berbasis bobot
    weighted_returns = portfolio_returns.dot(weights)
    cumulative_portfolio = (1 + weighted_returns).cumprod()

    cumulative_ihsg = (1 + ihsg_returns).cumprod()

    # Pastikan cumulative_portfolio dan cumulative_ihsg adalah 1D
    cumulative_portfolio = cumulative_portfolio.squeeze()
    cumulative_ihsg = cumulative_ihsg.squeeze()

    # Membuat DataFrame perbandingan
    comparison_df = pd.DataFrame({
        "Portofolio": cumulative_portfolio,
        "IHSG": cumulative_ihsg
    })

    st.write("Grafik Perbandingan Portofolio dan IHSG")
    st.line_chart(comparison_df)
