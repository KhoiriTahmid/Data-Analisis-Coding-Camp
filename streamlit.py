import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Daftar stasiun pemantauan polusi yang tersedia
files = [
    "Average", "Aotizhongxin", "Changping", "Dingling", "Dongsi",
    "Guanyuan", "Gucheng", "Huairou", "Nongzhanguan",
    "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"
]

# Memuat data CSV ke dalam dictionary
data = {}
for file in files:
    data[file] = pd.read_csv(f'./data/{file}.csv')
    data[file]['year_month'] = pd.to_datetime(data[file]['year_month'])
    data[file].set_index('year_month', inplace=True)

# Judul aplikasi di Streamlit
st.title("📊 Analisis Pertumbuhan Polusi")

# Dropdown untuk memilih stasiun pemantauan polusi
pollutant_selected = st.selectbox("Pilih Stasiun Polusi:", options=data.keys())

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📄 General Data", "📊 Pertumbuhan Bulanan", "📈 Pertumbuhan Tahunan"])

# --- TAB 1: General Data ---
with tab1:
    st.subheader("📄 Trend Polusi Berdasarkan Jenis")

    # Membuat grafik tren data time-series
    fig, ax = plt.subplots(figsize=(12, 6))
    data[pollutant_selected].plot(ax=ax)

    # Menggunakan skala logaritmik pada sumbu y
    ax.set_yscale("log")
    custom_ticks = [1, 5, 10, 50, 100, 200, 500, 1000]
    ax.set_yticks(custom_ticks)
    ax.set_yticklabels([str(tick) for tick in custom_ticks])

    # Menambahkan label dan grid pada grafik
    ax.set_title(f"Tren Polusi (2013 - 2017) - {pollutant_selected}")
    ax.set_xlabel("Waktu")
    ax.set_ylabel("Tingkat Polusi")
    ax.grid(True, linestyle="--", linewidth=0.5)
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))

    # Menampilkan grafik di Streamlit
    st.pyplot(fig)

    # Menampilkan tabel data mentah
    st.write('📄 Data dalam Tabel')
    st.dataframe(data[pollutant_selected])

# --- Menghitung Pertumbuhan Bulanan & Tahunan ---
monthly_growth = data[pollutant_selected].pct_change().multiply(100).mean()
yearly_growth = data[pollutant_selected].resample('YE').mean().pct_change().multiply(100).mean()

# --- TAB 2: Pertumbuhan Bulanan ---
with tab2:
    st.subheader("Ringkasan Pertumbuhan Bulanan")

    # Menampilkan card pertumbuhan bulanan
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="📆 Rata-rata Pertumbuhan  (%)", value=f"{monthly_growth.mean():.2f}%", border=True)

    with col2:
        st.metric(label="📈 Pertumbuhan  Tertinggi (%)", value=f"{monthly_growth.max():.2f}% {monthly_growth.idxmax()}", border=True)

    with col3:
        st.metric(label="📉 Pertumbuhan  Terendah (%)", value=f"{monthly_growth.min():.2f}%", border=True)

    # Bar Plott Pertumbuhan Bulanan
    st.subheader("Pertumbuhan Bulanan (%)")
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_growth.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_ylabel("Pertumbuhan (%)")
    ax.set_title("Rata-rata Pertumbuhan Bulanan per Jenis Polusi")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# TAB 3: Pertumbuhan Tahunan 
with tab3:
    st.subheader("Ringkasan Pertumbuhan Tahunan")

    # Menampilkan bar pertumbuhan tahunan
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="📆 Rata-rata Pertumbuhan  (%)", value=f"{yearly_growth.mean():.2f}%", border=True)

    with col2:
        st.metric(label="📈 Pertumbuhan  Tertinggi (%)", value=f"{yearly_growth.max():.2f}%", border=True)

    with col3:
        st.metric(label="📉 Pertumbuhan  Terendah (%)", value=f"{yearly_growth.min():.2f}%", border=True)

    # Bar Plot Pertumbuhan Tahunan
    st.subheader("Pertumbuhan Tahunan (%)")
    fig, ax = plt.subplots(figsize=(10, 5))
    yearly_growth.plot(kind="bar", ax=ax, color="orange")
    ax.set_ylabel("Pertumbuhan (%)")
    ax.set_title("Rata-rata Pertumbuhan Tahunan per Jenis Polusi")
    plt.xticks(rotation=45)
    st.pyplot(fig)
