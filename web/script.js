Papa.parse("../data.csv", {
    download: true,
    header: true, // Set to true if your CSV has a header row
    skipEmptyLines: true,
    complete: function(results) {
        // Data is now in results.data
        $('#csvTable').DataTable({
            data: results.data,
            columns: Object.keys(results.data[0]).map(key => ({
                title: key,
                data: key
            }))
        });
    }
});
