import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def load_data():
    sns.set(style='dark')

    day_df = pd.read_csv("https://raw.githubusercontent.com/RizalNR03/Proyek-Analisis-Data-Bike-Sharing/main/data/day.csv")
    hour_df = pd.read_csv("https://raw.githubusercontent.com/RizalNR03/Proyek-Analisis-Data-Bike-Sharing/main/data/hour.csv")

    bike_sharing_df = day_df.merge(hour_df, on='dteday', how='inner', suffixes=('_d', '_h'))
    season_labels = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
    }
    bike_sharing_df['season_labels'] = bike_sharing_df['season_d'].map(season_labels)
    bike_sharing_df.groupby('season_labels')['cnt_d'].mean().reset_index().sort_values('cnt_d')
    
    weather_labels = {
    1: 'Clear, Few clouds, Partly cloudy, Partly cloudy',
    2: 'Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist',
    3: 'Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds',
    4: 'Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'
    }
    bike_sharing_df['weather_label'] = bike_sharing_df['weathersit_d'].map(weather_labels)
    bike_sharing_df.groupby('weather_label')['cnt_d'].mean().reset_index().sort_values('cnt_d')

    datetime_columns = ["dteday"]
    for column in datetime_columns:
        bike_sharing_df[column] = pd.to_datetime(bike_sharing_df[column])

    min_date = bike_sharing_df["dteday"].min()
    max_date = bike_sharing_df["dteday"].max()

    return bike_sharing_df, min_date, max_date

def setup_sidebar(min_date, max_date):
    with st.sidebar:
        st.subheader('Rental Sepeda')
        st.image("https://cdn.pixabay.com/photo/2012/04/28/19/26/bicycles-44154_960_720.png")
        
        selected_dates = st.date_input(
            label='Rentang Waktu', min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )

    # Periksa apakah sudah ada dua tanggal yang dimasukkan
        if len(selected_dates) != 2:
            raise ValueError("Masukkan rentang waktu yang lengkap. Mohon pilih kedua tanggal.")
        
        start_date, end_date = selected_dates
    return start_date, end_date

def filter_data(bike_sharing_df, start_date, end_date):
    main_df = bike_sharing_df[(bike_sharing_df["dteday"] >= str(start_date)) & 
                      (bike_sharing_df["dteday"] <= str(end_date))]
    return main_df

def show_header():
    st.header('Dashboard Analisis Data Bike Sharing')
    st.subheader('Daily User Total')

def show_user_metrics(main_df):
    total_user = main_df.cnt_h.sum()
    st.metric("Total user", value=total_user)

def show_graphic_1(main_df):
    st.subheader("Rata-Rata sewa per hari")
    total_user_per_day = main_df.groupby('dteday')['cnt_h'].sum()

    plt.figure(figsize=(12, 6))
    plt.plot(total_user_per_day.index, total_user_per_day.values, color='blue')
    plt.title('Total Pengguna Sepeda per Hari')
    plt.xlabel('Tanggal')
    plt.ylabel('Total Pengguna')
    plt.xticks(rotation=45)


    st.pyplot(plt)

def show_graphic_2(main_df):
    st.subheader("Rata-Rata sewa per jam")
    hourly_avg_rentals = main_df.groupby('hr')['cnt_h'].mean()
    plt.figure(figsize=(10,6))
    plt.bar(hourly_avg_rentals.index, hourly_avg_rentals.values, color='blue')
    plt.xlabel('Jam')
    plt.ylabel('Rata - Rata Penyewaan')
    st.pyplot(plt)

def show_graphic_3(bike_sharing_df):
    st.subheader("Rata - Rata Penyewaan Sepeda berdasarkan bulan")
    month_map = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
    }

    bike_sharing_df['mnth_d'] = bike_sharing_df['mnth_d'].map(month_map)

    monthly_avg = bike_sharing_df.groupby('mnth_d')['cnt_d'].mean().reset_index()
    monthly_avg_sorted = monthly_avg.sort_values(by='cnt_d')

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='mnth_d', y='cnt_d', data=monthly_avg_sorted, marker='o', color='blue')
    plt.title('Tren Rata-rata Jumlah Penyewaan Sepeda per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Rata-rata Jumlah Penyewaan')
    plt.xticks(rotation=45)
    plt.grid(True)
    
    st.pyplot(plt)

def show_graphic_4(bike_sharing_df):
    st.subheader("Jumlah Penyewaan Sepeda berdasarkan Musim")
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='cnt_d', y='season_labels', data=bike_sharing_df, hue='season_labels', palette='viridis', dodge=False)
    plt.title('Jumlah Penyewaan Sepeda berdasarkan Musim')
    plt.xlabel('Jumlah Penyewaan')
    plt.ylabel('Musim')
    plt.xticks(rotation=45)
    plt.legend([])

    st.pyplot(plt)

def show_graphic_5(bike_sharing_df):
    st.subheader("Proporsi Jumlah Penyewaan Sepeda berdasarkan Cuaca")
    
    plt.figure(figsize=(8, 8))
    weather_counts = bike_sharing_df['weather_label'].value_counts()
    plt.pie(weather_counts, labels=weather_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('viridis', len(weather_counts)))
    plt.title('Proporsi Jumlah Penyewaan Sepeda berdasarkan Cuaca')
    
    st.pyplot(plt)

def main():
    bike_sharing_df, min_date, max_date = load_data()
    start_date, end_date = setup_sidebar(min_date, max_date)
    main_df = filter_data(bike_sharing_df, start_date, end_date)

    show_header()
    show_user_metrics(main_df)
    col1, col2 = st.columns(2)
    with col1:
        show_graphic_1(main_df)

    with col2:
        show_graphic_2(main_df)

    show_graphic_3(bike_sharing_df)
    show_graphic_4(bike_sharing_df)
    show_graphic_5(bike_sharing_df)


if __name__ == '__main__':
    main()
