<?php
header("Content-Type: application/json");

// Ensure the uploads directory exists
$upload_dir = "uploads/";
if (!file_exists($upload_dir)) {
    mkdir($upload_dir, 0777, true);
}

// Check if a file was uploaded
if (!isset($_FILES['customerOrderFile'])) {
    echo json_encode(["status" => "error", "message" => "No file uploaded."]);
    exit;
}

// Get file details and rename it
$file = $_FILES['customerOrderFile'];
$file_extension = pathinfo($file['name'], PATHINFO_EXTENSION);
$new_filename = $upload_dir . "customer_orders." . $file_extension;

// Move the uploaded file
if (!move_uploaded_file($file['tmp_name'], $new_filename)) {
    echo json_encode(["status" => "error", "message" => "Failed to save uploaded file."]);
    exit;
}

// Define paths for processing
$grid_data_path = "output/grid_data.json";
$annotated_image_path = "output/annotated_plan.png";
$updated_image_path = "output/updated_plan.png";

// Log for debugging
error_log("Processing file: " . $new_filename);
error_log("Grid Data Path: " . $grid_data_path);
error_log("Annotated Image Path: " . $annotated_image_path);
error_log("Updated Image Path: " . $updated_image_path);


// Execute Python script
$command = "python analyze_orders.py " . escapeshellarg($new_filename) . " " . escapeshellarg($grid_data_path) . " " . escapeshellarg($annotated_image_path) . " " . escapeshellarg($updated_image_path);
error_log("Executing command: " . $command);  // Log command

$output = shell_exec($command . " 2>&1");  // Capture errors too
error_log("Python Output: " . $output);    // Log output

if (!$output) {
    error_log("ERROR: Python script failed or returned empty response.");
    echo json_encode(["status" => "error", "message" => "Analysis failed. No output received."]);
    exit;
}

echo $output;

?>
