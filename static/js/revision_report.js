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

// Export table data to Excel
function exportToExcel() {
    const table = document.getElementById('revisionReportTable');
    const wb = XLSX.utils.table_to_book(table, {sheet: "Revision Report"});
    XLSX.writeFile(wb, 'revision_report.xlsx');
}
