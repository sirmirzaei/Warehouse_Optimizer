import xlsxwriter
import os
import sys

def generate_order_template(output_dir):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    
    excel_path = os.path.join(output_dir, "order_template.xlsx")

    
    workbook = xlsxwriter.Workbook(excel_path)
    worksheet = workbook.add_worksheet("Order Template")

    
    columns = ["Product Name", "Customer Name", "Order Qty", "Order Date"]
    for col_num, column_name in enumerate(columns):
        worksheet.write(0, col_num, column_name)

    
    sample_data = [
        ["Widget A", "Customer 1", 10, "2025-01-15"],
        ["Widget B", "Customer 2", 5, "2025-01-16"],
        ["Widget C", "Customer 1", 20, "2025-01-17"],
        ["Widget A", "Customer 3", 8, "2025-01-18"],
        ["Widget B", "Customer 2", 15, "2025-01-19"],
    ]

    for row_num, row_data in enumerate(sample_data, start=1):
        for col_num, cell_data in enumerate(row_data):
            worksheet.write(row_num, col_num, cell_data)

    
    workbook.close()
    print(f"Order template saved to: {excel_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_customer_template.py <output_dir>")
        sys.exit(1)

    output_dir = sys.argv[1]
    generate_order_template(output_dir)
