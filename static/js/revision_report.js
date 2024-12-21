document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('filterButton').addEventListener('click', fetchFilteredData);

    fetchRevisionData(); // Initial fetch
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

// Populate the revision report table with sorted and grouped data
function populateRevisionReportTable(data) {
    const revisionReportTableBody = document.getElementById('revisionReportTable').getElementsByTagName('tbody')[0];
    revisionReportTableBody.innerHTML = ''; // Clear previous table content

    // Sort the data by `head_name`
    data.sort((a, b) => (a.head_name || '').localeCompare(b.head_name || ''));

    let headNamePrev = '';
    let departmentPrev = '';
    let schemePrev = '';
    let totalRowAdded = {}; // Object to track if total row has been added for a given head_name

    data.forEach((row) => {
        if (!row) return; // Skip null/undefined rows

        const {
            department_name = '',
            head_name = '',
            scheme_name = '',
            soe_name = '',
            sanctioned_budget = 0,
            revised_estimate = 0,
            excess = 0,
            surrender = 0,
            last_change_date = '',
        } = row;

        // Insert regular rows
        if (!head_name.endsWith('Total')) {
            revisionReportTableBody.insertRow().innerHTML = `
                <td>${departmentPrev !== department_name ? department_name : ''}</td>
                <td>${schemePrev !== scheme_name ? scheme_name : ''}</td>
                <td>${headNamePrev !== head_name ? head_name : ''}</td>
                <td>${soe_name}</td>
                <td>${parseFloat(sanctioned_budget).toFixed(2)}</td>
                <td>${parseFloat(revised_estimate).toFixed(2)}</td>
                <td>${parseFloat(excess || 0).toFixed(2)}</td>
                <td>${parseFloat(surrender || 0).toFixed(2)}</td>
                <td>${new Date(last_change_date).toLocaleDateString()}</td>
            `;
        } else {
            // If we encounter a row that is a total row for a head
            // Prevent duplicate total rows for the same head_name
            if (!totalRowAdded[head_name]) {
                totalRowAdded[head_name] = true;

                // Insert a summary row for the total row with no date
                revisionReportTableBody.insertRow().innerHTML = `
                    <td></td>
                    <td></td>
                    <td><strong>${head_name}</strong></td>
                    <td></td>
                    <td>${parseFloat(sanctioned_budget).toFixed(2)}</td>
                    <td>${parseFloat(revised_estimate).toFixed(2)}</td>
                    <td>${parseFloat(excess).toFixed(2)}</td>
                    <td>${parseFloat(surrender).toFixed(2)}</td>
                    <td></td> <!-- Empty date for summary row -->
                `;
            }
        }

        // Track previous values to prevent duplicates in the next row
        departmentPrev = department_name;
        schemePrev = scheme_name;
        headNamePrev = head_name;
    });
}





// Filter the data based on the date range
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
