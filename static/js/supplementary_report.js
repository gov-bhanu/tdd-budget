document.addEventListener("DOMContentLoaded", function() {
    fetchSupplementaryData(); // Fetch data when the page loads
});

// Fetch data from the API
function fetchSupplementaryData() {
    fetch('/fetch-supplementary-data/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                populateSupplementaryReportTable(data.data, data.department_totals, data.head_name_totals);
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
function populateSupplementaryReportTable(data, departmentTotals, headNameTotals) {
    const supplementaryReportTableBody = document.getElementById('supplementaryReportTable').getElementsByTagName('tbody')[0];
    supplementaryReportTableBody.innerHTML = '';  // Clear previous table content

    let departmentNamePrev = '';  // Track previous department name for grouping
    let headNamePrev = '';  // Track previous head name for grouping

    // Loop through the data and populate the table
    data.forEach((row, index) => {
        // Add department total row when department changes
        // if (row.department_name !== departmentNamePrev) {
        //     if (departmentNamePrev !== '') {
        //         supplementaryReportTableBody.insertRow().innerHTML = `
        //             <td colspan="4"><strong>${departmentNamePrev} Total</strong></td>
        //             <td><strong>${departmentTotals[departmentNamePrev].sanctioned_budget.toFixed(2)}</strong></td>
        //             <td><strong>${departmentTotals[departmentNamePrev].revised_estimate.toFixed(2)}</strong></td>
        //             <td><strong>${departmentTotals[departmentNamePrev].excess.toFixed(2)}</strong></td>
        //             <td><strong>${departmentTotals[departmentNamePrev].surrender.toFixed(2)}</strong></td>
        //             <td><strong>${departmentTotals[departmentNamePrev].variation.toFixed(2)}</strong></td>
        //         `;
        //     }
        //     // Add the new department row
        //     departmentNamePrev = row.department_name;
        // }

        // Add head total row when head changes
        // if (row.head_name !== headNamePrev) {
        //     if (headNamePrev !== '') {
        //         supplementaryReportTableBody.insertRow().innerHTML = `
        //             <td colspan="4"><strong>${headNamePrev} Total</strong></td>
        //             <td><strong>${headNameTotals[headNamePrev].sanctioned_budget.toFixed(2)}</strong></td>
        //             <td><strong>${headNameTotals[headNamePrev].revised_estimate.toFixed(2)}</strong></td>
        //             <td><strong>${headNameTotals[headNamePrev].excess.toFixed(2)}</strong></td>
        //             <td><strong>${headNameTotals[headNamePrev].surrender.toFixed(2)}</strong></td>
        //             <td><strong>${headNameTotals[headNamePrev].variation.toFixed(2)}</strong></td>
        //         `;
        //     }
        //     // Add the new head row
        //     headNamePrev = row.head_name;
        // }

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

    // Add final department total
    supplementaryReportTableBody.insertRow().innerHTML = `
        <td colspan="4"><strong>${departmentNamePrev} Total</strong></td>
        <td><strong>${departmentTotals[departmentNamePrev].sanctioned_budget.toFixed(2)}</strong></td>
        <td><strong>${departmentTotals[departmentNamePrev].revised_estimate.toFixed(2)}</strong></td>
        <td><strong>${departmentTotals[departmentNamePrev].excess.toFixed(2)}</strong></td>
        <td><strong>${departmentTotals[departmentNamePrev].surrender.toFixed(2)}</strong></td>
        <td><strong>${departmentTotals[departmentNamePrev].variation.toFixed(2)}</strong></td>
    `;
}
