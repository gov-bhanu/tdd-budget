function populateFinalReport(data) {
    const soeTotalTableBody = document.getElementById('soeTotalTable').getElementsByTagName('tbody')[0];
    const departmentTotalTableBody = document.getElementById('departmentTotalTable').getElementsByTagName('tbody')[0];

    let soeTotals = {}; // To store totals by SOE name
    let departmentTotals = {}; // To store totals by Department name

    // Loop through the data to accumulate totals by SOE and Department
    data.forEach((row) => {
        if (!row) return;

        const {
            department_name = '',
            soe_name = '',
            sanctioned_budget = 0,
            revised_estimate = 0,
            excess = 0,
            surrender = 0,
        } = row;

        // Accumulate totals by SOE name
        if (!soeTotals[soe_name]) {
            soeTotals[soe_name] = {
                sanctioned_budget: 0,
                revised_estimate: 0,
                excess: 0,
                surrender: 0,
            };
        }
        soeTotals[soe_name].sanctioned_budget += parseFloat(sanctioned_budget);
        soeTotals[soe_name].revised_estimate += parseFloat(revised_estimate);
        soeTotals[soe_name].excess += parseFloat(excess || 0);
        soeTotals[soe_name].surrender += parseFloat(surrender || 0);

        // Accumulate totals by Department name
        if (!departmentTotals[department_name]) {
            departmentTotals[department_name] = {
                sanctioned_budget: 0,
                revised_estimate: 0,
                excess: 0,
                surrender: 0,
            };
        }
        departmentTotals[department_name].sanctioned_budget += parseFloat(sanctioned_budget);
        departmentTotals[department_name].revised_estimate += parseFloat(revised_estimate);
        departmentTotals[department_name].excess += parseFloat(excess || 0);
        departmentTotals[department_name].surrender += parseFloat(surrender || 0);
    });

    // Populate the SOE Name wise total table
    Object.keys(soeTotals).forEach((soe_name) => {
        const total = soeTotals[soe_name];
        soeTotalTableBody.insertRow().innerHTML = `
            <td>${soe_name}</td>
            <td>${total.sanctioned_budget.toFixed(2)}</td>
            <td>${total.revised_estimate.toFixed(2)}</td>
            <td>${total.excess.toFixed(2)}</td>
            <td>${total.surrender.toFixed(2)}</td>
        `;
    });

    // Populate the Department wise total table
    Object.keys(departmentTotals).forEach((department_name) => {
        const total = departmentTotals[department_name];
        departmentTotalTableBody.insertRow().innerHTML = `
            <td>${department_name}</td>
            <td>${total.sanctioned_budget.toFixed(2)}</td>
            <td>${total.revised_estimate.toFixed(2)}</td>
            <td>${total.excess.toFixed(2)}</td>
            <td>${total.surrender.toFixed(2)}</td>
        `;
    });
}

// Call the function to populate the final report
populateFinalReport(data);




// Function to export a table to Excel
function exportToExcel(tableId, filename = 'excel_data') {
    const table = document.getElementById(tableId);
    if (!table) {
        console.error(`Table with ID "${tableId}" not found.`);
        return;
    }
    const workbook = XLSX.utils.book_new();
    const worksheet = XLSX.utils.table_to_sheet(table);
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
    XLSX.writeFile(workbook, `${filename}.xlsx`);
}
