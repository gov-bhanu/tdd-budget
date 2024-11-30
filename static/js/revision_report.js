document.addEventListener("DOMContentLoaded", function() {
    fetchRevisionData(); // Fetch data when the page loads
    document.getElementById('exportToExcel').addEventListener('click', exportToExcel); // Add event listener for the button
});

// Fetch data from the API
function fetchRevisionData() {
    fetch('/fetch-revision-data/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                populateRevisionReportTable(data.data);
            } else {
                alert('Error fetching data: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error fetching data. Please check the console for details.');
        });
}

// Populate the revision report table with data
function populateRevisionReportTable(data) {
    const revisionReportTableBody = document.getElementById('revisionReportTable').getElementsByTagName('tbody')[0];
    revisionReportTableBody.innerHTML = '';  // Clear previous table content

    // Loop through the data and populate the table
    data.forEach((row) => {
        const rowElement = revisionReportTableBody.insertRow();
        rowElement.innerHTML = `
            <td>${row.department_name}</td>
            <td>${row.head_name}</td>
            <td>${row.scheme_name}</td>
            <td>${row.soe_name}</td>
            <td>${parseFloat(row.sanctioned_budget).toFixed(2)}</td>
            <td>${parseFloat(row.revised_estimate).toFixed(2)}</td>
            <td>${parseFloat(row.excess || 0).toFixed(2)}</td>
            <td>${parseFloat(row.surrender || 0).toFixed(2)}</td>
            <td>${parseFloat(row.variation || 0).toFixed(2)}</td>
        `;
    });
}



// Function to export a table to Excel
function exportToExcel(tableId, filename = 'excel_data') {
    // Get the table element by its ID
    const table = document.getElementById(tableId);

    // Check if the table exists
    if (!table) {
        console.error(`Table with ID "${tableId}" not found.`);
        return;
    }

    // Create a workbook and worksheet from the table
    const workbook = XLSX.utils.book_new();
    const worksheet = XLSX.utils.table_to_sheet(table);

    // Append the worksheet to the workbook
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');

    // Trigger the Excel file download
    XLSX.writeFile(workbook, `${filename}.xlsx`);
}
