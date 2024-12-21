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




function populateSupplementaryReportTable(data) {
    const supplementaryReportTableBody = document.getElementById('supplementaryReportTable').getElementsByTagName('tbody')[0];
    supplementaryReportTableBody.innerHTML = ''; // Clear previous table content

    // Sort the data by `head_name`
    data.sort((a, b) => (a.head_name || '').localeCompare(b.head_name || ''));

    let headNamePrev = '';
    let departmentPrev = '';
    let schemePrev = '';
    let totalRowAdded = {}; // Object to track if total row has been added for a given head_name

    // Variables to accumulate totals for each head_name
    let accumulatedSanctionedBudget = 0;
    let accumulatedRevisedEstimate = 0;
    let accumulatedExcess = 0;
    let accumulatedSurrender = 0;

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
        } = row;

        // Insert regular rows (non-total)
        if (!head_name.endsWith('Total')) {
            // Add values to the accumulation
            accumulatedSanctionedBudget += parseFloat(sanctioned_budget);
            accumulatedRevisedEstimate += parseFloat(revised_estimate);
            accumulatedExcess += parseFloat(excess || 0);
            accumulatedSurrender += parseFloat(surrender || 0);

            supplementaryReportTableBody.insertRow().innerHTML = `
                <td>${departmentPrev !== department_name ? department_name : ''}</td>
                <td>${schemePrev !== scheme_name ? scheme_name : ''}</td>
                <td>${headNamePrev !== head_name ? head_name : ''}</td>
                <td>${soe_name}</td>
                <td>${parseFloat(sanctioned_budget).toFixed(2)}</td>
                <td>${parseFloat(revised_estimate).toFixed(2)}</td>
                <td>${parseFloat(excess || 0).toFixed(2)}</td>
                <td>${parseFloat(surrender || 0).toFixed(2)}</td>
            `;
        } else {
            // If we encounter a total row, insert it after processing the regular rows
            if (!totalRowAdded[head_name]) {
                totalRowAdded[head_name] = true;

                // Insert a summary row for the total with accumulated totals
                supplementaryReportTableBody.insertRow().innerHTML = `
                    <td></td>
                    <td></td>
                    <td><strong>${head_name}</strong></td>
                    <td></td>
                    <td><strong>${accumulatedSanctionedBudget.toFixed(2)}</strong></td>
                    <td><strong>${accumulatedRevisedEstimate.toFixed(2)}</strong></td>
                    <td><strong>${accumulatedExcess.toFixed(2)}</strong></td>
                    <td><strong>${accumulatedSurrender.toFixed(2)}</strong></td>
                `;

                // Reset the accumulated totals for the next head_name group
                accumulatedSanctionedBudget = 0;
                accumulatedRevisedEstimate = 0;
                accumulatedExcess = 0;
                accumulatedSurrender = 0;
            }
        }

        // Track previous values to prevent duplicates in the next row
        departmentPrev = department_name;
        schemePrev = scheme_name;
        headNamePrev = head_name;
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
