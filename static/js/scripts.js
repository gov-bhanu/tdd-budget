
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



// Populate the Head Name dropdown
function populateHeadNameDropdown() {
    const headNameDropdown = document.getElementById('headNameDropdown');
    const uniqueHeadNames = [...new Set(allData.map(row => row.head_name))];
    uniqueHeadNames.sort(); // Sort the head names in ascending order
    headNameDropdown.innerHTML = '<option value="">--Select Head Name--</option>';
    uniqueHeadNames.forEach(headName => {
        const option = document.createElement('option');
        option.value = headName;
        option.textContent = headName;
        headNameDropdown.appendChild(option);
    });
}

// Handle Head Name selection
function onHeadNameSelected() {
    const selectedHeadName = document.getElementById('headNameDropdown').value;
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
    const soeTable = document.getElementById('soeTable').getElementsByTagName('tbody')[0];
    soeTable.innerHTML = '';  // Clear existing rows

    filteredData.forEach((row, index) => {
        // Generate uniqueSearch based on the updated model logic
        // const uniqueSearch = `${row.department_code}-${row.department_name}-${row.scheme_name}-${row.head_name}-${row.soe_name}`;
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
        newRow.innerHTML = `
        <td>${row.scheme_name}</td>
        <td>${row.soe_name}</td>
        <td>${parseFloat(row.sanctioned_budget).toFixed(2)}</td>
        <td>${revisedEstimate}</td>
        <td><input type="number" value="${in_divisible}" class="expandable-input" /></td>
        <td>${divisible}</td>
        <td><input type="number" value="${kinnaur}" class="expandable-input" /></td>
        <td><input type="number" value="${lahaul}" class="expandable-input" /></td>
        <td><input type="number" value="${spiti}" class="expandable-input" /></td>
        <td><input type="number" value="${pangi}" class="expandable-input" /></td>
        <td><input type="number" value="${bharmaur}" class="expandable-input" /></td>
        <td>
            <button onclick="updateRevisedEstimate('${uniqueSearch}', this)">Update</button>
        </td>
    `;
    });
}



// Update Revised Estimate for a single SOE
function updateRevisedEstimate(uniqueSearch, button) {
    const row = button.parentElement.parentElement; // Get the row that contains the data
    const in_divisible = parseFloat(row.cells[4].querySelector('input').value) || 0;
    const kinnaur = parseFloat(row.cells[6].querySelector('input').value) || 0;
    const lahaul = parseFloat(row.cells[7].querySelector('input').value) || 0;
    const spiti = parseFloat(row.cells[8].querySelector('input').value) || 0;
    const pangi = parseFloat(row.cells[9].querySelector('input').value) || 0;
    const bharmaur = parseFloat(row.cells[10].querySelector('input').value) || 0;

    // Calculate
    const divisible = kinnaur + lahaul + spiti + pangi + bharmaur
    const revisedEstimate = in_divisible + divisible

    // Make the API call to update the revised estimate in the backend
    fetch('/update-revised-estimate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
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
            inlineMessage.style.color = 'green'; // Success message style

            // Update the Revised Estimate cell in the SOE Details table
            row.cells[3].textContent = revisedEstimate.toFixed(2);

            // Update the Divisible cell in the SOE Details table
            row.cells[5].textContent = divisible.toFixed(2);


            fetchData();
        } else {
            inlineMessage.textContent = 'Error updating: ' + data.message;
            inlineMessage.style.color = 'red'; // Error message style
        }
    })
    .catch(error => {
        const inlineMessage = document.getElementById('inlineMessage');
        inlineMessage.style.display = 'block';
        inlineMessage.textContent = 'Error updating the estimate. Please try again later.';
        inlineMessage.style.color = 'red'; // Error message style
    });
}


// CSRF Token Helper
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
