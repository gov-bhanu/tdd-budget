document.addEventListener("DOMContentLoaded", function() {
    fetchSupplementaryData(); // Fetch data when the page loads
});

// Fetch data from the API
function fetchSupplementaryData() {
    fetch('/fetch-supplementary-data/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                populateSupplementaryReportTable(data.data, data.head_name_totals);
            } else {
                alert('Error fetching data: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error fetching data. Please check the console for details.');
        });
}







function populateSupplementaryReportTable(data, headNameTotals) {
    const supplementaryReportTableBody = document.getElementById('supplementaryReportTable').getElementsByTagName('tbody')[0];
    supplementaryReportTableBody.innerHTML = ''; // Clear previous table content

    // Sort the data by `head_name`
    data.sort((a, b) => a.head_name.localeCompare(b.head_name));

    let headNamePrev = ''; // Track previous head name for grouping
    let departmentNamePrev = ''; // Track previous department name for grouping
    let schemeNamePrev = ''; // Track previous scheme name for grouping

    // Loop through the data and populate the table
    data.forEach((row) => {
        // Add head total row when head changes
        if (row.head_name !== headNamePrev) {
            if (headNamePrev !== '') {
                const totals = headNameTotals[headNamePrev] || {
                    sanctioned_budget: 0,
                    revised_estimate: 0,
                    excess: 0,
                    surrender: 0,
                    variation: 0,
                };

                supplementaryReportTableBody.insertRow().innerHTML = `
                    <td></td>
                    <td></td>
                    <td><strong>${headNamePrev} Total</strong></td>
                    <td></td>
                    <td><strong>${totals.sanctioned_budget.toFixed(2)}</strong></td>
                    <td><strong>${totals.revised_estimate.toFixed(2)}</strong></td>
                    <td><strong>${totals.excess.toFixed(2)}</strong></td>
                    <td><strong>${totals.surrender.toFixed(2)}</strong></td>
                    <td><strong>${totals.variation.toFixed(2)}</strong></td>
                `;
            }
            // Update the previous head name
            headNamePrev = row.head_name;
        }

        // Show department_name and scheme_name only when they change
        const showDepartmentName = row.department_name !== departmentNamePrev;
        const showSchemeName = row.scheme_name !== schemeNamePrev;
        
        // Add the current row
        const rowElement = supplementaryReportTableBody.insertRow();
        rowElement.innerHTML = `
            <td>${showDepartmentName ? row.department_name : ''}</td>
            <td>${showSchemeName ? row.scheme_name : ''}</td>
            <td>${row.head_name}</td>  <!-- Only show head_name here for the first row in each group -->
            <td>${row.soe_name}</td>
            <td>${parseFloat(row.sanctioned_budget).toFixed(2)}</td>
            <td>${parseFloat(row.revised_estimate).toFixed(2)}</td>
            <td>${parseFloat(row.excess || 0).toFixed(2)}</td>
            <td>${parseFloat(row.surrender || 0).toFixed(2)}</td>
            <td>${parseFloat(row.variation || 0).toFixed(2)}</td>
        `;

        // Update the previous department, scheme, and head names
        departmentNamePrev = row.department_name;
        schemeNamePrev = row.scheme_name;
    });

    // Add the final head total
    if (headNamePrev !== '') {
        const totals = headNameTotals[headNamePrev] || {
            sanctioned_budget: 0,
            revised_estimate: 0,
            excess: 0,
            surrender: 0,
            variation: 0,
        };

        supplementaryReportTableBody.insertRow().innerHTML = `
            <td></td>
            <td></td>
            <td><strong>${headNamePrev} Total</strong></td>
            <td></td>
            <td><strong>${totals.sanctioned_budget.toFixed(2)}</strong></td>
            <td><strong>${totals.revised_estimate.toFixed(2)}</strong></td>
            <td><strong>${totals.excess.toFixed(2)}</strong></td>
            <td><strong>${totals.surrender.toFixed(2)}</strong></td>
            <td><strong>${totals.variation.toFixed(2)}</strong></td>
        `;
    }
}








// Export Excel thing
document.addEventListener("DOMContentLoaded", function () {
    fetchSupplementaryData(); // Fetch data when the page loads

    // Add click event for the Export to Excel button
    document.getElementById('exportToExcel').addEventListener('click', function () {
        exportTableToExcel('supplementaryReportTable', 'Supplementary_Report');
    });
});

// Function to export the table to Excel
function exportTableToExcel(tableId, filename = 'excel_data') {
    // Get the table element
    const table = document.getElementById(tableId);

    // Create a workbook and worksheet
    const workbook = XLSX.utils.book_new();
    const worksheet = XLSX.utils.table_to_sheet(table);

    // Append worksheet to workbook
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');

    // Trigger Excel file download
    XLSX.writeFile(workbook, `${filename}.xlsx`);
}