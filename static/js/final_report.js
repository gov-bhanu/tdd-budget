document.addEventListener("DOMContentLoaded", function() {
    fetchData(); // Fetch data when the page loads
});

// Fetch data from the API
function fetchData() {
    fetch('/fetch-data/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                populatefinal_reportTable(data.data, data.department_totals, data.head_name_totals);
            } else {
                alert('Error fetching data: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error fetching data. Please check the console for details.');
        });
}

// Populate the final_report table with data and totals
function populatefinal_reportTable(data, departmentTotals, headNameTotals) {
    const final_reportTableBody = document.getElementById('final_reportTable').getElementsByTagName('tbody')[0];
    final_reportTableBody.innerHTML = '';  // Clear previous table content

    let departmentNamePrev = '';  // Track previous department name for grouping
    let headNamePrev = '';  // Track previous head name for grouping

    // Loop through the data and populate the table
    data.forEach((row, index) => {
        // Add department total row when department changes
        if (row.department_name !== departmentNamePrev) {
            if (departmentNamePrev !== '') {
                // Add the department total row
                final_reportTableBody.insertRow().innerHTML = `
                    <td colspan="4"><strong>${departmentNamePrev} Total</strong></td>
                    <td><strong>${departmentTotals[departmentNamePrev].sanctioned_budget.toFixed(2)}</strong></td>
                    <td><strong>${departmentTotals[departmentNamePrev].revised_estimate.toFixed(2)}</strong></td>
                    <td><strong>${departmentTotals[departmentNamePrev].in_divisible.toFixed(2)}</strong></td>
                    <td><strong>${departmentTotals[departmentNamePrev].divisible.toFixed(2)}</strong></td>
                    <td><strong>${departmentTotals[departmentNamePrev].kinnaur.toFixed(2)}</strong></td>
                    <td><strong>${departmentTotals[departmentNamePrev].lahaul.toFixed(2)}</strong></td>
                    <td><strong>${departmentTotals[departmentNamePrev].spiti.toFixed(2)}</strong></td>
                    <td><strong>${departmentTotals[departmentNamePrev].pangi.toFixed(2)}</strong></td>
                    <td><strong>${departmentTotals[departmentNamePrev].bharmaur.toFixed(2)}</strong></td>
                `;
            }
            // Add the new department row
            departmentNamePrev = row.department_name;
        }

        // Add head total row when head changes
        if (row.head_name !== headNamePrev) {
            if (headNamePrev !== '') {
                // Add the head total row
                final_reportTableBody.insertRow().innerHTML = `
                    <td colspan="4"><strong>${headNamePrev} Total</strong></td>
                    <td><strong>${headNameTotals[headNamePrev].sanctioned_budget.toFixed(2)}</strong></td>
                    <td><strong>${headNameTotals[headNamePrev].revised_estimate.toFixed(2)}</strong></td>
                    <td><strong>${headNameTotals[headNamePrev].in_divisible.toFixed(2)}</strong></td>
                    <td><strong>${headNameTotals[headNamePrev].divisible.toFixed(2)}</strong></td>
                    <td><strong>${headNameTotals[headNamePrev].kinnaur.toFixed(2)}</strong></td>
                    <td><strong>${headNameTotals[headNamePrev].lahaul.toFixed(2)}</strong></td>
                    <td><strong>${headNameTotals[headNamePrev].spiti.toFixed(2)}</strong></td>
                    <td><strong>${headNameTotals[headNamePrev].pangi.toFixed(2)}</strong></td>
                    <td><strong>${headNameTotals[headNamePrev].bharmaur.toFixed(2)}</strong></td>
                `;
            }
            // Add the new head row
            headNamePrev = row.head_name;
        }

        // Add the current row
        const rowElement = final_reportTableBody.insertRow();
        rowElement.innerHTML = `
            <td>${row.department_name}</td>
            <td>${row.head_name}</td>
            <td>${row.scheme_name}</td>
            <td>${row.soe_name}</td>
            <td>${parseFloat(row.sanctioned_budget).toFixed(2)}</td>
            <td>${parseFloat(row.revised_estimate).toFixed(2)}</td>
            <td>${parseFloat(row.in_divisible || 0).toFixed(2)}</td>
            <td>${parseFloat(row.divisible || 0).toFixed(2)}</td>
            <td>${parseFloat(row.kinnaur || 0).toFixed(2)}</td>
            <td>${parseFloat(row.lahaul || 0).toFixed(2)}</td>
            <td>${parseFloat(row.spiti || 0).toFixed(2)}</td>
            <td>${parseFloat(row.pangi || 0).toFixed(2)}</td>
            <td>${parseFloat(row.bharmaur || 0).toFixed(2)}</td>
        `;
    });

    // Add final department total
    final_reportTableBody.insertRow().innerHTML = `
        <td colspan="4"><strong>${departmentNamePrev} Total</strong></td>
        <td><strong>${departmentTotals[departmentNamePrev].sanctioned_budget.toFixed(2)}</strong></td>
        <td><strong>${departmentTotals[departmentNamePrev].revised_estimate.toFixed(2)}</strong></td>
        <td><strong>${departmentTotals[departmentNamePrev].in_divisible.toFixed(2)}</strong></td>
        <td><strong>${departmentTotals[departmentNamePrev].divisible.toFixed(2)}</strong></td>
        <td><strong>${departmentTotals[departmentNamePrev].kinnaur.toFixed(2)}</strong></td>
        <td><strong>${departmentTotals[departmentNamePrev].lahaul.toFixed(2)}</strong></td>
        <td><strong>${departmentTotals[departmentNamePrev].spiti.toFixed(2)}</strong></td>
        <td><strong>${departmentTotals[departmentNamePrev].pangi.toFixed(2)}</strong></td>
        <td><strong>${departmentTotals[departmentNamePrev].bharmaur.toFixed(2)}</strong></td>
    `;
}




// Export table data to Excel
function exportToExcel() {
    const table = document.getElementById('final_reportTable');  // Use your table ID
    const rows = table.getElementsByTagName('tr');
    const sheetData = [];
    
    // Get table header
    const headers = [];
    const headerCells = rows[0].getElementsByTagName('th');
    for (let i = 0; i < headerCells.length; i++) {
        headers.push(headerCells[i].textContent.trim());
    }
    sheetData.push(headers);

    // Get table rows
    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName('td');
        const rowData = [];
        for (let j = 0; j < cells.length; j++) {
            rowData.push(cells[j].textContent.trim());
        }
        sheetData.push(rowData);
    }

    // Create a workbook and a worksheet
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(sheetData);
    XLSX.utils.book_append_sheet(wb, ws, "final_report Data");

    // Export to Excel
    XLSX.writeFile(wb, 'department_final_report.xlsx');
}
