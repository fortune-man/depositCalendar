let workRowCount = 0;

function toggleTable() {
    document.getElementById('expenseTable').style.display = document.getElementById('tab').value === '작업 일보' ? 'block' : 'none';
    document.getElementById('workTable').style.display = document.getElementById('tab').value === '출역 현황' ? 'block' : 'none';
}

function saveCell(input) {
    const tab = input.getAttribute('data-tab');
    const row = input.getAttribute('data-row');
    const col = input.getAttribute('data-col');
    const value = input.value;
    fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `tab=${tab}&row=${row}&col=${col}&value=${value}`
    }).then(() => {
        input.classList.add('input-feedback', 'saved');
        // 새로고침하여 백엔드에서 계산된 값을 반영
        location.reload();
    });
}

function addRow(tableId) {
    const table = document.getElementById(tableId === 'expenseTable' ? 'expense-table' : 'work-table');
    const rowCount = table.rows.length - (tableId === 'workTable' ? 1 : 2);
    const row = table.insertRow(rowCount);
    if (tableId === 'expenseTable') {
        appendExpenseRowCells(row, rowCount);
    } else {
        workRowCount++;
        appendWorkRowCells(row, workRowCount);
    }
}

function appendExpenseRowCells(row, rowCount) {
    const cols = ['직종', '소속팀', '전월 누계', '전일 누계', '금일 출역', '금일 누계', '총 누계', '비고', '금일 작업 내용', '금일 작업 수량'];
    cols.forEach((col, i) => {
        const cell = row.insertCell(i);
        if (i === 6) {
            cell.innerHTML = `<span id="expense-total-${rowCount}-${i}">0</span>`;
        } else {
            cell.innerHTML = `<input type="text" name="value" class="form-control" data-tab="작업 일보" data-row="${rowCount}" data-col="${col}" placeholder="${col}" onblur="saveCell(this)">`;
        }
    });
}

function appendWorkRowCells(row, rowCount) {
    row.insertCell(0).textContent = rowCount;
    const cols = ['직종', '성명', '공수', '작업 내용', '담당', '금액 PDC'];
    cols.forEach((col, i) => {
        const cell = row.insertCell(i + 1);
        cell.innerHTML = `<input type="text" name="value" class="form-control" data-tab="출역 현황" data-row="${rowCount}" data-col="${col}" placeholder="${col}" ${col === '작업 내용' ? 'list="task-list"' : ''} onblur="saveCell(this)">`;
    });
}

function deleteRow(tableId) {
    const table = document.getElementById(tableId === 'expenseTable' ? 'expense-table' : 'work-table');
    if (table.rows.length <= (tableId === 'expenseTable' ? 49 : 81)) return;
    table.deleteRow(table.rows.length - (tableId === 'workTable' ? 2 : 3));
    if (tableId === 'workTable') workRowCount--;
}

function copyRow(tableId) {
    const table = document.getElementById(tableId === 'expenseTable' ? 'expense-table' : 'work-table');
    const rowCount = table.rows.length - (tableId === 'workTable' ? 1 : 2);
    if (rowCount <= 1) return;
    const lastRow = table.rows[rowCount - (tableId === 'workTable' ? 1 : 2)];
    const newRow = table.insertRow(rowCount);
    if (tableId === 'expenseTable') {
        copyExpenseRow(lastRow, newRow, rowCount);
    } else {
        workRowCount++;
        copyWorkRow(lastRow, newRow, workRowCount);
    }
}

function copyExpenseRow(lastRow, newRow, rowCount) {
    const cols = ['직종', '소속팀', '전월 누계', '전일 누계', '금일 출역', '금일 누계', '총 누계', '비고', '금일 작업 내용', '금일 작업 수량'];
    cols.forEach((col, i) => {
        const cell = newRow.insertCell(i);
        const value = lastRow.cells[i].querySelector('input') ? lastRow.cells[i].querySelector('input').value : '0';
        cell.innerHTML = i === 6
            ? `<span id="expense-total-${rowCount}-${i}">${value}</span>`
            : `<input type="text" name="value" class="form-control" data-tab="작업 일보" data-row="${rowCount}" data-col="${col}" value="${value}" placeholder="${col}" onblur="saveCell(this)">`;
    });
}

function copyWorkRow(lastRow, newRow, rowCount) {
    newRow.insertCell(0).textContent = rowCount;
    const cols = ['직종', '성명', '공수', '작업 내용', '담당', '금액'];
    cols.forEach((col, i) => {
        const cell = newRow.insertCell(i + 1);
        const value = lastRow.cells[i + 1].querySelector('input').value;
        cell.innerHTML = `<input type="text" name="value" class="form-control" data-tab="출역 현황" data-row="${rowCount}" data-col="${col}" value="${value}" placeholder="${col}" ${col === '작업 내용' ? 'list="task-list"' : ''} onblur="saveCell(this)">`;
    });
}