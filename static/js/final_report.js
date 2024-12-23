// Function to export tables to Excel with tab names based on table IDs
function exportToExcel() {
    // Get all tables within the finalReportTable div
    const tables = document.querySelectorAll('#finalReportTable table');
    
    // Create a new workbook
    const wb = XLSX.utils.book_new();
    
    // Loop through each table and convert to sheet data
    tables.forEach((table) => {
        const sheet = XLSX.utils.table_to_sheet(table);
        const sheetName = table.id || `Sheet ${table.index + 1}`; // Use table's ID as sheet name
        XLSX.utils.book_append_sheet(wb, sheet, sheetName); // Add the sheet to the workbook
    });

    // Download the workbook as an Excel file
    XLSX.writeFile(wb, 'final_report.xlsx');
}
