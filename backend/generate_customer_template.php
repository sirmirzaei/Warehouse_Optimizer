<?php
header('Content-Type: application/json');

$outputDir = __DIR__ . "/output/";

$pythonPath = "python";
$command = escapeshellcmd("$pythonPath generate_customer_template.py \"$outputDir\"");
$output = shell_exec($command . " 2>&1");

if (strpos($output, "Order template saved to") !== false) {
    $templatePath = "output/order_template.xlsx";
    echo json_encode([
        "status" => "success",
        "message" => "Order template generated successfully.",
        "template_url" => $templatePath
    ]);
} else {
    echo json_encode([
        "status" => "error",
        "message" => "Failed to generate order template.",
        "debug" => $output
    ]);
}
?>
