import pandas as pd
import cv2
import json
import sys
import os

def process_excel(excel_path, grid_data_path, annotated_image_path, updated_image_path):
    if not os.path.exists(grid_data_path):
        print(json.dumps({"status": "error", "message": "Grid data file not found."}))
        return
    
    if not os.path.exists(annotated_image_path):
        print(json.dumps({"status": "error", "message": "Annotated image not found."}))
        return
    
    with open(grid_data_path, "r") as f:
        grid_data = json.load(f)
    
    df = pd.read_excel(excel_path)
    
    required_columns = ["Grid Location", "Product Name", "Quantity"]
    if not all(col in df.columns for col in required_columns):
        print(json.dumps({"status": "error", "message": "Excel file format is incorrect."}))
        return
    
    incomplete_rows = df[df.isnull().any(axis=1)]
    incomplete_count = len(incomplete_rows)
    complete_count = len(df) - incomplete_count
    
    product_map = {}
    product_list = []
    
    for _, row in df.dropna().iterrows():
        grid = row["Grid Location"]
        product = row["Product Name"]
        quantity = int(row["Quantity"])
        
        if quantity > 0:
            product_list.append({
                "Grid Location": grid,
                "Product Name": product,
                "Quantity": quantity
            })
        
        if grid in product_map:
            product_map[grid].append(f"{product} ({quantity})")
        else:
            product_map[grid] = [f"{product} ({quantity})"]
    
    # Save the filtered data to CSV in the same directory as updated_image_path
    output_csv_path = os.path.join(os.path.dirname(updated_image_path), "current_locations.csv")
    product_df = pd.DataFrame(product_list)
    product_df.to_csv(output_csv_path, index=False)
    
    image = cv2.imread(annotated_image_path)
    if image is None:
        print(json.dumps({"status": "error", "message": "Could not load annotated image."}))
        return
    
    height, width, _ = image.shape
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5  
    font_thickness = 2  
    text_color = (0, 0, 255)  
    padding = 10  
    
    for item in grid_data:
        grid_label = item["label"]
        if grid_label in product_map:
            x, y = item["x"], item["y"]
            products_text = ", ".join(product_map[grid_label])  
            
            text_size, _ = cv2.getTextSize(products_text, font, font_scale, font_thickness)
            text_width, text_height = text_size
            
            text_x = max(padding, min(x, width - text_width - padding))
            text_y = max(text_height + padding, min(y, height - padding))
            
            cv2.putText(image, products_text, (text_x, text_y), font, font_scale, text_color, font_thickness)
    
    cv2.imwrite(updated_image_path, image)
    
    print(json.dumps({
        "status": "success",
        "message": f"{complete_count} complete rows, {incomplete_count} incomplete rows found.",
        "complete_rows": complete_count,
        "incomplete_rows": incomplete_count,
        "updated_image": updated_image_path,
        "output_csv": output_csv_path
    }))

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(json.dumps({"status": "error", "message": "Invalid arguments."}))
        sys.exit(1)

    excel_path = sys.argv[1]
    grid_data_path = sys.argv[2]
    annotated_image_path = sys.argv[3]
    updated_image_path = sys.argv[4]

    process_excel(excel_path, grid_data_path, annotated_image_path, updated_image_path)
