<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $uploadDir = "uploads/";
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0777, true);
    }

    if (!isset($_FILES["warehouseMap"]) || empty($_POST["scale"])) {
        echo json_encode(["status" => "error", "message" => "File and scale are required."]);
        exit;
    }

    $file = $_FILES["warehouseMap"];
    $scale = floatval($_POST["scale"]);
    $filePath = $uploadDir . basename($file["name"]);

    if (!move_uploaded_file($file["tmp_name"], $filePath)) {
        echo json_encode(["status" => "error", "message" => "Failed to upload file."]);
        exit;
    }

    $outputDir = "output/";
    if (!is_dir($outputDir)) {
        mkdir($outputDir, 0777, true);
    }

    // Set the correct URL path for outputs
    $baseUrl = "http://" . $_SERVER['HTTP_HOST'] . "/warehouse-optimizer/backend/output/";

    // Run Python to generate grid network
    $pythonPath = "python";
    $gridCommand = escapeshellcmd("$pythonPath grid_generator.py " . escapeshellarg($filePath) . " " . escapeshellarg($scale) . " " . escapeshellarg($outputDir) . " 2>&1");
    exec($gridCommand, $gridOutput, $gridReturn);

    if ($gridReturn !== 0) {
        echo json_encode(["status" => "error", "message" => "Grid generation failed. Debug log updated."]);
        exit;
    }

    $gridDataPath = $outputDir . "grid_data.json";
    $annotatedImagePath = $outputDir . "annotated_plan.png";

    if (!file_exists($gridDataPath) || !file_exists($annotatedImagePath)) {
        echo json_encode(["status" => "error", "message" => "Grid files not generated properly."]);
        exit;
    }

   // Run Python to generate Excel template
    $excelCommand = escapeshellcmd("$pythonPath generate_excel_template.py " . escapeshellarg($gridDataPath) . " " . escapeshellarg($outputDir) . " 2>&1");
    exec($excelCommand, $excelOutput, $excelReturn);

    $templateExcelPath = $outputDir . "template.xlsx";
    if (!file_exists($templateExcelPath)) {
        echo json_encode(["status" => "error", "message" => "Excel template generation failed."]);
        exit;
    }

    // Process the filled Excel file uploaded by the user
    if (isset($_FILES["productExcel"])) {
        $excelFile = $_FILES["productExcel"];
        $excelPath = $outputDir . basename($excelFile["name"]);
    
        if (!move_uploaded_file($excelFile["tmp_name"], $excelPath)) {
            echo json_encode(["status" => "error", "message" => "Failed to upload Excel file."]);
            exit;
        }
    
        $processCommand = escapeshellcmd("$pythonPath process_excel.py " . escapeshellarg($excelPath) . " " . escapeshellarg($gridDataPath) . " " . escapeshellarg($annotatedImagePath) . " 2>&1");
        exec($processCommand, $processOutput, $processReturn);
    
        if ($processReturn !== 0) {
            echo json_encode(["status" => "error", "message" => "Excel processing failed."]);
            exit;
        }
    
        $processResult = json_decode(implode("\n", $processOutput), true);
        if (!$processResult || $processResult["status"] !== "success") {
            echo json_encode(["status" => "error", "message" => "Error processing Excel."]);
            exit;
        }
    
        echo json_encode([
            "status" => "success",
            "message" => $processResult["message"],
            "updated_image" => $processResult["updated_image"]
        ]);
        exit;
    }

    echo json_encode([
        "status" => "success",
        "message" => "Warehouse map processed successfully.",
        "annotated_plan" => $baseUrl . "annotated_plan.png",
        "grid_data" => $baseUrl . "grid_data.json",
        "template_excel" => $baseUrl . "template.xlsx"
    ]);
    exit;
}
?>