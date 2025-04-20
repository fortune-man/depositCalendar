let workRowCount = 0;

function toggleTable() {
    document.getElementById('expenseTable').style.display = document.getElementById('tab').value === '작업 일보' ? 'block' : 'none';
    document.getElementById('workTable').style.display = document.getElementById('tab').value === '출역 현황' ? 'block' : 'none';
}

function saveCell(element) {
    const tab = element.getAttribute('data-tab');
    const row = element.getAttribute('data-row');
    const col = element.getAttribute('data-col');
    const value = element.value;

    fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `tab=${tab}&row=${row}&col=${col}&value=${value}`
    }).then(response => response.text())
      .then(data => {
          element.classList.add('input-feedback');
          setTimeout(() => element.classList.add('saved'), 300);
      });
}

function addRow(tabId) {
    const table = document.querySelector(`#${tabId} table tbody`);
    const rowCount = table.rows.length;
    const newRow = table.insertRow();
    
    if (tabId === 'expenseTable') {
        const cols = ['직종', '소속팀', '전월 누계', '전일 누계', '금일 출역', '금일 누계', '총 누계', '비고', '금일 작업 내용', '금일 작업 수량'];
        for (let i = 0; i < cols.length; i++) {
            const cell = newRow.insertCell(i);
            if (i === 0) {
                cell.innerHTML = `<input type="text" name="value" class="form-control" data-tab="작업 일보" data-row="${rowCount + 1}" data-col="직종" placeholder="직종" onblur="saveCell(this)">`;
            } else if (cols[i] === '총 누계') {
                cell.innerHTML = `<span>0</span>`;
            } else {
                cell.innerHTML = `<input type="text" name="value" class="form-control" data-tab="작업 일보" data-row="${rowCount + 1}" data-col="${cols[i]}" placeholder="${cols[i]}" onblur="saveCell(this)">`;
            }
        }
    } else {
        const cols = ['번호', '직종', '성명', '공수', '작업 내용', '담당', '금액'];
        for (let i = 0; i < cols.length; i++) {
            const cell = newRow.insertCell(i);
            if (i === 0) {
                cell.textContent = rowCount + 1;
            } else {
                cell.innerHTML = `<input type="text" name="value" class="form-control" data-tab="출역 현황" data-row="${rowCount + 1}" data-col="${cols[i]}" placeholder="${cols[i]}" list="task-list" onblur="saveCell(this)">`;
            }
        }
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

function deleteRow(tabId) {
    const table = document.querySelector(`#${tabId} table tbody`);
    if (table.rows.length > 1) {
        table.deleteRow(table.rows.length - 1);
    }
}

function copyRow(tabId) {
    const table = document.querySelector(`#${tabId} table tbody`);
    const lastRow = table.rows[table.rows.length - 1];
    const newRow = table.insertRow();
    for (let i = 0; i < lastRow.cells.length; i++) {
        const cell = newRow.insertCell(i);
        cell.innerHTML = lastRow.cells[i].innerHTML;
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