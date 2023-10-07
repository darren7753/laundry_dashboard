import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from streamlit_gsheets import GSheetsConnection

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
df_transaksi_original.columns = [j if "Unnamed" in i else i for i, j in zip(df_transaksi_original.columns, df_transaksi_original.iloc[0])]
df_transaksi_original = df_transaksi_original.iloc[1:].reset_index(drop=True)

for old_month, new_month in month_mapping.items():
    df_transaksi_original["Tgl Terima"] = df_transaksi_original["Tgl Terima"].str.replace(old_month, new_month, regex=True)
df_transaksi_original["Tgl Terima"] = pd.to_datetime(df_transaksi_original["Tgl Terima"], format="%d %b %Y %H:%M")

for old_month, new_month in month_mapping.items():
    df_transaksi_original["Tgl Selesai"] = df_transaksi_original["Tgl Selesai"].str.replace(old_month, new_month, regex=True)
df_transaksi_original["Tgl Selesai"] = pd.to_datetime(df_transaksi_original["Tgl Selesai"], format="%d %b %Y %H:%M")

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
col1, col2, col3 = st.columns(3)

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

with col3:
    outlets = df_transaksi_original["Outlet"].unique()
    default_outlet = ["Matahari Laundry Ciputat"]
    selected_outlets = st.multiselect("Pilih Outlet", outlets, default=default_outlet)

df_transaksi = df_transaksi_original[
    (df_transaksi_original["Tahun"] == selected_year) &
    (df_transaksi_original["Outlet"].isin(selected_outlets))
].copy()

df_pembayaran = df_pembayaran_original[
    (df_pembayaran_original["Tahun"] == selected_year) &
    (df_pembayaran_original["Outlet"].isin(selected_outlets))
].copy()

df_pengerjaan = df_pengerjaan_original[
    (df_pengerjaan_original["Tahun"] == selected_year) &
    (df_pengerjaan_original["Outlet"].isin(selected_outlets))
].copy()

df_biaya = df_biaya_original[
    (df_biaya_original["Tahun"] == selected_year) &
    (df_biaya_original["Outlet"].isin(selected_outlets))
].copy()

# Metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(label="Jumlah Transaksi", value=df_transaksi["No Nota"].nunique(), delta=None)

with col2:
    st.metric(label="Total Pelanggan", value=df_transaksi["Customer"].nunique(), delta=None)

with col3:
    total_transaksi = int(np.sum(df_transaksi["Subtotal"] + df_transaksi["Tambahan Express"]))
    st.metric(label="Total Transaksi", value=f"Rp{total_transaksi:,}", delta=None)

with col4:
    omzet_transaksi = int(np.sum(df_transaksi["Subtotal"] + df_transaksi["Tambahan Express"] - df_transaksi["Diskon"] + df_transaksi["Pajak"]))
    st.metric(label="Omzet Transaksi", value=f"Rp{omzet_transaksi:,}", delta=None)

with col5:
    total_pengeluaran = int(df_biaya[df_biaya["Status"] == "Disetujui"]["Nominal Biaya"].sum())
    st.metric(label="Total Pengeluaran", value=f"Rp{total_pengeluaran:,}", delta=None)

st.markdown(f'<style>{metric_css}</style>',unsafe_allow_html=True)

# Row
title_box_css = """
<style>
    .title-box {
        width: 100%;
        background-color: #f5f5f7; /* Adjust this color if needed */
        padding: 10px 0;
        color: #5a606b;
        text-align: center;
        font-size: 24px; /* Adjust font size if needed */
        margin-bottom: 20px;
        height: 40px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: 600;
    }
</style>
"""
st.markdown(title_box_css, unsafe_allow_html=True)

title = "ANALISIS TREN"
st.markdown(f"<div class='title-box'>{title}</div>", unsafe_allow_html=True)

col1 = st.columns(1)[0]

tabs = ["Jumlah Transaksi", "Total Pelanggan", "Total Transaksi", "Omzet Transaksi", "Total Pengeluaran"]
selected_tab = col1.selectbox("Choose a Metric", tabs, label_visibility="collapsed")

if selected_tab == "Jumlah Transaksi":
    title = "Jumlah Transaksi"
    chart_data = df_transaksi.groupby(pd.to_datetime(df_transaksi["Tgl Terima"])).nunique()["No Nota"].resample(resample).sum().reset_index()
    x_data = "Tgl Terima:T"
    y_data = "No Nota:Q"
elif selected_tab == "Total Pelanggan":
    title = "Total Pelanggan"
    chart_data = df_transaksi.groupby(pd.to_datetime(df_transaksi["Tgl Terima"])).nunique()["Customer"].resample(resample).sum().reset_index()
    x_data = "Tgl Terima:T"
    y_data = "Customer:Q"
elif selected_tab == "Total Transaksi":
    title = "Total Transaksi"
    chart_data = df_transaksi.groupby(pd.to_datetime(df_transaksi["Tgl Terima"])).sum()[["Subtotal", "Tambahan Express"]].resample(resample).sum().reset_index()
    chart_data["Total Transaksi"] = chart_data["Subtotal"] + chart_data["Tambahan Express"]
    x_data = "Tgl Terima:T"
    y_data = "Total Transaksi:Q"
elif selected_tab == "Omzet Transaksi":
    title = "Omzet Transaksi"
    chart_data = df_transaksi.groupby(pd.to_datetime(df_transaksi["Tgl Terima"])).sum()[["Subtotal", "Tambahan Express", "Diskon", "Pajak"]].resample(resample).sum().reset_index()
    chart_data["Omzet Transaksi"] = chart_data["Subtotal"] + chart_data["Tambahan Express"] - chart_data["Diskon"] + chart_data["Pajak"]
    x_data = "Tgl Terima:T"
    y_data = "Omzet Transaksi:Q"
elif selected_tab == "Total Pengeluaran":
    title = "Total Pengeluaran"
    chart_data = df_biaya.groupby(pd.to_datetime(df_biaya["Tanggal Pemakaian"])).sum()["Nominal Biaya"].resample(resample).sum().reset_index()
    x_data = "Tanggal Pemakaian:T"
    y_data = "Nominal Biaya:Q"

col1.markdown(f"<h5>Tren {title}</h5>", unsafe_allow_html=True)

chart = alt.Chart(chart_data).mark_line(color="#3d39cc").encode(
    x=alt.X(x_data, title=None),
    y=alt.Y(y_data, title=title)
).properties(
    height=300
).configure_axis(
    grid=False
)

col1.altair_chart(chart, use_container_width=True)

# Row
title_box_css = """
<style>
    .title-box {
        width: 100%;
        background-color: #f5f5f7; /* Adjust this color if needed */
        padding: 10px 0;
        color: #5a606b;
        text-align: center;
        font-size: 24px; /* Adjust font size if needed */
        margin-bottom: 20px;
        height: 40px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: 600;
    }
</style>
"""
st.markdown(title_box_css, unsafe_allow_html=True)

title = "PENGELUARAN"
st.markdown(f"<div class='title-box'>{title}</div>", unsafe_allow_html=True)

def create_stacked_chart(data):
    # Calculate the total 'Nominal Biaya' for each 'Untuk Akun Biaya'
    total_biaya_per_akun = data.groupby('Untuk Akun Biaya')['Nominal Biaya'].sum()

    # Calculate the 'Nominal Biaya' for each 'Diambil Dari Akun Kas' category within each 'Untuk Akun Biaya'
    biaya_per_akun_and_kas = data.groupby(['Untuk Akun Biaya', 'Diambil Dari Akun Kas'])['Nominal Biaya'].sum().reset_index()

    # Calculate the percentage and add it to the dataframe
    biaya_per_akun_and_kas['percentage'] = biaya_per_akun_and_kas.apply(lambda row: row['Nominal Biaya'] / total_biaya_per_akun[row['Untuk Akun Biaya']], axis=1)

    chart = alt.Chart(biaya_per_akun_and_kas).mark_bar().encode(
        y=alt.Y('Untuk Akun Biaya:O', title='Untuk Akun Biaya'),
        x=alt.X('percentage:Q', axis=alt.Axis(format='%', title=None)),
        color=alt.Color('Diambil Dari Akun Kas:O', scale=alt.Scale(domain=list(color_mapping.keys()), range=list(color_mapping.values())), legend=None),
        order=alt.Order(
            'Diambil Dari Akun Kas:O',
            sort='ascending'
        ),
        tooltip=[
            alt.Tooltip('Untuk Akun Biaya:O', title='Untuk Akun Biaya'),
            alt.Tooltip('Diambil Dari Akun Kas:O', title='Diambil Dari Akun Kas'),
            alt.Tooltip('percentage:Q', title='Persentase', format='.0%'),
            alt.Tooltip('Nominal Biaya:Q', title='Nominal Biaya')
        ]
    ).properties(
        height=350
    )

    return chart

# Unique values for 'Diambil Dari Akun Kas'
unique_akun_kas = df_biaya['Diambil Dari Akun Kas'].dropna().unique()

# Define a list of purple shades
colors = ["#33348e", "#3d39cc", "#7d7bcf", "#6c6c6e", "#b5b4ba"]

# Map colors to 'Diambil Dari Akun Kas' categories
color_mapping = dict(zip(unique_akun_kas, colors))

# Create charts for both statuses
chart_disetujui = create_stacked_chart(df_biaya[df_biaya["Status"] == "Disetujui"])
chart_ditolak = create_stacked_chart(df_biaya[df_biaya["Status"] == "Ditolak"])

# Display the charts side-by-side
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<h5>Status: Disetujui</h5>", unsafe_allow_html=True)
    st.altair_chart(chart_disetujui, use_container_width=True)

with col2:
    st.markdown(f"<h5>Status: Ditolak</h5>", unsafe_allow_html=True)
    st.altair_chart(chart_ditolak, use_container_width=True)

# CSS for styling the boxes
st.markdown(f"""
    <style>
        .akun-kas-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            margin-top: -20px;
            margin-bottom: 20px;
        }}
        .akun-kas-box {{
            flex: 1;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }}
        {"".join([f".akun-kas-box:nth-child({i + 1}) {{ background-color: {color}; width: {100/len(unique_akun_kas)}%; }}" for i, color in enumerate(colors[:len(unique_akun_kas)])])}
    </style>
""", unsafe_allow_html=True)

# Creating the container and boxes
boxes_html = "<div class='akun-kas-container'>"
for akun in unique_akun_kas:
    boxes_html += f"<div class='akun-kas-box'>{akun}</div>"
boxes_html += "</div>"

st.markdown(boxes_html, unsafe_allow_html=True)

# Row
title_box_css = """
<style>
    .title-box {
        width: 100%;
        background-color: #f5f5f7; /* Adjust this color if needed */
        padding: 10px 0;
        color: #5a606b;
        text-align: center;
        font-size: 24px; /* Adjust font size if needed */
        margin-bottom: 20px;
        height: 40px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: 600;
    }
</style>
"""
st.markdown(title_box_css, unsafe_allow_html=True)

title = "PELANGGAN"
st.markdown(f"<div class='title-box'>{title}</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<h5>Pelanggan Tidak Aktif</h5>", unsafe_allow_html=True)

    last_order_date = df_transaksi.groupby('Customer')['Tgl Terima'].max()
    current_date = df_transaksi['Tgl Terima'].max()

    intervals = [1, 3, 6, 9]
    colors = ["#3d39cc", "#8a7fd8", "#b3a5e6", "#d4ccf3", "#ebe7fa"]
    customers_count = []

    previous_threshold = current_date

    for months in intervals:
        threshold_date = current_date - pd.DateOffset(months=months)
        count = sum((last_order_date <= previous_threshold) & (last_order_date > threshold_date))
        customers_count.append(count)
        previous_threshold = threshold_date

    inactive_customers = pd.DataFrame({
        'Bulan': [f"{i} Bulan" for i in intervals],
        'Jumlah Pelanggan': customers_count
    })

    # Create a donut chart for inactive customers
    inactive_customers_donut_chart = alt.Chart(inactive_customers).mark_arc(innerRadius=50).encode(
        theta=alt.Theta("Jumlah Pelanggan:Q", stack=True, title=None),
        color=alt.Color("Bulan:N", legend=alt.Legend(orient="bottom"), scale=alt.Scale(domain=[f"{i} Bulan" for i in intervals], range=colors)),
        tooltip=["Bulan:N", "Jumlah Pelanggan:Q"]
    ).properties(
        width=300,
        height=300
    )

    st.altair_chart(inactive_customers_donut_chart, use_container_width=True)

with col2:
    st.markdown(f"<h5>10 Pelanggan Teratas (Jumlah Transaksi)</h5>", unsafe_allow_html=True)

    # Calculate "Total Transaksi" for each customer
    df_transaksi['Total_Transaction'] = df_transaksi["Subtotal"] + df_transaksi["Tambahan Express"]
    customer_total_transaction = df_transaksi.groupby("Customer")['Total_Transaction'].sum().reset_index()

    # Calculate average days between repetitive orders for each customer
    df_sorted_transactions = df_transaksi.sort_values(by="Tgl Terima")
    days_difference = df_sorted_transactions.groupby('Customer')['Tgl Terima'].diff().dt.days
    avg_days_between_orders = days_difference.groupby(df_sorted_transactions['Customer']).mean().reset_index()
    avg_days_between_orders.rename(columns={"Tgl Terima": "Average_Days_Between_Orders"}, inplace=True)

    # Identify top 10 customers by number of transactions
    top_customers = df_transaksi.groupby("Customer").nunique()["No Nota"].sort_values(ascending=False).head(10).reset_index()

    # Merge this information with the `top_customers` DataFrame
    top_customers = top_customers.merge(customer_total_transaction, on="Customer", how="left")
    top_customers = top_customers.merge(avg_days_between_orders, on="Customer", how="left")

    # Update the Altair chart definition
    top_customers_chart = alt.Chart(top_customers).mark_bar(color="#3d39cc").encode(
        y=alt.Y("Customer:N", title=None, sort="-x"),
        x=alt.X("No Nota:Q", title="Jumlah Transaksi"),
        tooltip=[
            alt.Tooltip("Customer:N", title="Pelanggan"),
            alt.Tooltip("No Nota:Q", title="Jumlah Transaksi"),
            alt.Tooltip("Average_Days_Between_Orders:Q", title="Rata-rata Hari Antar Transaksi", format=".1f")
        ]
    ).properties(
        height=300
    ).configure_axis(
        grid=False
    )

    st.altair_chart(top_customers_chart, use_container_width=True)

with col3:
    st.markdown(f"<h5>10 Pelanggan Teratas (Total Transaksi)</h5>", unsafe_allow_html=True)

    # Rank customers based on total transactions and take the top 10
    top_total_value_customers = customer_total_transaction.sort_values(by="Total_Transaction", ascending=False).head(10)

    # Merge this information with the `avg_days_between_orders` DataFrame
    top_total_value_customers = top_total_value_customers.merge(avg_days_between_orders, on="Customer", how="left")

    # Create the Altair chart
    top_value_customers_chart = alt.Chart(top_total_value_customers).mark_bar(color="#3d39cc").encode(
        y=alt.Y("Customer:N", title=None, sort="-x"),
        x=alt.X("Total_Transaction:Q", title="Total Transaksi"),
        tooltip=[
            alt.Tooltip("Customer:N", title="Pelanggan"),
            alt.Tooltip("Total_Transaction:Q", title="Total Transaksi", format=".0f"),
            alt.Tooltip("Average_Days_Between_Orders:Q", title="Rata-rata Hari Antar Transaksi", format=".1f")
        ]
    ).properties(
        height=300
    ).configure_axis(
        grid=False
    )

    st.altair_chart(top_value_customers_chart, use_container_width=True)

# Row
title_box_css = """
<style>
    .title-box {
        width: 100%;
        background-color: #f5f5f7; /* Adjust this color if needed */
        padding: 10px 0;
        color: #5a606b;
        text-align: center;
        font-size: 24px; /* Adjust font size if needed */
        margin-bottom: 20px;
        height: 40px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: 600;
    }
</style>
"""
st.markdown(title_box_css, unsafe_allow_html=True)

title = "LAYANAN"
st.markdown(f"<div class='title-box'>{title}</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
# Top 10 services based on number of transactions
with col1:
    st.markdown(f"<h5>10 Layanan Teratas (Jumlah Transaksi)</h5>", unsafe_allow_html=True)

    top_services_by_transactions = df_transaksi["Detail Layanan"].value_counts().head(10).reset_index()
    top_services_by_transactions.columns = ["Detail Layanan", "Jumlah Transaksi"]

    # Create the Altair chart
    top_services_transactions_chart = alt.Chart(top_services_by_transactions).mark_bar(color="#3d39cc").encode(
        y=alt.Y("Detail Layanan:N", title=None, sort="-x"),
        x=alt.X("Jumlah Transaksi:Q", title="Jumlah Transaksi"),
        tooltip=[
            alt.Tooltip("Detail Layanan:N", title="Layanan"),
            alt.Tooltip("Jumlah Transaksi:Q", title="Jumlah Transaksi")
        ]
    ).properties(
        height=300
    ).configure_axis(
        grid=False
    )

    st.altair_chart(top_services_transactions_chart, use_container_width=True)

# Top 10 services based on total transaction value (subtotal + tambahan express)
with col2:
    st.markdown(f"<h5>10 Layanan Teratas (Total Transaksi)</h5>", unsafe_allow_html=True)

    top_services_by_value = df_transaksi.groupby("Detail Layanan")["Total_Transaction"].sum().nlargest(10).reset_index()
    top_services_by_value.columns = ["Detail Layanan", "Total Transaksi"]

    # Create the Altair chart
    top_services_value_chart = alt.Chart(top_services_by_value).mark_bar(color="#3d39cc").encode(
        y=alt.Y("Detail Layanan:N", title=None, sort="-x"),
        x=alt.X("Total Transaksi:Q", title="Total Transaksi"),
        tooltip=[
            alt.Tooltip("Detail Layanan:N", title="Layanan"),
            alt.Tooltip("Total Transaksi:Q", title="Total Transaksi", format=".0f")
        ]
    ).properties(
        height=300
    ).configure_axis(
        grid=False
    )

    st.altair_chart(top_services_value_chart, use_container_width=True)