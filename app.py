from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# ==========================================
# 1. API Endpoint REGRESI
# ==========================================
@app.route('/predict_regresi', methods=['POST'])
def predict_regresi():
    data = request.json 
    try:
        model = joblib.load('models/regresi_model.pkl')
        input_data = pd.DataFrame([[
            float(data['insulation']), float(data['temperature']), 
            float(data['num_occupants']), float(data['avg_age']), float(data['home_size'])
        ]])
        prediksi = model.predict(input_data)[0]
        hasil_teks = f"{prediksi:.2f} unit"
    except FileNotFoundError:
        dummy_pred = (float(data['insulation']) * 5) + (float(data['temperature']) * -1) + (float(data['home_size']) * 10) + 150
        hasil_teks = f"{abs(dummy_pred):.2f} unit (Hasil Simulasi)"
    return jsonify({'hasil': hasil_teks})


# ==========================================
# 2. API Endpoint KLASIFIKASI (Telah Diupdate dengan Encoder)
# ==========================================
@app.route('/predict_klasifikasi', methods=['POST'])
def predict_klasifikasi():
    data = request.json
    try:
        # Load Model dan Load Encoder
        model = joblib.load('models/klasifikasi_model.pkl')
        encoders = joblib.load('models/encoders_klasifikasi.pkl')
        # Transformasi input teks menggunakan encoder
        input_terenkode = {
            'Gender': encoders['Gender'].transform([data['gender']])[0],
            'Age': int(data['age']), 
            'Marital_Status': encoders['Marital_Status'].transform([data['marital_status']])[0],
            'Website_Activity': encoders['Website_Activity'].transform([data['website_activity']])[0],
            'Browsed_Electronics_12Mo': encoders['Browsed_Electronics_12Mo'].transform([data['browsed_electronics']])[0],
            'Bought_Electronics_12Mo': encoders['Bought_Electronics_12Mo'].transform([data['bought_electronics']])[0],
            'Bought_Digital_Media_18Mo': encoders['Bought_Digital_Media_18Mo'].transform([data['bought_media']])[0],
            'Bought_Digital_Books': encoders['Bought_Digital_Books'].transform([data['bought_books']])[0],
            'Payment_Method': encoders['Payment_Method'].transform([data['payment_method']])[0]
        }
        
        # Masukkan ke DataFrame sesuai urutan fitur
        input_data = pd.DataFrame([[
            input_terenkode['Gender'], input_terenkode['Age'], input_terenkode['Marital_Status'], 
            input_terenkode['Website_Activity'], input_terenkode['Browsed_Electronics_12Mo'], 
            input_terenkode['Bought_Electronics_12Mo'], input_terenkode['Bought_Digital_Media_18Mo'],
            input_terenkode['Bought_Digital_Books'], input_terenkode['Payment_Method']
        ]])
        
        prediksi = model.predict(input_data)[0]
        hasil_teks = "YES (Akan Mengadopsi Tablet)" if prediksi == 1 else "NO (Tidak Mengadopsi)"
        
    except FileNotFoundError:
        # Simulasi jika model atau encoder belum dibuat mahasiswa
        if data['website_activity'] == 'Frequent' or data['bought_electronics'] == 'Yes':
            hasil_teks = "YES (Akan Mengadopsi) - Simulasi"
        else:
            hasil_teks = "NO (Tidak Mengadopsi) - Simulasi"
            
    return jsonify({'hasil': hasil_teks})


# ==========================================
# 3. API Endpoint KLASTERISASI
# ==========================================
@app.route('/predict_klasterisasi', methods=['POST'])
def predict_klasterisasi():
    data = request.json
    try:
        model = joblib.load('models/klasterisasi_model.pkl')
        input_data = pd.DataFrame([[
            float(data['income']), int(data['kidhome']), float(data['total_spending']),
            int(data['num_purchases']), int(data['num_deals']), int(data['num_web']),
            int(data['num_catalog']), int(data['num_store']), int(data['num_visits'])
        ]])
        prediksi = model.predict(input_data)[0]
        hasil_teks = f"Klaster {prediksi}"
    except FileNotFoundError:
        income = float(data['income'])
        spending = float(data['total_spending'])
        if income > 75000:
            hasil_teks = "Klaster 2 (Pendapatan Tinggi) - Simulasi"
        elif spending > 500:
            hasil_teks = "Klaster 1 (Menengah Aktif) - Simulasi"
        else:
            hasil_teks = "Klaster 0 (Standar) - Simulasi"
    return jsonify({'hasil': hasil_teks})

if __name__ == '__main__':
    app.run(debug=True)