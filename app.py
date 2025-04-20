from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses 
                 (tab TEXT, row TEXT, col TEXT, value TEXT)''')
    conn.commit()
    conn.close()

def load_data():
    data = {'작업 일보': {}, '출역 현황': {}}
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT tab, row, col, value FROM expenses")
    for tab, row, col, value in c.fetchall():
        if tab not in data:
            data[tab] = {}
        if row not in data[tab]:
            data[tab][row] = {}
        data[tab][row][col] = value
    conn.close()
    return data

def save_data(tab, row, col, value):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (tab, row, col, value) VALUES (?, ?, ?, ?)", 
              (tab, row, col, value))
    conn.commit()
    conn.close()

def update_summary_row(row_data, totals, label):
    return {
        '직종': label,
        '소속팀': row_data.get('소속팀', ''),
        '전월 누계': str(totals['전월 누계']),
        '전일 누계': str(totals['전일 누계']),
        '금일 출역': str(totals['금일 출역']),
        '금일 누계': str(totals['금일 누계']),
        '총 누계': str(totals['총 누계']),
        '비고': row_data.get('비고', ''),
        '금일 작업 내용': row_data.get('금일 작업 내용', ''),
        '금일 작업 수량': row_data.get('금일 작업 수량', '')
    }

def calculate_totals(data):
    expense_data = data['작업 일보']
    subtotal_rows = [21, 43]
    subtotals = {'전월 누계': 0, '전일 누계': 0, '금일 출역': 0, '금일 누계': 0, '총 누계': 0}
    totals = {'전월 누계': 0, '전일 누계': 0, '금일 출역': 0, '금일 누계': 0, '총 누계': 0}

    for row in range(1, 48):
        row_str = str(row)
        if row_str not in expense_data:
            expense_data[row_str] = {}
        try:
            prev_month = float(expense_data[row_str].get('전월 누계', '0') or 0)
            prev_day = float(expense_data[row_str].get('전일 누계', '0') or 0)
            today_work = float(expense_data[row_str].get('금일 출역', '0') or 0)
            today_total = float(expense_data[row_str].get('금일 누계', '0') or 0)
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
                expense_data[str(row)] = update_summary_row(expense_data[str(row)], subtotals, '소계')
                subtotals = {'전월 누계': 0, '전일 누계': 0, '금일 출역': 0, '금일 누계': 0, '총 누계': 0}
        except ValueError:
            continue

    expense_data['48'] = update_summary_row(expense_data.get('48', {}), totals, '총계')
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    init_db()
    table_data = load_data()

    if request.method == 'POST':
        tab = request.form.get('tab')
        row = request.form.get('row')
        col = request.form.get('col')
        value = request.form.get('value')
        save_data(tab, row, col, value)
        table_data = load_data()
        table_data = calculate_totals(table_data)
        return '', 204

    table_data = calculate_totals(table_data)
    return render_template('index.html', table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True)