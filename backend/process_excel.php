<?php
header('Content-Type: application/json');


if (!isset($_FILES['productExcel'])) {
    echo json_encode(["status" => "error", "message" => "No file uploaded."]);
    exit;
}

$uploadDir = __DIR__ . "/uploads/";
$outputDir = __DIR__ . "/output/";  


if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}
if (!is_dir($outputDir)) {
    mkdir($outputDir, 0777, true);
}


$fileName = basename($_FILES['productExcel']['name']);
$filePath = $uploadDir . $fileName;

if (!move_uploaded_file($_FILES['productExcel']['tmp_name'], $filePath)) {
    echo json_encode(["status" => "error", "message" => "Failed to upload file."]);
    exit;
}


$gridDataPath = $outputDir . "grid_data.json";  
$annotatedImagePath = $outputDir . "annotated_plan.png"; 
$updatedImagePath = $outputDir . "annotated_plan_updated.png"; 


$pythonPath = "python";  
$command = escapeshellcmd("$pythonPath process_excel.py \"$filePath\" \"$gridDataPath\" \"$annotatedImagePath\" \"$updatedImagePath\"");
$output = shell_exec($command . " 2>&1");

error_log("Python Script Output: " . $output);

$response = json_decode($output, true);

if ($response === null) {
    echo json_encode(["status" => "error", "message" => "Failed to process Excel file.", "debug" => $output]);
    exit;
}


$response["updated_image"] = "output/annotated_plan_updated.png";

echo json_encode($response);
?>
