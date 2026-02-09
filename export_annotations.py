#!/usr/bin/env python3
"""
Export annotations to various formats (COCO, YOLO, CSV, etc.)
"""

import json
import csv
from pathlib import Path
from datetime import datetime

def load_annotations(annotations_folder='./annotations'):
    """Load all annotations from the annotations folder"""
    annotations = []
    folder = Path(annotations_folder)
    
    for file in folder.glob('*.json'):
        with open(file, 'r') as f:
            annotations.append(json.load(f))
    
    return annotations

def export_to_csv(annotations, output_file='annotations.csv'):
    """Export annotations to CSV format"""
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header with new 6-point system
        writer.writerow([
            'image_name', 'annotator_name', 'timestamp',
            'nose_tip_x', 'nose_tip_y', 'nose_tip_visible',
            'left_wing_tip_x', 'left_wing_tip_y', 'left_wing_tip_visible',
            'right_wing_tip_x', 'right_wing_tip_y', 'right_wing_tip_visible',
            'fuselage_tail_x', 'fuselage_tail_y', 'fuselage_tail_visible',
            'wing_root_x', 'wing_root_y', 'wing_root_visible',
            'vertical_stabilizer_x', 'vertical_stabilizer_y', 'vertical_stabilizer_visible'
        ])
        
        # Data
        for ann in annotations:
            points = ann['points']
            row = [
                ann['image_name'],
                ann['annotator_name'],
                ann['timestamp'],
            ]
            
            # Add all points (handle variable length for backward compatibility)
            for i in range(6):
                if i < len(points):
                    row.extend([
                        points[i]['x'], 
                        points[i]['y'], 
                        points[i].get('visible', True)
                    ])
                else:
                    # Fill with empty values for missing points
                    row.extend(['', '', ''])
            
            writer.writerow(row)
    
    print(f"✓ Exported to CSV: {output_file}")

def export_to_coco(annotations, images_folder='./images', output_file='coco_annotations.json'):
    """Export annotations to COCO keypoint format"""
    
    coco_format = {
        "info": {
            "description": "UAV Pose Dataset",
            "version": "1.0",
            "year": datetime.now().year,
            "date_created": datetime.now().isoformat()
        },
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": [
            {
                "id": 1,
                "name": "uav",
                "supercategory": "vehicle",
                "keypoints": ["nose_tip", "left_wing_tip", "right_wing_tip", "fuselage_tail", "wing_root", "vertical_stabilizer"],
                "skeleton": [[0, 3], [1, 2]]  # nose to tail, left wing to right wing
            }
        ]
    }
    
    images_folder = Path(images_folder)
    
    for idx, ann in enumerate(annotations):
        image_path = images_folder / ann['image_name']
        
        # Get image dimensions (you might need to use PIL for this)
        # For now, using placeholder values
        image_info = {
            "id": idx + 1,
            "file_name": ann['image_name'],
            "width": 1920,  # Update with actual dimensions
            "height": 1080,  # Update with actual dimensions
        }
        coco_format["images"].append(image_info)
        
        # Convert points to COCO keypoint format [x, y, visibility]
        # visibility: 0=not labeled, 1=labeled but not visible, 2=labeled and visible
        keypoints = []
        num_keypoints = len(ann['points'])
        
        for point in ann['points']:
            visible = point.get('visible', True)
            visibility_flag = 2 if visible else 1
            keypoints.extend([point['x'], point['y'], visibility_flag])
        
        # Pad to 6 keypoints if needed (for backward compatibility)
        while len(keypoints) < 18:  # 6 keypoints * 3 values each
            keypoints.extend([0, 0, 0])
        
        annotation_info = {
            "id": idx + 1,
            "image_id": idx + 1,
            "category_id": 1,
            "keypoints": keypoints,
            "num_keypoints": num_keypoints,
            "bbox": [0, 0, 0, 0],  # Calculate bounding box if needed
            "area": 0,
            "iscrowd": 0
        }
        coco_format["annotations"].append(annotation_info)
    
    with open(output_file, 'w') as f:
        json.dump(coco_format, f, indent=2)
    
    print(f"✓ Exported to COCO format: {output_file}")

def export_to_yolo(annotations, images_folder='./images', output_folder='./yolo_annotations'):
    """Export annotations to YOLO format (normalized coordinates)"""
    
    output_folder = Path(output_folder)
    output_folder.mkdir(exist_ok=True)
    
    images_folder = Path(images_folder)
    
    for ann in annotations:
        image_name = Path(ann['image_name']).stem
        
        # You'll need actual image dimensions for normalization
        # For now using placeholder values
        img_width = 1920
        img_height = 1080
        
        # Normalize coordinates
        normalized_points = []
        for point in ann['points']:
            norm_x = point['x'] / img_width
            norm_y = point['y'] / img_height
            normalized_points.append(f"{norm_x:.6f} {norm_y:.6f}")
        
        # YOLO format: class_id x1 y1 x2 y2 x3 y3 x4 y4
        yolo_line = "0 " + " ".join(normalized_points)
        
        output_file = output_folder / f"{image_name}.txt"
        with open(output_file, 'w') as f:
            f.write(yolo_line + '\n')
    
    print(f"✓ Exported to YOLO format in folder: {output_folder}")

def export_statistics(annotations, output_file='annotation_stats.txt'):
    """Generate statistics about the annotations"""
    
    total = len(annotations)
    annotators = {}
    
    for ann in annotations:
        name = ann['annotator_name']
        annotators[name] = annotators.get(name, 0) + 1
    
    with open(output_file, 'w') as f:
        f.write("UAV Pose Annotation Statistics\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total Annotations: {total}\n")
        f.write(f"Number of Annotators: {len(annotators)}\n\n")
        f.write("Annotations per Annotator:\n")
        f.write("-" * 50 + "\n")
        
        for name, count in sorted(annotators.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total) * 100
            f.write(f"{name:30s}: {count:4d} ({percentage:5.1f}%)\n")
        
        f.write("\n")
        f.write(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"✓ Statistics exported: {output_file}")
    
    # Also print to console
    print("\n" + "=" * 50)
    print("Annotation Statistics")
    print("=" * 50)
    print(f"Total annotations: {total}")
    print(f"Annotators: {len(annotators)}")
    for name, count in sorted(annotators.items(), key=lambda x: x[1], reverse=True):
        print(f"  {name}: {count}")
    print("=" * 50 + "\n")

def main():
    """Main export function"""
    print("\n" + "=" * 60)
    print("UAV Annotation Exporter")
    print("=" * 60 + "\n")
    
    # Load annotations
    print("Loading annotations...")
    annotations = load_annotations()
    
    if not annotations:
        print("❌ No annotations found! Make sure you have annotated images.")
        return
    
    print(f"✓ Loaded {len(annotations)} annotations\n")
    
    # Export to different formats
    print("Exporting to multiple formats...\n")
    
    export_to_csv(annotations)
    export_to_coco(annotations)
    export_to_yolo(annotations)
    export_statistics(annotations)
    
    # Also create a simple JSON export
    with open('annotations_all.json', 'w') as f:
        json.dump(annotations, f, indent=2)
    print(f"✓ Exported raw JSON: annotations_all.json")
    
    print("\n" + "=" * 60)
    print("✅ Export complete!")
    print("=" * 60 + "\n")
    
    print("Files created:")
    print("  - annotations.csv (CSV format)")
    print("  - coco_annotations.json (COCO format)")
    print("  - yolo_annotations/ (YOLO format)")
    print("  - annotations_all.json (Raw JSON)")
    print("  - annotation_stats.txt (Statistics)")
    print()

if __name__ == '__main__':
    main()