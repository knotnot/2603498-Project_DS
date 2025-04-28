from flask import Flask, render_template, request  # เพิ่มการ import request
import numpy as np
import joblib

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # ใช้ไฟล์ HTML ที่ชื่อว่า index.html

@app.route('/start', methods=['GET', 'POST'])
def input_form():
    model = joblib.load('final_model.pkl')

    # ข้อมูลสภาพอากาศตามภาคที่ใช้เฉพาะภายในฟังก์ชันนี้
    weather_data_by_region = {
        'north': {
            'T2M_MAX-W': 30.5, 'T2M_MAX-Sp': 32.2, 'T2M_MAX-Su': 34.0, 'T2M_MAX-Au': 31.0,
            'T2M_MIN-W': 15.2, 'T2M_MIN-Sp': 18.0, 'T2M_MIN-Su': 22.1, 'T2M_MIN-Au': 19.5,
            'PRECTOTCORR-W': 12.1, 'PRECTOTCORR-Sp': 30.5, 'PRECTOTCORR-Su': 45.0, 'PRECTOTCORR-Au': 25.2,
            'WD10M': 5.5, 'GWETTOP': 0.3, 'CLOUD_AMT': 0.5, 'WS2M_RANGE': 1.5, 'PS': 77.5
        },
        'northeast': {
            'T2M_MAX-W': 30.0, 'T2M_MAX-Sp': 31.5, 'T2M_MAX-Su': 34.5, 'T2M_MAX-Au': 31.5,
            'T2M_MIN-W': 16.0, 'T2M_MIN-Sp': 18.5, 'T2M_MIN-Su': 22.0, 'T2M_MIN-Au': 19.5,
            'PRECTOTCORR-W': 30.0, 'PRECTOTCORR-Sp': 45.0, 'PRECTOTCORR-Su': 70.0, 'PRECTOTCORR-Au': 35.0,
            'WD10M': 5.8, 'GWETTOP': 0.3, 'CLOUD_AMT': 0.4, 'WS2M_RANGE': 1.6, 'PS': 77.0
        },
        'central': {
        'T2M_MAX-W': 0, 'T2M_MAX-Sp': 32.5, 'T2M_MAX-Su': 34.0, 'T2M_MAX-Au': 32.0,
        'T2M_MIN-W': 0, 'T2M_MIN-Sp': 21.5, 'T2M_MIN-Su': 23.5, 'T2M_MIN-Au': 21.0,
        'PRECTOTCORR-W': 0, 'PRECTOTCORR-Sp': 15.0, 'PRECTOTCORR-Su': 30.0, 'PRECTOTCORR-Au': 12.0,
        'WD10M': 6.0, 'GWETTOP': 0.4, 'CLOUD_AMT': 0.6, 'WS2M_RANGE': 1.2, 'PS': 77.0
         },
        'south': {
            'T2M_MAX-W': 0.0, 'T2M_MAX-Sp': 3.5, 'T2M_MAX-Su': 2.0, 'T2M_MAX-Au': 0.5,
            'T2M_MIN-W': 2.0, 'T2M_MIN-Sp': 2.5, 'T2M_MIN-Su': 5.5, 'T2M_MIN-Au': 2.0,
            'PRECTOTCORR-W': 50.0, 'PRECTOTCORR-Sp': 7.0, 'PRECTOTCORR-Su': 12.0, 'PRECTOTCORR-Au': 6.0,
            'WD10M': 5.2, 'GWETTOP': 0.5, 'CLOUD_AMT': 0.7, 'WS2M_RANGE': 1.4, 'PS': 7.5
        },
        'east': {
            'T2M_MAX-W': 30.0, 'T2M_MAX-Sp': 31.5, 'T2M_MAX-Su': 33.5, 'T2M_MAX-Au': 31.5,
            'T2M_MIN-W': 19.0, 'T2M_MIN-Sp': 20.5, 'T2M_MIN-Su': 23.0, 'T2M_MIN-Au': 21.5,
            'PRECTOTCORR-W': 20.0, 'PRECTOTCORR-Sp': 35.0, 'PRECTOTCORR-Su': 45.0, 'PRECTOTCORR-Au': 30.0,
            'WD10M': 5.0, 'GWETTOP': 0.4, 'CLOUD_AMT': 0.6, 'WS2M_RANGE': 1.3, 'PS': 77.0
        },
        'west': {
            'T2M_MAX-W': 30.5, 'T2M_MAX-Sp': 32.0, 'T2M_MAX-Su': 33.0, 'T2M_MAX-Au': 31.5,
            'T2M_MIN-W': 18.0, 'T2M_MIN-Sp': 20.0, 'T2M_MIN-Su': 23.0, 'T2M_MIN-Au': 21.0,
            'PRECTOTCORR-W': 15.0, 'PRECTOTCORR-Sp': 25.0, 'PRECTOTCORR-Su': 50.0, 'PRECTOTCORR-Au': 20.0,
            'WD10M': 6.1, 'GWETTOP': 0.4, 'CLOUD_AMT': 0.5, 'WS2M_RANGE': 1.1, 'PS': 77.5
        }
    }
    crop_labels = {
        0: 'Barley',
        1: 'Bean',
        2: 'Dagussa',
        3: 'Fallow',
        4: 'Maize',
        5: 'Niger seed',
        6: 'Pea',
        7: 'Potato',
        8: 'Red Pepper',
        9: 'Sorghum',
        10: 'Teff',
        11: 'Wheat'
    }

    if request.method == 'POST':
        # รับข้อมูลจากฟอร์ม
        soil_minerals = [
            1.0,
            float(request.form['mineral1']),
            float(request.form['mineral2']),
            float(request.form['mineral3']),
            float(request.form['mineral4']),
            float(request.form['mineral5']),
            float(request.form['mineral6']),
        ]
        
        province = request.form['province']  # เลือกภาคจากฟอร์ม
        target_crop = int(request.form['target'])

        # นำข้อมูลจากฟอร์ม + ข้อมูลสภาพอากาศตามภาค
        region_data = weather_data_by_region.get(province, {})

        qv2m_data = {
            'QV2M-W': 7.5,
            'QV2M-Sp': 10.45,
            'QV2M-Su': 11.2,
            'QV2M-Au': 15.0,
        }

        # รวมข้อมูลแร่ธาตุกับสภาพอากาศ
        all_features = soil_minerals + list(qv2m_data.values()) + list(region_data.values())

        # เปลี่ยนข้อมูลที่ได้รับเป็น numpy array (หรือให้เหมาะสมกับโมเดลของคุณ)
        input_data = np.array(all_features).reshape(1, -1)
        prediction = model.predict(input_data)

        if prediction[0] == target_crop:
            return render_template('ready.html', target_crop=crop_labels[target_crop])

        # ประมวลผลผลลัพธ์จาก prediction
        predicted_crop = crop_labels.get(prediction[0], "ไม่ทราบพืชที่แนะนำ")
        result = f"แนะนำให้ปลูก: {predicted_crop}"
        target_crop = crop_labels.get(target_crop, "ไม่ทราบพืชที่ต้องการปลูก")

        return render_template('result.html', result=result, prediction=prediction , 
                               target_crop=target_crop)
    return render_template('input.html')


@app.route('/how_to')
def how_to():
    return render_template('how_to.html')

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # เปิดเซิร์ฟเวอร์ที่พอร์ต 5000
