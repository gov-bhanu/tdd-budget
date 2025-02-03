function exportToExcel() {
    // Get all tables within the #typereport div
    const tables = document.querySelectorAll('#finalTypeTable table');
    
    if (tables.length === 0) {
        alert("No tables found for export.");
        return; // Exit the function if no tables are found
    }

    // Create a new workbook
    const wb = XLSX.utils.book_new();

    // Loop through each table and convert to sheet data
    tables.forEach((table, index) => {
        // Check if the table has any rows before proceeding
        if (table.rows.length > 0) {
            const sheet = XLSX.utils.table_to_sheet(table);
            const sheetName = table.id || `Sheet ${index + 1}`; // Use table's ID as sheet name
            XLSX.utils.book_append_sheet(wb, sheet, sheetName); // Add the sheet to the workbook
        } else {
            console.warn(`Table ${index + 1} is empty and will be skipped.`);
        }
    });

    // If the workbook contains sheets, export it
    if (wb.SheetNames.length > 0) {
        XLSX.writeFile(wb, 'type_summary.xlsx');
    } else {
        alert("No data found to export.");
    }
}
