import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# KONFIGURASI HALAMAN HARUS DI PALING AWAL
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Membaca dataset
try:
    archive = pd.read_csv('all_data.csv')  # Sesuaikan nama file
    st.success("Dataset berhasil dimuat!")
    st.write(archive.head())  # Menampilkan 5 baris pertama untuk memastikan data benar
except FileNotFoundError:
    st.error("File tidak ditemukan! Periksa kembali lokasi file.")
    st.stop()  # Menghentikan eksekusi jika dataset tidak ada

# Judul Dashboard
st.title("Bike Sharing Dashboard 🚴‍♂️")

# Menampilkan data
st.subheader("Data Day dan Data Hour")
st.write(archive)

# Menampilkan visualisasi barchart "Total Penyewaan Sepeda Berdasarkan Musim"
st.header("Total Penyewaan Sepeda Berdasarkan Musim")

# Pastikan kolom 'season' ada
if 'season' in archive.columns and 'cnt' in archive.columns:
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    archive['season'] = archive['season'].map(season_mapping)
    season_counts = archive.groupby('season')['cnt'].sum()

    plt.figure(figsize=(8, 5))
    sns.barplot(x=season_counts.index, y=season_counts.values, palette="Blues")
    plt.title('Total Penyewaan Sepeda Berdasarkan Musim', fontsize=14)
    plt.xlabel('Musim', fontsize=12)
    plt.ylabel('Total Penyewaan', fontsize=12)
    st.pyplot(plt)
else:
    st.warning("Kolom 'season' atau 'cnt' tidak ditemukan di dataset!")

# Perbandingan Rata-rata Penyewaan Sepeda antara Hari Kerja dan Akhir Pekan
st.header("Perbandingan Rata-rata Penyewaan Sepeda antara Hari Kerja dan Akhir Pekan")

if 'workingday' in archive.columns and 'cnt' in archive.columns:
    ratarata_pengguna = archive.groupby('workingday')[['cnt', 'casual', 'registered']].mean().reset_index()
    
    plt.figure(figsize=(8, 5))
    sns.barplot(x='workingday', y='cnt', data=ratarata_pengguna, palette=['skyblue', 'orange'])
    plt.xlabel("Kategori Hari", fontsize=12)
    plt.ylabel("Rata-rata Jumlah Penyewaan", fontsize=12)
    plt.title("Perbandingan Rata-rata Penyewaan Sepeda\nantara Hari Kerja dan Akhir Pekan", fontsize=14)
    plt.xticks(ticks=[0, 1], labels=["Akhir Pekan", "Hari Kerja"])
    st.pyplot(plt)
else:
    st.warning("Kolom 'workingday' atau 'cnt' tidak ditemukan di dataset!")

# Perbandingan Rata-rata Penyewaan Sepeda oleh Kasual dan Terdaftar
st.header("Perbandingan Rata-rata Penyewaan Sepeda oleh Kasual dan Terdaftar")

if 'casual' in archive.columns and 'registered' in archive.columns:
    avg_users_melted = ratarata_pengguna.melt(id_vars='workingday', value_vars=['casual', 'registered'], 
                                              var_name='User Type', value_name='Average Rentals')
    plt.figure(figsize=(8, 5))
    sns.barplot(x='workingday', y='Average Rentals', hue='User Type', data=avg_users_melted, palette=['skyblue', 'orange'])
    plt.xlabel("Kategori Hari", fontsize=12)
    plt.ylabel("Rata-rata Jumlah Penyewa", fontsize=12)
    plt.title("Perbandingan Rata-rata Penyewaan Sepeda oleh Kasual dan Terdaftar", fontsize=14)
    plt.legend(title="Tipe Pengguna")
    st.pyplot(plt)
else:
    st.warning("Kolom 'casual' atau 'registered' tidak ditemukan di dataset!")

# Footer
st.caption("📊 Dashboard Bike Sharing | Dibuat oleh Salsabila Mahiroh")
