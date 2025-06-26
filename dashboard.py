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
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    return hour_df, day_df

hour_df, day_df = load_data()

# Streamlit Dashboard
st.title("📊 Dashboard Analisis Penyewaan Sepeda 🚴‍♂️")

# Sidebar - Filter
st.sidebar.header("🔎 Filter Data")
years_selected = st.sidebar.multiselect("Pilih Tahun:", options=[2011, 2012], default=[2012])

if not years_selected:
    st.warning("⚠️ Mohon pilih minimal satu tahun untuk menampilkan visualisasi.")
    st.stop()

# Mapping season & weather
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_mapping = {
    1: "Clear/Few Clouds",
    2: "Mist/Cloudy",
    3: "Light Snow/Rain",
    4: "Heavy Rain/Snow"
}
season_order = ["Spring", "Summer", "Fall", "Winter"]
weather_order = ["Clear/Few Clouds", "Mist/Cloudy", "Light Snow/Rain", "Heavy Rain/Snow"]
custom_palette = {
    "Clear/Few Clouds": "#66c2a5",
    "Mist/Cloudy": "#fc8d62",
    "Light Snow/Rain": "#8da0cb",
    "Heavy Rain/Snow": "#e78ac3"
}

day_df['season'] = day_df['season'].map(season_mapping)
day_df['weathersit'] = day_df['weathersit'].map(weather_mapping)
day_df['yr'] = day_df['dteday'].dt.year
hour_df['yr'] = hour_df['dteday'].dt.year

# Filtering berdasarkan tahun yang dipilih
day_filtered = day_df[day_df['yr'].isin(years_selected)]
hour_filtered = hour_df[hour_df['yr'].isin(years_selected)]

# Sidebar tambahan: Filter season dan cuaca
season_options = sorted(day_filtered['season'].dropna().unique(), key=lambda x: season_order.index(x))
weather_options = sorted(day_filtered['weathersit'].dropna().unique(), key=lambda x: weather_order.index(x))
selected_season = st.sidebar.multiselect("Pilih Musim:", season_options, default=season_options)
selected_weather = st.sidebar.multiselect("Pilih Kondisi Cuaca:", weather_options, default=weather_options)

# Terapkan filter season dan cuaca
day_filtered = day_filtered[
    (day_filtered['season'].isin(selected_season)) &
    (day_filtered['weathersit'].isin(selected_weather))
]

# === VISUALISASI 1 ===
st.subheader("Pola Penggunaan Sepeda Berdasarkan Jam dalam Hari Biasa, Akhir Pekan, dan Hari Libur")

fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=hour_filtered, 
    x="hr", 
    y="cnt", 
    hue="workingday", 
    style="holiday", 
    errorbar=None,
    markers=True, 
    dashes=False,
    ax=ax1
)

title_str = " & ".join(str(y) for y in years_selected)
ax1.set_title(f"Pola Penggunaan Sepeda Berdasarkan Jam ({title_str})")
ax1.set_xlabel("Jam dalam Sehari")
ax1.set_ylabel("Jumlah Penyewa")
ax1.set_xticks(range(0, 24))
ax1.legend(title="Kategori", labels=["Akhir Pekan", "Hari Libur", "Hari Biasa"])
ax1.grid(True)
st.pyplot(fig1)

# === VISUALISASI 2 ===
st.subheader("Pengaruh Cuaca terhadap Jumlah Penyewa Sepeda Berdasarkan Musim")

agg_weather = day_filtered.groupby(['season', 'weathersit'])['cnt'].mean().reset_index()

fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.barplot(
    data=agg_weather,
    x="season",
    y="cnt",
    hue="weathersit",
    order=season_order,
    hue_order=weather_order,
    palette=custom_palette,
    ax=ax2
)

ax2.set_title(f"Rata-rata Jumlah Penyewa Berdasarkan Musim dan Cuaca ({title_str})")
ax2.set_xlabel("Musim")
ax2.set_ylabel("Rata-rata Jumlah Penyewa")
ax2.legend(title="Kondisi Cuaca")
ax2.grid(axis="y")
st.pyplot(fig2)

# === VISUALISASI 3 ===
st.subheader("Perbandingan Pengguna Terdaftar dan Tidak Terdaftar")

user_type_yearly = day_df[day_df['yr'].isin(years_selected)].groupby("yr")[["casual", "registered"]].sum()

fig3, axes = plt.subplots(1, len(user_type_yearly), figsize=(6 * len(user_type_yearly), 6))

if len(user_type_yearly) == 1:
    axes = [axes]  # buat jadi list jika hanya satu tahun

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

st.pyplot(fig3)
