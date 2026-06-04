import streamlit as st
import pandas as pd
import joblib

# Konfigurasi Halaman
st.set_page_config(page_title="Demo Machine Learning", page_icon="🤖", layout="wide")

st.sidebar.title("Navigasi Studi Kasus")
pilihan_menu = st.sidebar.radio(
    "Pilih Model Machine Learning:",
    ("📈 Regresi (Prediksi Minyak Pemanas)", "📱 Klasifikasi (Adopsi Tablet)", "👥 Klasterisasi (Segmentasi Pelanggan)")
)

st.sidebar.markdown("---")
st.sidebar.info("Aplikasi ini adalah contoh hasil akhir dari model prediksi yang telah dilatih.")

# ==========================================
# 1. MENU REGRESI
# ==========================================
if pilihan_menu == "📈 Regresi (Prediksi Minyak Pemanas)":
    st.title("📈 Prediksi Konsumsi Minyak Pemanas (Regresi)")
    st.markdown("Masukkan data parameter rumah untuk memprediksi berapa banyak minyak pemanas yang dibutuhkan.")
    
    col1, col2 = st.columns(2)
    with col1:
        insulation = st.slider("Tingkat Insulasi (Insulation)", min_value=2, max_value=10, value=6)
        temperature = st.number_input("Suhu (Temperature)", min_value=38, max_value=90, value=65)
        num_occupants = st.slider("Jumlah Penghuni (Num_Occupants)", min_value=1, max_value=10, value=3)
    with col2:
        avg_age = st.number_input("Rata-rata Usia (Avg_Age)", min_value=15.1, max_value=72.2, value=42.7)
        home_size = st.slider("Ukuran Rumah (Home_Size)", min_value=1, max_value=8, value=4)

    if st.button("Hitung Prediksi Konsumsi", type="primary"):
        try:
            model = joblib.load('models/regresi_model.pkl')
            input_data = pd.DataFrame([[insulation, temperature, num_occupants, avg_age, home_size]],
                                      columns=['Insulation', 'Temperature', 'Num_Occupants', 'Avg_Age', 'Home_Size'])
            prediksi = model.predict(input_data)[0]
            st.success(f"Estimasi Konsumsi Minyak Pemanas: **{prediksi:.2f} unit**")
        except FileNotFoundError:
            dummy_pred = (insulation * 5) + (temperature * -1) + (home_size * 10) + 150
            st.warning("⚠️ File 'regresi_model.pkl' tidak ditemukan. Menampilkan hasil simulasi:")
            st.success(f"Estimasi Konsumsi Minyak Pemanas: **{abs(dummy_pred):.2f} unit**")


# ==========================================
# 2. MENU KLASIFIKASI (Telah Diupdate dengan Encoder)
# ==========================================
elif pilihan_menu == "📱 Klasifikasi (Adopsi Tablet)":
    st.title("📱 Prediksi Potensi Adopsi Tablet (Klasifikasi)")
    st.markdown("Masukkan profil pelanggan untuk memprediksi apakah mereka akan mengadopsi tablet.")
    
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Jenis Kelamin (Gender)", ["M", "F"])
        age = st.number_input("Usia (Age)", min_value=16, max_value=66, value=42)
        marital_status = st.selectbox("Status Pernikahan (Marital_Status)", ["S", "M"])
        website_activity = st.selectbox("Aktivitas Website", ["Seldom", "Regular", "Frequent"])
        payment_method = st.selectbox("Metode Pembayaran", ["Credit Card", "Bank Transfer", "Website Account", "Monthly Billing"])
    with col2:
        browsed_electronics = st.selectbox("Mencari Elektronik 12 Bulan Terakhir?", ["Yes", "No"])
        bought_electronics = st.selectbox("Beli Elektronik 12 Bulan Terakhir?", ["Yes", "No"])
        bought_media = st.selectbox("Beli Media Digital 18 Bulan Terakhir?", ["Yes", "No"])
        bought_books = st.selectbox("Beli Buku Digital?", ["Yes", "No"])
        
    if st.button("Klasifikasikan Pelanggan", type="primary"):
        try:
            # Load model dan load encoder (kamus penerjemah teks ke angka)
            model = joblib.load('models/klasifikasi_model.pkl')
            encoders = joblib.load('models/encoders_klasifikasi.pkl')
            
            # Transformasi input teks menggunakan encoder yang sesuai
            gender_enc = encoders['Gender'].transform([gender])[0]
            marital_enc = encoders['Marital_Status'].transform([marital_status])[0]
            web_act_enc = encoders['Website_Activity'].transform([website_activity])[0]
            browsed_enc = encoders['Browsed_Electronics_12Mo'].transform([browsed_electronics])[0]
            bought_elec_enc = encoders['Bought_Electronics_12Mo'].transform([bought_electronics])[0]
            bought_media_enc = encoders['Bought_Digital_Media_18Mo'].transform([bought_media])[0]
            bought_books_enc = encoders['Bought_Digital_Books'].transform([bought_books])[0]
            payment_enc = encoders['Payment_Method'].transform([payment_method])[0]
            
            # Masukkan ke DataFrame sesuai urutan fitur saat training
            input_data = pd.DataFrame([[
                gender_enc, age, marital_enc, web_act_enc, browsed_enc, 
                bought_elec_enc, bought_media_enc, bought_books_enc, payment_enc
            ]])
            
            prediksi = model.predict(input_data)[0]
            
            if prediksi == 1:
                st.success("Pelanggan diprediksi: **YES (Akan mengadopsi tablet)**")
            else:
                st.error("Pelanggan diprediksi: **NO (Tidak mengadopsi tablet)**")
                
        except FileNotFoundError:
            st.warning("⚠️ File 'models/klasifikasi_model.pkl' atau 'models/encoders_klasifikasi.pkl' tidak ditemukan. Menampilkan simulasi:")
            hasil = "YES (Akan Mengadopsi)" if website_activity == "Frequent" or bought_electronics == "Yes" else "NO (Tidak Mengadopsi)"
            st.success(f"Prediksi Adopsi Tablet: **{hasil}**")


# ==========================================
# 3. MENU KLASTERISASI
# ==========================================
else:
    st.title("👥 Segmentasi Pelanggan (Klasterisasi)")
    st.markdown("Masukkan data transaksi dan demografi pelanggan untuk melihat segmen klaster.")
    
    col1, col2 = st.columns(2)
    with col1:
        income = st.number_input("Pendapatan Tahunan (Income)", min_value=1730.0, max_value=666666.0, value=52247.0)
        kidhome = st.slider("Jumlah Anak (Kidhome)", 0, 2, 0)
        total_spending = st.number_input("Total Pengeluaran (TotalSpending)", value=600)
        num_purchases = st.number_input("Total Transaksi (NumPurchases)", value=15)
        
    with col2:
        num_deals = st.number_input("Pembelian dengan Diskon (NumDealsPurchases)", value=2)
        num_web = st.number_input("Pembelian via Web (NumWebPurchases)", value=5)
        num_catalog = st.number_input("Pembelian via Katalog (NumCatalogPurchases)", value=3)
        num_store = st.number_input("Pembelian di Toko (NumStorePurchases)", value=6)
        num_visits = st.number_input("Kunjungan Web per Bulan (NumWebVisitsMonth)", value=5)

    if st.button("Tentukan Klaster", type="primary"):
        try:
            model = joblib.load('models/klasterisasi_model.pkl')
            input_data = pd.DataFrame([[
                income, kidhome, total_spending, num_purchases, 
                num_deals, num_web, num_catalog, num_store, num_visits
            ]])
            prediksi = model.predict(input_data)[0]
            st.success(f"Pelanggan ini masuk ke dalam: **Klaster {prediksi}**")
        except FileNotFoundError:
            st.warning("⚠️ File 'models/klasterisasi_model.pkl' tidak ditemukan. Menampilkan hasil simulasi:")
            klaster = 2 if income > 75000 else (1 if total_spending > 500 else 0)
            st.success(f"Pelanggan ini dikelompokkan ke: **Klaster {klaster}**")