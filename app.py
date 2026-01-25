import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.title("Analisis Peta Persebaran SMA di Bandung Raya & Sumedang")

df = pd.read_json("data/data_sekolah_clean.json")

data_list = df.to_dict(orient="records")

st.subheader("Data Sekolah")
st.dataframe(df)

m = folium.Map(location=[-6.9147, 107.6098], zoom_start=12)

marker_cluster = MarkerCluster().add_to(m)

for sekolah in data_list:
    bentuk = sekolah["bentuk_pendidikan"].upper()

    if bentuk == "SMA":
        warna = "blue"
    elif bentuk =="SMK":
        warna = "red"
    elif bentuk == "SMAK":
        warna = "yellow"
    else:
        warna = "green"

    html_content = f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 10px; line-height: 1.4;">
        <h5 style="margin: 0 0 10px 0; color: {warna}; font-size: 16px;">{sekolah['nama_sekolah']}</h5>
        <table style="width: 100%; font-size: 12px; border-collapse: collapse;">
            <tr>
                <td style="vertical-align: top; font-weight: bold; width: 60px; padding-bottom: 5px;">Status</td>
                <td style="vertical-align: top; padding-bottom: 5px;">: {sekolah['status']}</td>
            </tr>
            <tr>
                <td style="vertical-align: top; font-weight: bold;">Alamat</td>
                <td style="vertical-align: top; color: #555;">: {sekolah['alamat']}, {sekolah['wilayah']}</td>
            </tr>
            <tr>
                <td style="vertical-align: top; font-weight: bold; padding-top: 5px;">Akreditasi</td>
                <td style="vertical-align: top; padding-top: 5px;">: {sekolah['akreditasi']}</td>
            </tr>
        </table>
    </div>
    """

    iframe = folium.IFrame(html_content, width=300, height=180)
    popup = folium.Popup(iframe, max_width=300)


    folium.Marker(
        location=[sekolah["latitude"], sekolah["longitude"]],
        popup=popup,
        icon=folium.Icon(color=warna, icon="university", prefix="fa")
    ).add_to(marker_cluster) 

st_folium(m, use_container_width=True)