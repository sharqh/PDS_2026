import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman (Harus di baris pertama perintah Streamlit)
st.set_page_config(
    page_title="Dashboard Kinerja Karyawan",
    page_icon="📊",
    layout="wide"
)

# 2. Data Contoh (Sesuai dengan tabel Anda)
data = {
    "nama": ["Andi", "Budi", "Chandra", "Dudi", "Eko", "Fahri", "Gina", "Herman", "Indara", "Joni"],
    "jan": [100, 200, 300, 250, 150, 95, 125, 130, 320, 200],
    "feb": [135, 240, 315, 270, 195, 130, 175, 155, 374, 220],
    "mar": [85, 185, 285, 230, 110, 75, 110, 100, 300, 175],
    "apr": [75, 160, 190, 200, 100, 45, 70, 85, 270, 155]
}

df = pd.DataFrame(data)

# Hitung kolom total dan rata-rata per karyawan
df['total'] = df['jan'] + df['feb'] + df['mar'] + df['apr']
df['rata_rata'] = df['total'] / 4

# 3. Sidebar untuk Filter & Navigasi
st.sidebar.header("⚙️ Pengaturan Dashboard")
selected_karyawan = st.sidebar.multiselect(
    "Pilih Karyawan:",
    options=df["nama"].tolist(),
    default=df["nama"].tolist()
)

# Filter dataframe berdasarkan pilihan sidebar
df_filtered = df[df["nama"].isin(selected_karyawan)]

# 4. Judul Utama Dashboard
st.title("📊 Dashboard Analisis Kinerja Karyawan")
st.markdown("Dashboard interaktif untuk memantau performa bulanan (Januari - April).")
st.markdown("---")

# 5. Bagian KPI / Metrik Utama (Atas)
total_keseluruhan = df_filtered['total'].sum()
rata_keseluruhan = df_filtered['rata_rata'].mean() if not df_filtered.empty else 0
karyawan_terbaik = df_filtered.loc[df_filtered['total'].idxmax()]['nama'] if not df_filtered.empty else "-"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="💰 Total Penjualan / Kinerja", value=f"{total_keseluruhan:,}")
with col2:
    st.metric(label="📈 Rata-rata Per Karyawan", value=f"{rata_keseluruhan:.1f}")
with col3:
    st.metric(label="⭐ Karyawan Terbaik", value=karyawan_terbaik)

st.markdown("---")

# 6. Bagian Grafik Interaktif (Plotly)
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Perbandingan Kinerja per Bulan")
    if not df_filtered.empty:
        # Ubah format data dari wide ke long untuk grafik batang
        df_melted = df_filtered.melt(id_vars=["nama"], value_vars=["jan", "feb", "mar", "apr"], 
                                     var_name="Bulan", value_name="Nilai")
        fig_bar = px.bar(df_melted, x="Bulan", y="Nilai", color="nama", barmode="group",
                         title="Grafik Batang Kinerja Bulanan")
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Pilih minimal satu karyawan di sidebar.")

with col_chart2:
    st.subheader("🏆 Total Kontribusi Karyawan")
    if not df_filtered.empty:
        fig_pie = px.pie(df_filtered, names="nama", values="total", 
                         title="Persentase Kontribusi Total", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("Pilih minimal satu karyawan di sidebar.")

st.markdown("---")

# 7. Bagian Tabel Data Lengkap
st.subheader("📋 Tabel Detail Data Kinerja")
st.dataframe(df_filtered, use_container_width=True)
