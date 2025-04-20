from flask import Flask, render_template, request
import os

app = Flask(__name__)

# 데이터 파일 경로
DATA_FILE = 'expenses.txt'

# 데이터 로드 함수
def load_data():
    data = {'작업 일보': {}, '출역 현황': {}}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                tab, row, col, value = line.strip().split('|')
                if tab not in data:
                    data[tab] = {}
                if row not in data[tab]:
                    data[tab][row] = {}
                data[tab][row][col] = value
    return data

# 데이터 저장 함수
def save_data(tab, row, col, value):
    with open(DATA_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{tab}|{row}|{col}|{value}\n")

# 소계/총계 계산 함수
def calculate_totals(data):
    # 작업 일보 소계/총계 계산
    expense_data = data['작업 일보']
    subtotal_rows = [21, 43]
    subtotals = {'전월 누계': 0, '전일 누계': 0, '금일 출역': 0, '금일 누계': 0, '총 누계': 0}
    totals = {'전월 누계': 0, '전일 누계': 0, '금일 출역': 0, '금일 누계': 0, '총 누계': 0}

    for row in range(1, 48):
        row_str = str(row)
        if row_str not in expense_data:
            expense_data[row_str] = {}
        prev_month = float(expense_data[row_str].get('전월 누계', '0')) or 0
        prev_day = float(expense_data[row_str].get('전일 누계', '0')) or 0
        today_work = float(expense_data[row_str].get('금일 출역', '0')) or 0
        today_total = float(expense_data[row_str].get('금일 누계', '0')) or 0
        total = prev_month + today_work
        expense_data[row_str]['총 누계'] = str(total)

        subtotals['전월 누계'] += prev_month
        subtotals['전일 누계'] += prev_day
        subtotals['금일 출역'] += today_work
        subtotals['금일 누계'] += today_total
        subtotals['총 누계'] += total
        totals['전월 누계'] += prev_month
        totals['전일 누계'] += prev_day
        totals['금일 출역'] += today_work
        totals['금일 누계'] += today_total
        totals['총 누계'] += total

        if row in subtotal_rows:
            expense_data[str(row)] = {
                '직종': '소계',
                '전월 누계': str(subtotals['전월 누계']),
                '전일 누계': str(subtotals['전일 누계']),
                '금일 출역': str(subtotals['금일 출역']),
                '금일 누계': str(subtotals['금일 누계']),
                '총 누계': str(subtotals['총 누계'])
            }
            subtotals = {'전월 누계': 0, '전일 누계': 0, '금일 출역': 0, '금일 누계': 0, '총 누계': 0}

    expense_data['48'] = {
        '직종': '총계',
        '전월 누계': str(totals['전월 누계']),
        '전일 누계': str(totals['전일 누계']),
        '금일 출역': str(totals['금일 출역']),
        '금일 누계': str(totals['금일 누계']),
        '총 누계': str(totals['총 누계'])
    }

    # 출역 현황 총계 계산
    work_data = data['출역 현황']
    total_work_days = 0
    total_amount = 0
    for row in range(1, 80):
        row_str = str(row)
        if row_str in work_data:
            work_days = float(work_data[row_str].get('공수', '0')) or 0
            amount = float(work_data[row_str].get('금액', '0')) or 0
            total_work_days += work_days
            total_amount += amount
    work_data['80'] = {
        '공수': str(total_work_days),
        '금액': str(total_amount)
    }

    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    # 데이터 로드
    table_data = load_data()

    # POST 요청 처리 (데이터 저장)
    if request.method == 'POST':
        tab = request.form.get('tab')
        row = request.form.get('row')
        col = request.form.get('col')
        value = request.form.get('value')
        save_data(tab, row, col, value)
        # 데이터 갱신 후 재계산
        table_data = load_data()
        table_data = calculate_totals(table_data)
        return '', 204

    # 초기 데이터 계산
    table_data = calculate_totals(table_data)
    return render_template('index.html', table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True)