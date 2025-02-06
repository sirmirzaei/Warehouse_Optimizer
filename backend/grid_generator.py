import cv2
import numpy as np
import json
import sys
import os

def generate_grid(image_path, scale, output_dir):
    
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return

    height, width, _ = image.shape
    print(f"Image dimensions: {width}x{height}")

    
    scale_pixels_per_meter = 100 / scale

    
    points_x = int(width / scale_pixels_per_meter) + 1
    points_y = int(height / scale_pixels_per_meter) + 1

    x_coords = np.linspace(0, width, points_x, endpoint=True, dtype=int)
    y_coords = np.linspace(0, height, points_y, endpoint=True, dtype=int)

    
    annotated_image = image.copy()
    grid_data = []

    for j, y in enumerate(y_coords):
        for i, x in enumerate(x_coords):
            
            cv2.circle(annotated_image, (x, y), radius=3, color=(0, 255, 0), thickness=-1)

            
            label = f"{chr(65 + j)}{i}"
            grid_data.append({"label": label, "x": int(x), "y": int(y)})

            
            text_x = min(x + 5, width - 30)
            text_y = max(y - 5, 10)
            cv2.putText(annotated_image, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)

    
    annotated_path = os.path.join(output_dir, "annotated_plan.png")
    json_path = os.path.join(output_dir, "grid_data.json")
    cv2.imwrite(annotated_path, annotated_image)
    with open(json_path, "w") as f:
        json.dump(grid_data, f, indent=4)

    print(f"Annotated plan saved to: {annotated_path}")
    print(f"Grid data saved to: {json_path}")

if __name__ == "__main__":
    
    image_path = sys.argv[1]
    scale = float(sys.argv[2])
    output_dir = sys.argv[3]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generate_grid(image_path, scale, output_dir)
