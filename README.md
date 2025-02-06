# Warehouse Optimizer

## Overview
Warehouse Optimizer is a web-based tool designed to streamline warehouse operations by optimizing product placements based on customer orders. It enables warehouse managers to upload warehouse maps, manage product storage, and analyze order data to enhance efficiency.

## Features
- Upload warehouse maps (PDF/JPG) and define scales.
- Generate and upload warehouse layout templates in Excel.
- Upload customer order files and optimize storage layouts.
- Analyze order trends and recommend optimized product placements.
- Visualize annotated warehouse maps with product placements.

## Installation
### Prerequisites
- [XAMPP](https://www.apachefriends.org/download.html) or any local server supporting PHP and MySQL.
- Python 3.x with required libraries:
  ```bash
  pip install pandas numpy networkx xlsxwriter opencv-python flask scipy openpyxl
  ```

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/sirmirzaei/Warehouse_Optimizer.git
   cd Warehouse_Optimizer
   ```
2. Move the project files to the `htdocs` directory if using XAMPP.
3. Start Apache and MySQL from XAMPP.
4. Ensure Python scripts are executable.
5. Open `index.html` in a browser.

## Usage
### Step 1: Upload Warehouse Map
1. Open the application in your browser.
2. Click on **Step 1: Upload Warehouse Map**.
3. Choose a warehouse map file (PNG, JPG, PDF).
4. Enter the scale (e.g., `1mm = 1 meter`).
5. Click **Submit** to generate a grid layout.
6. Download the annotated warehouse layout if needed.

### Step 2: Upload Product List
1. Download the warehouse template from the application.
2. Fill in the product names, grid locations, and quantities.
3. Upload the completed Excel file.
4. The system processes the file and updates the warehouse layout.

### Step 3: Upload Customer Orders
1. Download the customer order template.
2. Fill in the required fields: product name, customer name, order quantity, and date.
3. Upload the completed customer order file.
4. The system analyzes orders and generates an optimized warehouse layout.

### Step 4: Download Optimized Layout
1. Once analysis is complete, view the recommended product placements.
2. Download the updated warehouse layout in Excel format.
3. The application also provides an annotated image of the optimized layout.

## File Structure
```
warehouse-optimizer/
├── backend/
│   ├── upload.php (Handles file uploads)
│   ├── process_excel.php (Processes Excel files)
│   ├── analyze_orders.php (Analyzes customer orders)
│   ├── generate_excel_template.py (Generates warehouse templates)
│   ├── generate_customer_template.py (Generates customer order templates)
│   ├── grid_generator.py (Generates warehouse grid layout)
├── styles.css (UI styles)
├── script.js (Handles frontend interactivity)
├── index.html (Main UI page)
└── README.md (Project documentation)
```

## Troubleshooting
- Ensure uploaded files match the expected format.
- If an error occurs, check the **console log** for details.
- Ensure Python scripts have the necessary permissions to execute.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch (`feature-name`).
3. Commit changes and push to the branch.
4. Create a pull request.

## Contact
For questions, open an issue on the [GitHub repository](https://github.com/sirmirzaei/Warehouse_Optimizer) or contact me via [LinkedIn](https://www.linkedin.com/in/mehranmirzaei/).

