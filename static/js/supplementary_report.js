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

// Populate the supplementary report table with data and totals
function populateSupplementaryReportTable(data, headNameTotals) {
    const supplementaryReportTableBody = document.getElementById('supplementaryReportTable').getElementsByTagName('tbody')[0];
    supplementaryReportTableBody.innerHTML = ''; // Clear previous table content

    // Sort the data by `head_name`
    data.sort((a, b) => a.head_name.localeCompare(b.head_name));

    let headNamePrev = ''; // Track previous head name for grouping

    // Loop through the data and populate the table
    data.forEach((row, index) => {
        // Add head total row when head changes
        if (row.head_name !== headNamePrev) {
            if (headNamePrev !== '') {
                supplementaryReportTableBody.insertRow().innerHTML = `
                    <td colspan="4"><strong>${headNamePrev} Total</strong></td>
                    <td><strong>${headNameTotals[headNamePrev].sanctioned_budget.toFixed(2)}</strong></td>
                    <td><strong>${headNameTotals[headNamePrev].revised_estimate.toFixed(2)}</strong></td>
                    <td><strong>${headNameTotals[headNamePrev].excess.toFixed(2)}</strong></td>
                    <td><strong>${headNameTotals[headNamePrev].surrender.toFixed(2)}</strong></td>
                    <td><strong>${headNameTotals[headNamePrev].variation.toFixed(2)}</strong></td>
                `;
            }
            // Update the previous head name
            headNamePrev = row.head_name;
        }

        // Add the current row
        const rowElement = supplementaryReportTableBody.insertRow();
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

    // Add the final head total
    if (headNamePrev !== '') {
        supplementaryReportTableBody.insertRow().innerHTML = `
            <td colspan="4"><strong>${headNamePrev} Total</strong></td>
            <td><strong>${headNameTotals[headNamePrev].sanctioned_budget.toFixed(2)}</strong></td>
            <td><strong>${headNameTotals[headNamePrev].revised_estimate.toFixed(2)}</strong></td>
            <td><strong>${headNameTotals[headNamePrev].excess.toFixed(2)}</strong></td>
            <td><strong>${headNameTotals[headNamePrev].surrender.toFixed(2)}</strong></td>
            <td><strong>${headNameTotals[headNamePrev].variation.toFixed(2)}</strong></td>
        `;
    }
}
