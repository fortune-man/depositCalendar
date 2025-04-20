from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        date = request.form['date']
        amount = request.form['amount']
        item = request.form['item']
        expense = f"{date},{amount},{item}"
        with open('expenses.txt', 'a') as f:
            f.write(expense + '\n')
    try:
        with open('expenses.txt', 'r') as f:
            expenses = f.readlines()
    except:
        expenses = []
    return render_template('index.html', expenses=expenses)

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    with open('expenses.txt', 'r') as f:
        expenses = f.readlines()
    if request.method == 'POST':
        date = request.form['date']
        amount = request.form['amount']
        item = request.form['item']
        expenses[index] = f"{date},{amount},{item}\n"
        with open('expenses.txt', 'w') as f:
            f.writelines(expenses)
        return redirect(url_for('home'))
    expense = expenses[index].strip().split(',')
    return render_template('edit.html', expense=expense, index=index)

@app.route('/delete/<int:index>')
def delete(index):
    with open('expenses.txt', 'r') as f:
        expenses = f.readlines()
    expenses.pop(index)
    with open('expenses.txt', 'w') as f:
        f.writelines(expenses)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()