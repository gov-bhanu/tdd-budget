let allData = []; // To store all fetched data

// Fetch all data and populate the main table and dropdown
function fetchData() {
    fetch('/fetch-data/')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                allData = data.data;
                allData.sort((a, b) => a.head_name.localeCompare(b.head_name)); // Sort by Head Name
                populateMainTable();
                populateHeadNameDropdown();
            } else {
                alert('Error fetching data: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error fetching data. Please check the console for details.');
        });
}

// Populate the main data table
function populateMainTable() {
    const dataTable = document.getElementById('dataTable').getElementsByTagName('tbody')[0];
    dataTable.innerHTML = ''; // Clear previous table content
    allData.sort((a, b) => (a.head_name || '').localeCompare(b.head_name || '') || (a.soe_name || '').localeCompare(b.soe_name || ''));
    allData.forEach(row => {
        const newRow = dataTable.insertRow();
        newRow.innerHTML = `
            <td>${row.department_name}</td>
            <td>${row.head_name}</td>
            <td>${row.scheme_name}</td>
            <td>${row.soe_name}</td>
            <td>${parseFloat(row.sanctioned_budget).toFixed(2)}</td>
            <td>${parseFloat(row.revised_estimate).toFixed(2)}</td>
            <td>${parseFloat(row.in_divisible).toFixed(2)}</td>
            <td>${(row.divisible || 0).toFixed(2)}</td>
            <td>${(row.kinnaur || 0).toFixed(2)}</td>
            <td>${(row.lahaul || 0).toFixed(2)}</td>
            <td>${(row.spiti || 0).toFixed(2)}</td>
            <td>${(row.pangi || 0).toFixed(2)}</td>
            <td>${(row.bharmaur || 0).toFixed(2)}</td>
        `;
    });
}




// Populate the Head Name datalist for suggestions
function populateHeadNameDropdown() {
    const headNameInput = document.getElementById('headNameInput');
    const datalist = document.getElementById('headNameSuggestions');
    const uniqueHeadNames = [...new Set(allData.map(row => row.head_name))];
    uniqueHeadNames.sort(); // Sort the head names in ascending order

    // Clear existing suggestions
    datalist.innerHTML = '';

    uniqueHeadNames.forEach(headName => {
        const option = document.createElement('option');
        option.value = headName;
        datalist.appendChild(option);
    });
}

// Handle Head Name selection from the input field with suggestions
function onHeadNameSelected() {
    const selectedHeadName = document.getElementById('headNameInput').value.trim();
    if (!selectedHeadName) {
        document.getElementById('soeDetails').style.display = 'none';
        return;
    }
    const filteredData = allData.filter(row => row.head_name === selectedHeadName);
    populateSOETable(filteredData);
    document.getElementById('soeDetails').style.display = 'block';
}

// Populate the SOE table for updating revised estimate
function populateSOETable(filteredData) {
    // Sort the filtered data by soe_name in ascending order
    filteredData.sort((a, b) => a.soe_name.localeCompare(b.soe_name));

    const soeTable = document.getElementById('soeTable').getElementsByTagName('tbody')[0];
    soeTable.innerHTML = '';  // Clear existing rows

    filteredData.forEach((row, index) => {
        // Generate uniqueSearch based on the updated model logic
        const uniqueSearch = `${row.department_name}-${row.scheme_name}-${row.head_name}-${row.soe_name}`;

        const in_divisible = (row.in_divisible || 0).toFixed(2);
        const kinnaur = (row.kinnaur || 0).toFixed(2);
        const lahaul = (row.lahaul || 0).toFixed(2);
        const spiti = (row.spiti || 0).toFixed(2);
        const pangi = (row.pangi || 0).toFixed(2);
        const bharmaur = (row.bharmaur || 0).toFixed(2);

        // Sum up the values for revisedEstimate
        const divisible = (parseFloat(kinnaur) + parseFloat(lahaul) + parseFloat(spiti) + parseFloat(pangi) + parseFloat(bharmaur)).toFixed(2);
        const revisedEstimate = (parseFloat(in_divisible) + parseFloat(divisible)).toFixed(2);
        
        // Add a row with input fields for editing
        const newRow = soeTable.insertRow();
        // Store the uniqueSearch as a data attribute for later retrieval
        newRow.setAttribute('data-unique-search', uniqueSearch);

        newRow.innerHTML = `
            <td>${row.department_name}</td>
            <td>${row.scheme_name}</td>
            <td>${row.soe_name}</td>
            <td>${parseFloat(row.sanctioned_budget).toFixed(2)}</td>
            <td><strong>${revisedEstimate}</strong></td>
            <td><input type="number" value="${in_divisible}" class="expandable-input" /></td>
            <td>${divisible}</td>
            <td><input type="number" value="${kinnaur}" class="expandable-input" /></td>
            <td><input type="number" value="${lahaul}" class="expandable-input" /></td>
            <td><input type="number" value="${spiti}" class="expandable-input" /></td>
            <td><input type="number" value="${pangi}" class="expandable-input" /></td>
            <td><input type="number" value="${bharmaur}" class="expandable-input" /></td>
            <td>
                <button class="btn btn-success" onclick="updateRevisedEstimate('${uniqueSearch}', this)">Update</button>
            </td>
        `;
    });
}

// Update Revised Estimate for a single SOE
function updateRevisedEstimate(uniqueSearch, button) {
    const row = button.parentElement.parentElement; // Get the row that contains the data

    // Updated cell indices after adding the department column:
    // 0: Department, 1: Scheme, 2: SOE, 3: Sanctioned Budget, 4: Revised Estimate,
    // 5: In Divisible, 6: Divisible, 7: Kinnaur, 8: Lahaul, 9: Spiti, 10: Pangi, 11: Bharmaur, 12: Action
    const in_divisible = parseFloat(row.cells[5].querySelector('input').value) || 0;
    const kinnaur = parseFloat(row.cells[7].querySelector('input').value) || 0;
    const lahaul = parseFloat(row.cells[8].querySelector('input').value) || 0;
    const spiti = parseFloat(row.cells[9].querySelector('input').value) || 0;
    const pangi = parseFloat(row.cells[10].querySelector('input').value) || 0;
    const bharmaur = parseFloat(row.cells[11].querySelector('input').value) || 0;

    // Calculate totals
    const divisible = kinnaur + lahaul + spiti + pangi + bharmaur;
    const revisedEstimate = in_divisible + divisible;

    // Preserve the currently selected Head Name
    const headNameInput = document.getElementById('headNameInput');
    const selectedHeadName = headNameInput.value.trim();

    // Make the API call to update the revised estimate in the backend
    fetch('/update-revised-estimate/', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json', 
            'X-CSRFToken': getCookie('csrftoken') 
        },
        body: JSON.stringify({
            uniqueSearch,  // Send the unique search key
            revisedEstimate,  // Send the updated revised estimate value
            in_divisible,
            divisible,
            kinnaur,
            lahaul,
            spiti,
            pangi,
            bharmaur
        })
    })
    .then(response => response.json())
    .then(data => {
        const inlineMessage = document.getElementById('inlineMessage');
        inlineMessage.style.display = 'block';
        if (data.status === 'success') {
            inlineMessage.textContent = `Updated ${uniqueSearch} successfully!`;
            inlineMessage.style.color = 'green';

            // Update the Revised Estimate cell in the SOE Details table (cell index 4)
            row.cells[4].textContent = revisedEstimate.toFixed(2);
            // Update the Divisible cell in the SOE Details table (cell index 6)
            row.cells[6].textContent = divisible.toFixed(2);

            // Refresh main table data
            fetchData();
            // Delay reapplying the filter to ensure fetchData has finished
            setTimeout(() => {
                headNameInput.value = selectedHeadName;
                onHeadNameSelected();
            }, 500);
        } else {
            inlineMessage.textContent = 'Error updating: ' + data.message;
            inlineMessage.style.color = 'red';
        }
    })
    .catch(error => {
        const inlineMessage = document.getElementById('inlineMessage');
        inlineMessage.style.display = 'block';
        inlineMessage.textContent = 'Error updating the estimate. Please try again later.';
        inlineMessage.style.color = 'red';
    });
}

// Make updateRevisedEstimate globally accessible for inline event attributes
window.updateRevisedEstimate = updateRevisedEstimate;

// CSRF Token Helper (unchanged)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Load data automatically when the page is loaded
window.onload = function() {
    fetchData();
};






document.addEventListener('DOMContentLoaded', () => {
    // Your other function definitions and initializations, e.g., fetchData(), populateSOETable(), etc.

    // Event delegation for the Enter key on input fields in the SOE table
    document.getElementById('soeTable').addEventListener('keydown', function(e) {
        if (e.target && e.target.matches('input.expandable-input') && e.key === "Enter") {
            const row = e.target.closest('tr');
            const updateButton = row.querySelector("button");
            if (updateButton) {
                updateButton.click();
            }
        }
    });
});




// Export table data to CSV
function exportToCSV() {
    const table = document.getElementById('dataTable');
    const rows = table.getElementsByTagName('tr');
    const csv = [];
    
    // Get table header
    const headers = [];
    const headerCells = rows[0].getElementsByTagName('th');
    for (let i = 0; i < headerCells.length; i++) {
        headers.push(headerCells[i].textContent);
    }
    csv.push(headers.join(','));

    // Get table rows
    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.getElementsByTagName('td');
        const rowData = [];
        for (let j = 0; j < cells.length; j++) {
            rowData.push(cells[j].textContent);
        }
        csv.push(rowData.join(','));
    }

    // Create a CSV file and download it
    const csvString = csv.join('\n');
    const blob = new Blob([csvString], { type: 'text/csv' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'data.csv';
    link.click();
}


function exportToExcel() {
    const table = document.getElementById('dataTable');
    const rows = table.getElementsByTagName('tr');

    // Prepare data for the Excel file
    const data = [];
    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        const rowData = [];
        for (let j = 0; j < cells.length; j++) {
            rowData.push(cells[j].textContent.trim());
        }
        data.push(rowData);
    }

    // Create a workbook and add the data
    const ws = XLSX.utils.aoa_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');

    // Generate Excel file and trigger download
    XLSX.writeFile(wb, 'data.xlsx');
}
