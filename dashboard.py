import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import datetime as dt
import calendar

from streamlit_gsheets import GSheetsConnection
from numerize.numerize import numerize

# Setup
st.set_page_config(
    # page_title="Jakarta Housing Prices Dashboard",
    layout="wide",
)

url = "https://docs.google.com/spreadsheets/d/1j59iQOTSbjn2XcGbcZSCLIXsHevil8OeKFmjkXXomFY/edit?usp=sharing"
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

reduce_header_height_style = """
    <style>
        div.block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)

st.markdown("""
    <style type="text/css">
    div[data-testid="stHorizontalBlock"] > div {
        border: 1.5px solid #e0e0e2;
        padding: 10px;
        margin: -5px;
        border-radius: 10px;
        background: transparent;
    }
    </style>
""", unsafe_allow_html=True)

metric_css = """
    [data-testid="metric-container"] {
        width: fit-content;
        margin: auto;
    }

    [data-testid="metric-container"] > div {
        width: fit-content;
        margin: auto;
    }

    [data-testid="metric-container"] label {
        width: fit-content;
        margin: auto;
    }
"""

# with st.sidebar:
#     st.write("A")

# Data loading
month_mapping = {
    "Jan": "Jan",
    "Feb": "Feb",
    "Mar": "Mar",
    "Apr": "Apr",
    "Mei": "May",
    "Jun": "Jun",
    "Jul": "Jul",
    "Ags": "Aug",
    "Sept": "Sep",
    "Okt": "Oct",
    "Nov": "Nov",
    "Des": "Dec"
}

# df_transaksi
df_transaksi_original = conn.read(spreadsheet=url, worksheet="0")
df_transaksi_original = df_transaksi_original.replace("-", np.nan)
# df_transaksi_original.columns = [j if "Unnamed" in i else i for i, j in zip(df_transaksi_original.columns, df_transaksi_original.iloc[0])]
# df_transaksi_original = df_transaksi_original.iloc[1:].reset_index(drop=True)

for old_month, new_month in month_mapping.items():
    df_transaksi_original["Tgl Terima"] = df_transaksi_original["Tgl Terima"].str.replace(old_month, new_month, regex=True)
df_transaksi_original["Tgl Terima"] = pd.to_datetime(df_transaksi_original["Tgl Terima"], format="%d %b %Y %H:%M")

for old_month, new_month in month_mapping.items():
    df_transaksi_original["Tgl Selesai"] = df_transaksi_original["Tgl Selesai"].str.replace(old_month, new_month, regex=True)
df_transaksi_original["Tgl Selesai"] = pd.to_datetime(df_transaksi_original["Tgl Selesai"], format="%d %b %Y %H:%M")

# df_snapclean
df_snapclean_original = conn.read(spreadsheet=url, worksheet="331647216")
df_snapclean_original = df_snapclean_original.replace("-", np.nan)
# df_snapclean_original.columns = [j if "Unnamed" in i else i for i, j in zip(df_snapclean_original.columns, df_snapclean_original.iloc[0])]
# df_snapclean_original.columns = df_snapclean_original.columns.str.strip()
# df_snapclean_original = df_snapclean_original.iloc[1:].reset_index(drop=True)

for old_month, new_month in month_mapping.items():
    df_snapclean_original["Tanggal Diterima"] = df_snapclean_original["Tanggal Diterima"].str.replace(old_month, new_month, regex=True)
df_snapclean_original["Tanggal Diterima"] = pd.to_datetime(df_snapclean_original["Tanggal Diterima"], format="%d %b %Y %H:%M")

for old_month, new_month in month_mapping.items():
    df_snapclean_original["Tanggal Selesai"] = df_snapclean_original["Tanggal Selesai"].str.replace(old_month, new_month, regex=True)
df_snapclean_original["Tanggal Selesai"] = pd.to_datetime(df_snapclean_original["Tanggal Selesai"], format="%d %b %Y %H:%M")

# df_pembayaran
df_pembayaran_original = conn.read(spreadsheet=url, worksheet="588904373")
df_pembayaran_original = df_pembayaran_original.replace("-", np.nan)
df_pembayaran_original.columns = [j if "Unnamed" in i else i for i, j in zip(df_pembayaran_original.columns, df_pembayaran_original.iloc[0])]
df_pembayaran_original = df_pembayaran_original.iloc[1:].reset_index(drop=True)

for old_month, new_month in month_mapping.items():
    df_pembayaran_original["Tanggal Pembuatan Nota"] = df_pembayaran_original["Tanggal Pembuatan Nota"].str.replace(old_month, new_month, regex=True)
df_pembayaran_original["Tanggal Pembuatan Nota"] = pd.to_datetime(df_pembayaran_original["Tanggal Pembuatan Nota"], format="%d %b %Y %H:%M")

for old_month, new_month in month_mapping.items():
    df_pembayaran_original["Waktu Bayar"] = df_pembayaran_original["Waktu Bayar"].str.replace(old_month, new_month, regex=True)
df_pembayaran_original["Waktu Bayar"] = pd.to_datetime(df_pembayaran_original["Waktu Bayar"], format="%d %b %Y %H:%M")

# df_pengerjaan
df_pengerjaan_original = conn.read(spreadsheet=url, worksheet="561410319")
df_pengerjaan_original = df_pengerjaan_original.replace("-", np.nan)
df_pengerjaan_original.columns = [j if "Unnamed" in i else i for i, j in zip(df_pengerjaan_original.columns, df_pengerjaan_original.iloc[0])]
df_pengerjaan_original = df_pengerjaan_original.iloc[1:].reset_index(drop=True)

for old_month, new_month in month_mapping.items():
    df_pengerjaan_original["Waktu Pengerjaan"] = df_pengerjaan_original["Waktu Pengerjaan"].str.replace(old_month, new_month, regex=True)
df_pengerjaan_original["Waktu Pengerjaan"] = pd.to_datetime(df_pengerjaan_original["Waktu Pengerjaan"], format="%d %b %Y %H:%M")

# df_biaya
df_biaya_original = conn.read(spreadsheet=url, worksheet="1750228284")
df_biaya_original = df_biaya_original.replace("-", np.nan)
df_biaya_original.columns = [j if "Unnamed" in i else i for i, j in zip(df_biaya_original.columns, df_biaya_original.iloc[0])]
df_biaya_original = df_biaya_original.iloc[1:].reset_index(drop=True)

for old_month, new_month in month_mapping.items():
    df_biaya_original["Tanggal Dibuat"] = df_biaya_original["Tanggal Dibuat"].str.replace(old_month, new_month, regex=True)
df_biaya_original["Tanggal Dibuat"] = pd.to_datetime(df_biaya_original["Tanggal Dibuat"], format="%d %b %Y %H:%M")

for old_month, new_month in month_mapping.items():
    df_biaya_original["Tanggal Pemakaian"] = df_biaya_original["Tanggal Pemakaian"].str.replace(old_month, new_month, regex=True)
df_biaya_original["Tanggal Pemakaian"] = pd.to_datetime(df_biaya_original["Tanggal Pemakaian"], format="%d %b %Y %H:%M")

# Title
st.markdown(f"<h1 style='text-align: center; margin-bottom: 20px;'>LAUNDRY DASHBOARD</h1>", unsafe_allow_html=True)

# Filters
st.markdown(f"<h3>🔍 Filters</h3>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    years = [int(i) for i in df_transaksi_original["Tahun"].unique()]
    years = sorted(years, reverse=True)
    selected_year = st.selectbox("Pilih Tahun", years, index=0)

with col2:
    periods = ["Harian", "Mingguan", "Bulanan"]
    selected_period = st.selectbox("Pilih Periode", periods, index=0)

if selected_period == "Harian":
    resample = "D"
elif selected_period == "Mingguan":
    resample = "W"
else:
    resample = "M"

current_year = dt.datetime.now().year

if selected_year != current_year:
    start_date_default = dt.datetime(selected_year, 1, 1)
    
    # Get the last day of December for the selected year
    last_day_dec = calendar.monthrange(selected_year, 12)[1]
    end_date_default = dt.datetime(selected_year, 12, last_day_dec)
else:
    start_date_default = dt.datetime(current_year, 1, 1)
    end_date_default = dt.datetime.now()  # Today's date

with col3:
    selected_date_range = st.date_input("Pilih Rentang Tanggal", [start_date_default, end_date_default])

with col4:
    outlets = df_transaksi_original["Outlet"].unique()
    default_outlet = ["Matahari Laundry Ciputat"]
    selected_outlet = st.selectbox("Pilih Outlet", outlets)

# Slicing
start_date = pd.Timestamp(selected_date_range[0])
end_date = pd.Timestamp(selected_date_range[1]).replace(hour=23, minute=59, second=59)

df_transaksi = df_transaksi_original[
    (df_transaksi_original["Tahun"] == selected_year) &
    (df_transaksi_original["Outlet"] == selected_outlet) &
    (df_transaksi_original["Tgl Terima"] >= start_date) &
    (df_transaksi_original["Tgl Terima"] <= end_date)
].copy()

df_snapclean = df_snapclean_original[
    (df_snapclean_original["Tahun"] == selected_year) &
    (df_snapclean_original["Outlet"] == selected_outlet) &
    (df_snapclean_original["Tanggal Diterima"] >= start_date) &
    (df_snapclean_original["Tanggal Diterima"] <= end_date)
].copy()

df_biaya = df_biaya_original[
    (df_biaya_original["Tahun"] == selected_year) &
    (df_biaya_original["Outlet"] == selected_outlet) &
    (df_biaya_original["Tanggal Dibuat"] >= start_date) &
    (df_biaya_original["Tanggal Dibuat"] <= end_date)
].copy()

# df_pembayaran = df_pembayaran_original[
#     (df_pembayaran_original["Tahun"] == selected_year) &
#     (df_pembayaran_original["Outlet"] == selected_outlets)
# ].copy()

# df_pengerjaan = df_pengerjaan_original[
#     (df_pengerjaan_original["Tahun"] == selected_year) &
#     (df_pengerjaan_original["Outlet"] == selected_outlets)
# ].copy()

st.empty()

# Metrics
st.markdown(f"<h3>📋 Overview</h3>", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(label="Jumlah Transaksi", value=df_transaksi["No Nota"].nunique(), delta=None)

with col2:
    st.metric(label="Total Pelanggan", value=df_transaksi["Customer"].nunique(), delta=None)

with col3:
    total_transaksi = int(np.sum(df_transaksi["Subtotal"] + df_transaksi["Tambahan Express"]))
    st.metric(label="Total Transaksi", value=f"Rp{numerize(total_transaksi, 1)}", delta=None)

with col4:
    omzet_transaksi = int(np.sum(df_transaksi["Subtotal"] + df_transaksi["Tambahan Express"] - df_transaksi["Diskon"] + df_transaksi["Pajak"]))
    st.metric(label="Omzet Transaksi", value=f"Rp{numerize(omzet_transaksi, 1)}", delta=None)

with col5:
    total_pengeluaran = int(df_biaya[df_biaya["Status"] == "Disetujui"]["Nominal Biaya"].sum())
    st.metric(label="Total Pengeluaran", value=f"Rp{numerize(total_pengeluaran, 1)}", delta=None)

st.empty()

# Charts
st.markdown(f"<h3>📊 Charts</h3>", unsafe_allow_html=True)

# Pendapatan & Pengeluaran
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<h5>Pendapatan</h5>", unsafe_allow_html=True)

    with st.expander("Klik di sini untuk melihat lebih detail"):
        pendapatan = pd.DataFrame({
            "Pendapatan": [
                "Pendapatan Transaksi",
                "Pendapatan SnapClean",
                "Diskon Transaksi Reguler"
            ],
            "Nominal": [
                df_transaksi["Subtotal"].sum(),
                df_snapclean["Total Tagihan"].sum(),
                df_transaksi["Diskon"].sum()
            ]
        })
        pendapatan = pendapatan.sort_values("Nominal", ascending=False).reset_index(drop=True)
        st.dataframe(pendapatan, use_container_width=True)

    income_without_tax_discount = pendapatan[~pendapatan["Pendapatan"].str.contains("Pajak|Diskon")]["Nominal"].sum()
    tax_and_discount = pendapatan[pendapatan["Pendapatan"].str.contains("Pajak|Diskon")]["Nominal"].sum()
    total_pendapatan = income_without_tax_discount - tax_and_discount
    st.info(f"Total Pendapatan: Rp{total_pendapatan:,}", icon="ℹ️")

    transaksi = df_transaksi.set_index("Tgl Terima")
    transaksi = transaksi.resample(resample)[["Subtotal"]].sum()
    transaksi = transaksi.rename(columns={"Subtotal": "Pendapatan Transaksi"})

    diskon = df_transaksi.set_index("Tgl Terima")
    diskon = diskon.resample(resample)[["Diskon"]].sum()
    diskon = diskon.rename(columns={"Diskon": "Diskon Transaksi Reguler"})

    snapclean = df_snapclean.set_index("Tanggal Diterima")
    snapclean = snapclean.resample(resample)[["Total Tagihan"]].sum()
    snapclean = snapclean.rename(columns={"Total Tagihan": "Pendapatan SnapClean"})

    df_pendapatan = transaksi.merge(diskon, left_index=True, right_index=True, how="left")
    df_pendapatan = df_pendapatan.merge(snapclean, left_index=True, right_index=True, how="left")

    df_pendapatan = df_pendapatan.reset_index().melt(
        id_vars="Tgl Terima",
        value_vars=df_pendapatan.columns,
        var_name="Pendapatan", 
        value_name="Nominal"
    )

    category_pendapatan = st.multiselect("label", label_visibility="collapsed", options=df_pendapatan["Pendapatan"].unique(), default=df_pendapatan["Pendapatan"].unique())

    fig = px.line(df_pendapatan[df_pendapatan["Pendapatan"].isin(category_pendapatan)], x="Tgl Terima", y="Nominal", color="Pendapatan")
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        legend_title_text="",
        margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=300
    )  
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_traces(hovertemplate="Tanggal: %{x}<br>Nominal: %{y}")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(f"<h5>Pengeluaran</h5>", unsafe_allow_html=True)

    with st.expander("Klik di sini untuk melihat lebih detail"):
        pengeluaran = df_biaya[df_biaya["Status"] == "Disetujui"]
        pengeluaran = pengeluaran.groupby("Untuk Akun Biaya")[["Nominal Biaya"]].sum().reset_index()
        pengeluaran = pengeluaran.sort_values("Nominal Biaya", ascending=False).reset_index(drop=True)
        pengeluaran.columns = ["Pengeluaran", "Nominal"]
        st.dataframe(pengeluaran, use_container_width=True)

    total_pengeluaran = pengeluaran["Nominal"].sum()
    st.info(f"Total Pengeluaran: Rp{total_pengeluaran:,}", icon="ℹ️")

    df_pengeluaran = df_biaya.copy()
    df_pengeluaran["Tanggal Dibuat"] = pd.to_datetime(df_pengeluaran["Tanggal Dibuat"])
    df_pengeluaran = df_pengeluaran.set_index("Tanggal Dibuat")
    df_pengeluaran = df_pengeluaran.groupby("Untuk Akun Biaya").resample(resample).sum().reset_index()

    category_pengeluaran = st.multiselect("label", label_visibility="collapsed", options=df_pengeluaran["Untuk Akun Biaya"].unique(), default=pengeluaran.head(3)["Pengeluaran"])

    fig = px.line(
        df_pengeluaran[df_pengeluaran["Untuk Akun Biaya"].isin(category_pengeluaran)],
        x="Tanggal Dibuat",
        y="Nominal Biaya",
        color="Untuk Akun Biaya"
    )
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        legend_title_text="",
        margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=300
    )  
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    fig.update_traces(hovertemplate="Tanggal: %{x}<br>Nominal: %{y}")
    st.plotly_chart(fig, use_container_width=True)

# Laba/Rugi
col1, col2 = st.columns(2)

col1.markdown(f"<h5>Laba/Rugi</h5>", unsafe_allow_html=True)

col1.info(f"Total Laba/Rugi: Rp{total_pendapatan - total_pengeluaran:,}", icon="ℹ️")

df_laba_rugi = df_pendapatan.merge(df_pengeluaran, left_on="Tgl Terima", right_on="Tanggal Dibuat", how="left")
df_laba_rugi = df_laba_rugi[["Tgl Terima", "Nominal", "Nominal Biaya"]]
df_laba_rugi = df_laba_rugi.set_index("Tgl Terima").resample(resample).sum()
df_laba_rugi.columns = ["Pendapatan", "Pengeluaran"]
df_laba_rugi["Laba_Rugi"] = df_laba_rugi["Pendapatan"] - df_laba_rugi["Pengeluaran"]

fig = px.line(df_laba_rugi, x=df_laba_rugi.index, y="Laba_Rugi")
fig.update_layout(
    xaxis_title=None,
    yaxis_title=None,
    margin=dict(t=0, b=0, l=0, r=0),
    height=300
)  
fig.update_xaxes(showgrid=False, zeroline=False)
fig.update_yaxes(showgrid=False, zeroline=False)
fig.update_traces(hovertemplate="Tanggal: %{x}<br>Laba/Rugi: %{y}")

col1.plotly_chart(fig, use_container_width=True)

# Perbandingan
col2.markdown(f"<h5>Perbandingan antara Omzet, Pengeluaran, dan Laba/Rugi</h5>", unsafe_allow_html=True)

df_omset = df_transaksi[["Tgl Terima", "Subtotal", "Tambahan Express", "Diskon", "Pajak"]]
df_omset["omset"] = df_omset["Subtotal"] + df_omset["Tambahan Express"] - df_omset["Diskon"] + df_omset["Pajak"]
df_omset = df_omset.set_index("Tgl Terima")
df_omset = df_omset.resample(resample).sum()[["omset"]]

df_perbandingan = pd.concat([df_omset, df_laba_rugi], axis=1)
df_perbandingan = df_perbandingan.drop("Pendapatan", axis=1)
df_perbandingan.columns = ["Omzet", "Pengeluaran", "Laba/Rugi"]

fig = go.Figure()

for column in df_perbandingan.columns:
    fig.add_trace(go.Scatter(x=df_perbandingan.index, y=df_perbandingan[column], mode="lines", name=column))

fig.update_layout(
    margin=dict(t=0, b=0, l=0, r=0),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    height=300
)
fig.update_xaxes(showgrid=False, zeroline=False, title_text=None)
fig.update_yaxes(showgrid=False, zeroline=False, title_text=None)

col2.plotly_chart(fig, use_container_width=True)

# Pengeluaran Bar Chart
col1 = st.columns(1)[0]

col1.markdown(f"<h5>Pengeluaran</h5>", unsafe_allow_html=True)

df_pengeluaran_bar = df_biaya[df_biaya["Status"] == "Disetujui"]
df_pengeluaran_bar = df_pengeluaran_bar.groupby(["Untuk Akun Biaya", "Diambil Dari Akun Kas"])["Nominal Biaya"].sum().reset_index()
df_pengeluaran_bar = df_pengeluaran_bar.sort_values(by="Nominal Biaya", ascending=False)

fig = px.histogram(
    df_pengeluaran_bar,
    x="Nominal Biaya",
    y="Untuk Akun Biaya",
    color="Diambil Dari Akun Kas",
    category_orders={"Untuk Akun Biaya": df_pengeluaran_bar.groupby("Untuk Akun Biaya")["Nominal Biaya"].sum().sort_values(ascending=False).index}
)
fig.update_layout(
    xaxis_title=None,
    legend=dict(
        title="",
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    margin=dict(t=0, b=0, l=0, r=0),
    height=400
)
col1.plotly_chart(fig, use_container_width=True)

# Top 10 Pelanggan
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<h5>Pelanggan Tidak Aktif</h5>", unsafe_allow_html=True)

    last_order_date = df_transaksi.groupby("Customer")["Tgl Terima"].max()
    current_date = df_transaksi["Tgl Terima"].max()

    intervals = [1, 3, 6, 9]
    customers_count = []

    previous_threshold = current_date

    for months in intervals:
        threshold_date = current_date - pd.DateOffset(months=months)
        count = sum((last_order_date <= previous_threshold) & (last_order_date > threshold_date))
        customers_count.append(count)
        previous_threshold = threshold_date

    inactive_customers = pd.DataFrame({
        "Bulan": [f"{i} Bulan" for i in intervals],
        "Jumlah Pelanggan": customers_count
    })

    fig = go.Figure(data=[go.Pie(labels=inactive_customers["Bulan"], values=inactive_customers["Jumlah Pelanggan"], hole=.3)])
    fig.update_layout(
        legend=dict(
            title="",
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=0, b=0, l=0, r=0),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(f"<h5>10 Pelanggan Teratas (Jumlah Transaksi)</h5>", unsafe_allow_html=True)

    df_transaksi['Total_Transaction'] = df_transaksi["Subtotal"] + df_transaksi["Tambahan Express"]
    customer_total_transaction = df_transaksi.groupby("Customer")['Total_Transaction'].sum().reset_index()

    df_sorted_transactions = df_transaksi.sort_values(by="Tgl Terima")
    days_difference = df_sorted_transactions.groupby('Customer')['Tgl Terima'].diff().dt.days
    avg_days_between_orders = days_difference.groupby(df_sorted_transactions['Customer']).mean().reset_index()
    avg_days_between_orders.rename(columns={"Tgl Terima": "Average_Days_Between_Orders"}, inplace=True)

    top_customers = df_transaksi.groupby("Customer").nunique()["No Nota"].sort_values(ascending=False).head(10).reset_index()

    top_customers = top_customers.merge(customer_total_transaction, on="Customer", how="left")
    top_customers = top_customers.merge(avg_days_between_orders, on="Customer", how="left")

    fig = px.bar(
        top_customers,
        x="No Nota",
        y="Customer",
        orientation="h",
        labels={"No Nota": "Jumlah Transaksi", "Customer": "Pelanggan"},
        hover_data=["Average_Days_Between_Orders"]
    )
    fig.update_layout(
        yaxis=dict(categoryorder="total ascending", title=None),
        margin=dict(t=0, b=0, l=0, r=0),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.markdown(f"<h5>10 Pelanggan Teratas (Total Transaksi)</h5>", unsafe_allow_html=True)

    top_total_value_customers = customer_total_transaction.sort_values(by="Total_Transaction", ascending=False).head(10)
    top_total_value_customers = top_total_value_customers.merge(avg_days_between_orders, on="Customer", how="left")

    fig = px.bar(
        top_total_value_customers,
        x="Total_Transaction",
        y="Customer",
        orientation="h",
        labels={"Total_Transaction": "Total Transaksi", "Customer": "Pelanggan"},
        hover_data=["Average_Days_Between_Orders"]
    )
    fig.update_layout(
        yaxis=dict(categoryorder="total ascending", title=None),
        margin=dict(t=0, b=0, l=0, r=0),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

# Top 10 Layanan
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<h5>10 Layanan Teratas (Jumlah Transaksi)</h5>", unsafe_allow_html=True)

    top_services_by_transactions = df_transaksi["Detail Layanan"].value_counts().head(10).reset_index()
    top_services_by_transactions.columns = ["Detail Layanan", "Jumlah Transaksi"]

    fig = px.bar(
        top_services_by_transactions,
        x="Jumlah Transaksi",
        y="Detail Layanan",
        orientation="h",
    )
    fig.update_layout(
        yaxis=dict(categoryorder="total ascending", title=None),
        margin=dict(t=0, b=0, l=0, r=0),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(f"<h5>10 Layanan Teratas (Total Transaksi)</h5>", unsafe_allow_html=True)

    top_services_by_value = df_transaksi.groupby("Detail Layanan")["Total_Transaction"].sum().nlargest(10).reset_index()
    top_services_by_value.columns = ["Detail Layanan", "Total Transaksi"]

    fig_top_services_value_plotly = px.bar(
        top_services_by_value,
        x="Total Transaksi",
        y="Detail Layanan",
        orientation="h",
    )
    fig.update_layout(
        yaxis=dict(categoryorder="total ascending", title=None),
        margin=dict(t=0, b=0, l=0, r=0),
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown(f'<style>{metric_css}</style>',unsafe_allow_html=True)