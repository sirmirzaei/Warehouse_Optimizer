import sys
import pandas as pd
import json
import os
import cv2
import numpy as np
import networkx as nx
from scipy.cluster.hierarchy import linkage, fcluster

def log_message(message):
    with open("debug_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")

def analyze_orders(file_path, grid_data_path, annotated_image_path, updated_image_path):
    if not os.path.exists(file_path):
        print(json.dumps({"status": "error", "message": "Excel file not found."}))
        return

    if not os.path.exists(grid_data_path):
        print(json.dumps({"status": "error", "message": "Grid data file not found."}))
        return

    current_locations_path = "output/current_locations.csv"
    if not os.path.exists(current_locations_path):
        print(json.dumps({"status": "error", "message": "Current locations file not found."}))
        return

    # Load order data
    df = pd.read_excel(file_path)
    required_columns = ["Product Name", "Customer Name", "Order Qty", "Order Date"]
    if not all(col in df.columns for col in required_columns):
        print(json.dumps({"status": "error", "message": "Invalid Excel format."}))
        return

    # Load current locations of products
    current_locations = pd.read_csv(current_locations_path)

    # Ensure required columns exist in current locations
    if not all(col in current_locations.columns for col in ["Product Name", "Grid Location"]):
        print(json.dumps({"status": "error", "message": "Invalid format in current locations file."}))
        return

    # Load warehouse grid data
    with open(grid_data_path, "r") as f:
        grid_data = json.load(f)
    warehouse_data = pd.DataFrame(grid_data)

    # Calculate total orders per product
    product_order_totals = df.groupby("Product Name")["Order Qty"].sum().reset_index()
    product_order_totals.rename(columns={"Order Qty": "Total Ordered Qty"}, inplace=True)

    # Compute order probabilities
    merged_data = df.merge(product_order_totals, on="Product Name")
    merged_data["Order Probability"] = merged_data["Order Qty"] / merged_data["Total Ordered Qty"]

    # Create a demand matrix based on shared customers
    demand_matrix = merged_data.pivot_table(
        index="Product Name", columns="Customer Name", values="Order Probability", fill_value=0
    )

    # Calculate similarity based on shared customers
    similarity_matrix = demand_matrix.dot(demand_matrix.T)

    # Perform hierarchical clustering based on similarity
    linkage_matrix = linkage(similarity_matrix, method="ward")
    num_clusters = min(len(similarity_matrix) // 5, 5) or 3  # At least 3 clusters, max 5
    clusters = fcluster(linkage_matrix, t=num_clusters, criterion="maxclust")

    # Assign cluster labels dynamically
    product_clusters = pd.DataFrame({"Product Name": similarity_matrix.index, "Cluster": clusters})

    # Merge product clusters with current locations
    warehouse_with_clusters = current_locations.merge(product_clusters, on="Product Name", how="left")

    # Restrict grid locations to predefined spots in the current locations file
    predefined_locations = current_locations["Grid Location"].tolist()

    # Ensure valid new grid locations are assigned from the predefined list
    available_locations = predefined_locations.copy()
    new_grid_locations = []

    for _, row in warehouse_with_clusters.iterrows():
        if available_locations:
            new_location = available_locations.pop(0)  # Assign the next available predefined location
            new_grid_locations.append(new_location)
        else:
            new_grid_locations.append(None)  # If no available locations, leave as None

    warehouse_with_clusters["New Grid Location"] = new_grid_locations

    # Sort products by cluster and assign adjacency dynamically
    warehouse_with_clusters.sort_values(by=["Cluster", "Grid Location"], inplace=True)

    # Create relocation plan
    relocation_plan = warehouse_with_clusters[["Product Name", "Grid Location", "New Grid Location", "Cluster"]]
    log_message(f"Relocation Plan: {relocation_plan.to_json(orient='records', indent=2)}")

    # Load and annotate the image
    image = cv2.imread(annotated_image_path)
    if image is None:
        print(json.dumps({"status": "error", "message": "Could not load annotated image."}))
        return

    height, width, _ = image.shape

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5  
    font_thickness = 2  
    text_color = (0, 0, 255)  # Red color
    padding = 10  

    # Draw product locations
    for _, row in warehouse_with_clusters.iterrows():
        # Ensure the new location exists and is valid
        if row["New Grid Location"] in predefined_locations:
            location_data = warehouse_data.loc[warehouse_data["label"] == row["New Grid Location"], ["x", "y"]]

            if not location_data.empty:
                x, y = location_data.values[0]
            else:
                log_message(f"Skipped drawing product {row['Product Name']} - Invalid location {row['New Grid Location']}.")
                continue

            product = row["Product Name"]

            # Ensure text stays within image boundaries
            text_size, _ = cv2.getTextSize(product, font, font_scale, font_thickness)
            text_width, text_height = text_size

            text_x = max(padding, min(int(x), width - text_width - padding))
            text_y = max(text_height + padding, min(int(y), height - padding))

            cv2.putText(image, product, (text_x, text_y), font, font_scale, text_color, font_thickness)

    # Save the updated image
    success = cv2.imwrite(updated_image_path, image)
    if success:
        log_message(f"Updated image saved to {updated_image_path}")
    else:
        log_message("Failed to save the updated image.")

    # Save to Excel
    output_path = "output/optimized_layout.xlsx"
    with pd.ExcelWriter(output_path) as writer:
        relocation_plan.to_excel(writer, sheet_name="Relocation Plan", index=False)
    log_message(f"Results saved to {output_path}")

    print(
        json.dumps(
            {
                "status": "success",
                "message": "Analysis completed.",
                "recommended_layout": output_path,
                "updated_image": updated_image_path,
            }
        )
    )

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(json.dumps({"status": "error", "message": "Invalid arguments."}))
        sys.exit(1)

    file_path = sys.argv[1]
    grid_data_path = sys.argv[2]
    annotated_image_path = sys.argv[3]
    updated_image_path = sys.argv[4]

    analyze_orders(file_path, grid_data_path, annotated_image_path, updated_image_path)
