import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    hour_df = pd.read_csv("hour.csv")
    day_df = pd.read_csv("day.csv")
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    return hour_df, day_df

hour_df, day_df = load_data()

# Filter data untuk tahun terakhir (2012)
latest_year = hour_df['dteday'].dt.year.max()
hour_df_last_year = hour_df[hour_df['dteday'].dt.year == latest_year]

# Streamlit Dashboard
st.title("📊 Dashboard Analisis Penyewaan Sepeda 🚴‍♂️")

## **Visualisasi 1: Pola Penggunaan Sepeda Berdasarkan Jam**
st.subheader("Pola Penggunaan Sepeda Berdasarkan Jam dalam Hari Biasa, Akhir Pekan, dan Hari Libur")

fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=hour_df_last_year, 
    x="hr", 
    y="cnt", 
    hue="workingday", 
    style="holiday", 
    errorbar=None,
    markers=True, 
    dashes=False,
    ax=ax1
)

ax1.set_title("Pola Penggunaan Sepeda Berdasarkan Jam dalam Hari Biasa, Akhir Pekan, dan Hari Libur (2012)")
ax1.set_xlabel("Jam dalam Sehari")
ax1.set_ylabel("Jumlah Penyewa")
ax1.set_xticks(range(0, 24))
ax1.legend(title="Kategori", labels=["Akhir Pekan", "Hari Libur", "Hari Biasa"])
ax1.grid(True)

st.pyplot(fig1)

## **Visualisasi 2: Pengaruh Cuaca terhadap Penyewaan Sepeda**
st.subheader("Pengaruh Cuaca terhadap Jumlah Penyewa Sepeda Berdasarkan Musim")

# Mapping nama musim
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
day_df['season'] = day_df['season'].map(season_mapping)

# Mapping kondisi cuaca
weather_mapping = {
    1: "Clear/Few Clouds",
    2: "Mist/Cloudy",
    3: "Light Snow/Rain",
    4: "Heavy Rain/Snow"
}
day_df['weathersit'] = day_df['weathersit'].map(weather_mapping)

fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.boxplot(
    data=day_df, 
    x="season", 
    y="cnt", 
    hue="weathersit",
    palette="Set2",
    ax=ax2
)

ax2.set_title("Pengaruh Cuaca terhadap Jumlah Penyewa Sepeda Berdasarkan Musim")
ax2.set_xlabel("Musim")
ax2.set_ylabel("Jumlah Penyewa Sepeda")
ax2.legend(title="Kondisi Cuaca")
ax2.grid(axis="y")

st.pyplot(fig2)

## **Visualisasi 3: Perbandingan Pengguna Terdaftar vs Tidak Terdaftar (2011 vs 2012)**
st.subheader("Perbandingan Pengguna Terdaftar dan Tidak Terdaftar (2011 vs 2012)")

# Mapping tahun
year_mapping = {0: 2011, 1: 2012}
day_df['yr'] = day_df['yr'].map(year_mapping)

# Agregasi jumlah penyewa berdasarkan tahun
user_type_yearly = day_df.groupby("yr")[["casual", "registered"]].sum()

fig3, axes = plt.subplots(1, 2, figsize=(12, 6))

for i, year in enumerate(user_type_yearly.index):
    axes[i].pie(
        user_type_yearly.loc[year], 
        labels=["Casual", "Registered"], 
        autopct="%1.1f%%", 
        colors=["#ff9999", "#66b3ff"],
        startangle=90,
        wedgeprops={"edgecolor": "black"}
    )
    axes[i].set_title(f"Persentase Pengguna Sepeda - {year}")

plt.suptitle("Perbandingan Pengguna Terdaftar dan Tidak Terdaftar (2011 vs 2012)")
st.pyplot(fig3)