import json
import xlsxwriter
import os
import sys

def generate_excel_template(json_path, output_dir):
    
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        return

    
    with open(json_path, 'r') as f:
        grid_data = json.load(f)

    
    excel_path = os.path.join(output_dir, "template.xlsx")

    
    workbook = xlsxwriter.Workbook(excel_path)
    worksheet = workbook.add_worksheet("Warehouse Template")

    
    worksheet.write(0, 0, "Grid Location")  
    worksheet.write(0, 1, "Product Name")  
    worksheet.write(0, 2, "Quantity")      

    
    example_data = [
        {"grid": "A1", "product": "Widget A", "quantity": 50},
        {"grid": "A1", "product": "Widget B", "quantity": 30},
        {"grid": "B2", "product": "Gadget X", "quantity": 100},
        {"grid": "C3", "product": "Tool Y", "quantity": 20},
        {"grid": "C3", "product": "Tool Z", "quantity": 15},
    ]

    
    row = 1
    for example in example_data:
        worksheet.write(row, 0, example["grid"])
        worksheet.write(row, 1, example["product"])
        worksheet.write(row, 2, example["quantity"])
        row += 1

    
    for item in grid_data:
        worksheet.write(row, 0, item["label"])  
        worksheet.write(row, 1, "")            
        worksheet.write(row, 2, "")            
        row += 1

    workbook.close()
    print(f"Excel template saved to: {excel_path}")

if __name__ == "__main__":
    
    json_path = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generate_excel_template(json_path, output_dir)
