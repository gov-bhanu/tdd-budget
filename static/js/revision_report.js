document.addEventListener("DOMContentLoaded", function () {
    fetchRevisionData(); // Fetch data when the page loads
    document.getElementById('exportToExcel').addEventListener('click', exportToExcel); // Add event listener for the button
});

// Fetch data from the API
function fetchRevisionData() {
    fetch('/fetch-revision-data/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                populateRevisionReportTable(data.data, data.head_name_totals);
            } else {
                alert('Error fetching data: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error fetching data. Please check the console for details.');
        });
}

// Populate the revision report table with sorted and grouped data
function populateRevisionReportTable(data, headNameTotals) {
    const revisionReportTableBody = document.getElementById('revisionReportTable').getElementsByTagName('tbody')[0];
    revisionReportTableBody.innerHTML = ''; // Clear previous table content

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
                };

                revisionReportTableBody.insertRow().innerHTML = `
                    <td></td>
                    <td></td>
                    <td><strong>${headNamePrev} Total</strong></td>
                    <td></td>
                    <td><strong>${totals.sanctioned_budget.toFixed(2)}</strong></td>
                    <td><strong>${totals.revised_estimate.toFixed(2)}</strong></td>
                    <td><strong>${totals.excess.toFixed(2)}</strong></td>
                    <td><strong>${totals.surrender.toFixed(2)}</strong></td>
                    <td></td>
                `;
            }
            // Update the previous head name
            headNamePrev = row.head_name;
        }

        // Show department_name and scheme_name only when they change
        const showDepartmentName = row.department_name !== departmentNamePrev;
        const showSchemeName = row.scheme_name !== schemeNamePrev;

        // Add the current row
        const rowElement = revisionReportTableBody.insertRow();
        rowElement.innerHTML = `
            <td>${showDepartmentName ? row.department_name : ''}</td>
            <td>${showSchemeName ? row.scheme_name : ''}</td>
            <td>${row.head_name}</td> <!-- Only show head_name here for the first row in each group -->
            <td>${row.soe_name}</td>
            <td>${parseFloat(row.sanctioned_budget).toFixed(2)}</td>
            <td>${parseFloat(row.revised_estimate).toFixed(2)}</td>
            <td>${parseFloat(row.excess || 0).toFixed(2)}</td>
            <td>${parseFloat(row.surrender || 0).toFixed(2)}</td>
            <td>${new Date(row.last_change_date).toLocaleDateString()}</td>
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
        };

        revisionReportTableBody.insertRow().innerHTML = `
            <td></td>
            <td></td>
            <td><strong>${headNamePrev} Total</strong></td>
            <td></td>
            <td><strong>${totals.sanctioned_budget.toFixed(2)}</strong></td>
            <td><strong>${totals.revised_estimate.toFixed(2)}</strong></td>
            <td><strong>${totals.excess.toFixed(2)}</strong></td>
            <td><strong>${totals.surrender.toFixed(2)}</strong></td>
            <td></td>
        `;
    }
}



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





// filteration based on date range
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('filterButton').addEventListener('click', fetchFilteredData);

    fetchRevisionData(); // Initial fetch
});

function fetchFilteredData() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    const url = new URL('/fetch-revision-data/', window.location.origin);
    if (startDate) url.searchParams.append('start_date', startDate);
    if (endDate) url.searchParams.append('end_date', endDate);

    fetch(url)
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
