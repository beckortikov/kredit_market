import streamlit as st
import pandas as pd
import joblib
import gspread
# Загрузка модели
model = joblib.load('tj_consolidate_pycaret_02.pkl')
import pdfkit
# Функция для генерации PDF
from datetime import datetime
def generate_pdf(data, document_number, date):
    rendered = f'''
    <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <title>Client Request</title>
</head>

<body>
    <div class="container">
        <img src="km_logo.png" alt="Company Logo" width="100" height="100" style="position: absolute; top: 10px; left: 10px;">
        <br><br>
        <h4 class="text-center"><strong>Документ</strong></h4>
        <br><br>
        <table class="table table-bordered">
            <tbody>
                <tr>
                    <td style="width: 50%;">Менеджер</td>
                    <td style="width: 50%;">{data['Manager'][0]}</td>
                </tr>
                <tr>
                    <td style="width: 50%;">Филиал</td>
                    <td style="width: 50%;">{data['district'][0]}</td>
                </tr>
                <tr>
                    <td style="width: 50%;">Имя</td>
                    <td style="width: 50%;">{data['name'][0]}</td>
                </tr>
                <tr>
                    <td style="width: 50%;">Фамилия</td>
                    <td style="width: 50%;">{data['surname'][0]}</td>
                </tr>
                <tr>
                    <td style="width: 50%;">Телефон номер</td>
                    <td style="width: 50%;">{data['phone'][0]}</td>
                </tr>
                <tr>
                    <td style="width: 50%;">Возраст</td>
                    <td style="width: 50%;">{data['age'][0]}</td>
                </tr>
                <tr>
                    <td style="width: 50%;">Пол</td>
                    <td style="width: 50%;">{data['gender'][0]}</td>
                </tr>
                <tr>
                    <td style="width: 50%;">Сумма</td>
                    <td style="width: 50%;">{data['amount'][0]}</td>
                </tr>
                <tr>
                    <td style="width: 50%;">Период</td>
                    <td style="width: 50%;">{data['duration'][0]}</td>
                </tr>
                <tr>
                    <td style="width: 50%;">Семейный статус</td>
                    <td style="width: 50%;">{data['marital_status'][0]}</td>
                </tr>
                <tr>
                    <td style="width: 50%;">Результат скоринга</td>
                    <td style="width: 50%;">{data['Result'][0]}</td>
                </tr>
                <tr>
                    <td style="width: 50%;">Вероятность возврата</td>
                    <td style="width: 50%;">{data['Probability'][0]}</td>
                </tr>
            </tbody>
        </table>

   <br><br><br><br>
        <tr>
            <td colspan="2" style="text-align: left;">Дата {datetime.strptime(date,'%Y-%m-%d %H:%M:%S').date()}</td>
        </tr>
        </t>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <tr>
            <td colspan="2" style="text-align: right;">Подпись: ______________________</td>
    <br><br><br><br>
    <tr>
        <td colspan="2" style="text-align: right;">Уникальный номер документа: {document_number}</td>
    </tr>
    </div>
    </body>

    </html>
    '''

    pdfkit.from_string(rendered, 'result.pdf', options={'encoding': 'utf-8'})
    with open("result.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="Скачать документ",
                       data=PDFbyte,
                       file_name="test.pdf",
                       mime='application/octet-stream')

# Ввод данных с использованием инпутов
st.title('Модель скоринга')
manager = st.sidebar.selectbox(r'$\textsf{\normalsize Менеджер}$', ["Мирзоев Чахонгир", "Нурматов Камолчон", "Махмадияров Бахром", "Зокиров Улугбек"])
district_options = {
    "Мирзоев Чахонгир": "Джаббор Расулов",
    "Нурматов Камолчон": "Спитамен",
    "Махмадияров Бахром": "Пенджикент",
    "Зокиров Улугбек": "Худжанд"
}

default_district = "Душанбе"  # Default district if no match found

district = district_options.get(manager, default_district)

# # Use district variable in your Streamlit app
st.sidebar.write(rf'$\textsf{{\normalsize Филиал}}$: {district}')
# district = st.sidebar.selectbox(r'$\textsf{\normalsize Филиал}$', ["Душанбе", "Худжанд", "Пенджикент", "Джаббор Расулов", "Спитамен"])
name = st.sidebar.text_input(r'$\textsf{\normalsize Имя}$', '')
surname = st.sidebar.text_input(r'$\textsf{\normalsize Фамилия}$', '')
phone = st.sidebar.number_input(r'$\textsf{\normalsize Телефон номер}$', value=None, placeholder="928009292")
age = st.sidebar.number_input(r'$\textsf{\normalsize Возраст}$', value=24, step=1)
gender = st.sidebar.radio(r'$\textsf{\normalsize Пол}$', ['Мужчина', 'Женщина'])
amount = st.sidebar.number_input(r'$\textsf{\normalsize Сумма}$', value=0, placeholder="Телефон нархи")
duration = st.sidebar.selectbox(r'$\textsf{\normalsize Срок}$', [3, 6, 9, 12])
marital_status = st.sidebar.selectbox(r'$\textsf{\normalsize Семейный статус}$', ['Женат/Замужем', 'Не женат/Не замужем', 'Вдова/Вдовец', 'Разведен'])
credit_history_count = st.sidebar.number_input(r'$\textsf{\normalsize Количество кредитов(история)}$', value=0, step=1)

def authenticate_gspread():
    # Load Google Sheets API credentials
    sa = gspread.service_account(filename='credits_mobi.json')
    return sa

# Function to duplicate data to Google Sheets
def duplicate_to_gsheet(new_row):
    # Authenticate with Google Sheets
    gc = authenticate_gspread()

    # Create a new Google Sheets spreadsheet
    sh = gc.open("KreditMarket")

    # Select the first sheet (index 0)
    worksheet = sh.worksheet("Scoring")

    # Check if there's any content in the worksheet
    existing_data = worksheet.get_all_values()

    # Get existing headers if they exist
    headers = existing_data[0] if existing_data else None

    if not headers:
        headers = ['Менеджер', 'Филиал', 'Телефон номер', 'Имя', 'Фамилия', 'Возраст', 'Пол', 'Сумма кредита', 'Период', 'Семейное положение', 'Количество кредитов(история)', 'Результат', 'Вероятность возврата', 'Дата', 'Номер документа']
        worksheet.append_row(headers)

    # Convert the new_row DataFrame to a list and append it to the worksheet
    new_row = new_row[['Manager','district', 'phone', 'name', 'surname', 'age', 'gender', 'amount', 'duration', 'marital_status', "credit_history_count",
                        'Result', 'Probability', 'Date', 'DocumentNumber']]
    new_row_list = new_row.values.tolist()
    worksheet.append_rows(new_row_list)

# Предсказание
if st.sidebar.button('Получить скоринг'):
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    document_number = f'Doc_{current_date.replace(" ", "_").replace(":", "_")}'
    mapping_dis = {
    "Душанбе": "dushanbe",
    "Худжанд": "khujand",
    "Пенджикент": "panjakent",
    "Джаббор Расулов": "j.rasulov",
    "Спитамен": "spitamen"
    }
    mapping_mar = {
        'Женат/Замужем': 'married', 'Не женат/Не замужем':'single', 'Вдова/Вдовец':'widow/widower', 'Разведен':'divorced'
    }

    input_data = pd.DataFrame({
        'age': [age],
        'amount': [amount],
        'credit_history_count': [credit_history_count],
        'district': [mapping_dis[district]],
        'duration': [duration],
        'gender': [1 if gender == 'Мужчина' else 0],
        'marital_status': [mapping_mar[marital_status]],
    })

    prediction = model.predict_proba(input_data)[:, 0]
    st.subheader('Результат:')
    st.write(f'Вероятность возврата: {round(prediction[0]*100, 2)}%')
    input_data['Manager'] = manager
    input_data['district'] = district
    input_data['name'] = name
    input_data['surname'] = surname
    input_data['phone'] = phone
    input_data['Result'] = 'Одобрено' if prediction > 1 - 0.05 else 'Отказано'
    input_data['gender'] = gender
    input_data['marital_status'] = marital_status
    input_data['Probability'] = f'{round(prediction[0]*100, 2)}%'
    input_data['Date'] = current_date
    input_data['DocumentNumber'] = document_number

    if prediction > 1 - 0.05:
        st.success(r'$\textsf{\Large Кредит одобрен! 🎉}$')
        st.balloons()
        duplicate_to_gsheet(input_data)
    else:
        st.error(r'$\textsf{\Large Отказано! 😞}$')
        duplicate_to_gsheet(input_data)

    generate_pdf(input_data, document_number, current_date)