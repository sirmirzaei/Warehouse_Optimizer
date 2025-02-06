<?php
header("Content-Type: application/json");

// Define paths
$file_path = "uploads/customer_orders.xlsx";  // Ensure this file exists
$grid_data_path = "output/grid_data.json";
$annotated_image_path = "output/annotated_plan.png";
$updated_image_path = "output/updated_plan.png";

// Debugging logs (check Apache error log)
error_log("Starting Analysis...");
error_log("File Path: " . $file_path);
error_log("Grid Data Path: " . $grid_data_path);
error_log("Annotated Image Path: " . $annotated_image_path);
error_log("Updated Image Path: " . $updated_image_path);

// Check if the uploaded file exists before running the script
if (!file_exists($file_path)) {
    error_log("ERROR: Customer order file missing!");
    echo json_encode(["status" => "error", "message" => "Customer order file not found."]);
    exit;
}

// Run Python script
$command = "python analyze_orders.py " . escapeshellarg($file_path) . " " . escapeshellarg($grid_data_path) . " " . escapeshellarg($annotated_image_path) . " " . escapeshellarg($updated_image_path);
error_log("Executing: " . $command);

$output = shell_exec($command);
error_log("Python Output: " . $output);

// Check if Python script returned data
if (!$output) {
    error_log("ERROR: Python script failed to return data!");
    echo json_encode(["status" => "error", "message" => "Analysis failed.", "output" => null]);
    exit;
}

// Return Python output
echo $output;
?>
