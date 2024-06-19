# Define the path to the original CSV file
$originalCsvPath = "dataset.csv"

# Define the path for the new CSV file with filtered data
$newCsvPath = "indian-food.csv"

# Import the original CSV file
$data = Import-Csv $originalCsvPath

# Filter the data to keep rows where "Keywords" contains "Indian"
$filteredData = $data | Where-Object { $_.Keywords -like "*Indian*" }

# Export the filtered data to a new CSV file
$filteredData | Export-Csv -Path $newCsvPath -NoTypeInformation

Write-Host "Filtered data with 'Indian' in Keywords column has been saved to $newCsvPath."
