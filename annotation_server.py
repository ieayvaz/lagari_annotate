#!/usr/bin/env python3
"""
UAV Pose Annotation Server
Serves images to annotators and collects their annotations
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import socket

app = Flask(__name__)
CORS(app)

# Configuration
IMAGE_FOLDER = Path("./images")
ANNOTATIONS_FOLDER = Path("./annotations")
ANNOTATORS_FILE = Path("./annotators.json")

# Create folders if they don't exist
IMAGE_FOLDER.mkdir(exist_ok=True)
ANNOTATIONS_FOLDER.mkdir(exist_ok=True)

# Initialize annotators tracking
if not ANNOTATORS_FILE.exists():
    with open(ANNOTATORS_FILE, 'w') as f:
        json.dump({}, f)

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

@app.route('/')
def index():
    """Serve the annotation interface"""
    return render_template('annotator.html')

@app.route('/api/register', methods=['POST'])
def register_annotator():
    """Register a new annotator"""
    data = request.json
    name = data.get('name', 'Unknown')
    
    with open(ANNOTATORS_FILE, 'r') as f:
        annotators = json.load(f)
    
    annotator_id = f"annotator_{len(annotators) + 1}"
    annotators[annotator_id] = {
        'name': name,
        'registered_at': datetime.now().isoformat(),
        'annotations_count': 0
    }
    
    with open(ANNOTATORS_FILE, 'w') as f:
        json.dump(annotators, f, indent=2)
    
    return jsonify({'annotator_id': annotator_id, 'name': name})

@app.route('/api/images', methods=['GET'])
def get_images():
    """Get list of all images"""
    images = []
    for img_file in IMAGE_FOLDER.glob('*'):
        if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
            images.append(img_file.name)
    
    images.sort()
    return jsonify({'images': images})

@app.route('/api/image/<filename>')
def serve_image(filename):
    """Serve an image file"""
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/api/annotations/<filename>', methods=['GET'])
def get_annotation(filename):
    """Get existing annotation for an image"""
    annotation_file = ANNOTATIONS_FOLDER / f"{Path(filename).stem}.json"
    
    if annotation_file.exists():
        with open(annotation_file, 'r') as f:
            return jsonify(json.load(f))
    
    return jsonify({'exists': False})

@app.route('/api/annotate', methods=['POST'])
def save_annotation():
    """Save an annotation"""
    data = request.json
    
    image_name = data['image_name']
    annotator_id = data['annotator_id']
    annotator_name = data['annotator_name']
    points = data['points']
    
    # Create annotation record with visibility support
    annotation = {
        'image_name': image_name,
        'annotator_id': annotator_id,
        'annotator_name': annotator_name,
        'timestamp': datetime.now().isoformat(),
        'points': points  # Now includes x, y, and visible for each point
    }
    
    # Save to file
    annotation_file = ANNOTATIONS_FOLDER / f"{Path(image_name).stem}.json"
    with open(annotation_file, 'w') as f:
        json.dump(annotation, f, indent=2)
    
    # Update annotator stats
    with open(ANNOTATORS_FILE, 'r') as f:
        annotators = json.load(f)
    
    if annotator_id in annotators:
        annotators[annotator_id]['annotations_count'] = annotators[annotator_id].get('annotations_count', 0) + 1
        annotators[annotator_id]['last_annotation'] = datetime.now().isoformat()
        
        with open(ANNOTATORS_FILE, 'w') as f:
            json.dump(annotators, f, indent=2)
    
    print(f"✓ Annotation saved: {image_name} by {annotator_name}")
    
    return jsonify({'status': 'success', 'message': 'Annotation saved'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get annotation statistics"""
    with open(ANNOTATORS_FILE, 'r') as f:
        annotators = json.load(f)
    
    total_images = len(list(IMAGE_FOLDER.glob('*')))
    total_annotations = len(list(ANNOTATIONS_FOLDER.glob('*.json')))
    
    return jsonify({
        'total_images': total_images,
        'total_annotations': total_annotations,
        'annotators': annotators
    })

@app.route('/api/export', methods=['GET'])
def export_dataset():
    """Export all annotations in a standard format"""
    dataset = []
    
    for annotation_file in ANNOTATIONS_FOLDER.glob('*.json'):
        with open(annotation_file, 'r') as f:
            data = json.load(f)
            dataset.append(data)
    
    export_file = Path('dataset_export.json')
    with open(export_file, 'w') as f:
        json.dump(dataset, f, indent=2)
    
    return send_from_directory('.', 'dataset_export.json', as_attachment=True)

if __name__ == '__main__':
    local_ip = get_local_ip()
    
    print("=" * 60)
    print("UAV POSE ANNOTATION SERVER")
    print("=" * 60)
    print(f"\nServer starting on:")
    print(f"  Local:   http://localhost:5000")
    print(f"  Network: http://{local_ip}:5000")
    print(f"\nShare the Network URL with your team members!")
    print(f"\nImages folder: {IMAGE_FOLDER.absolute()}")
    print(f"Annotations folder: {ANNOTATIONS_FOLDER.absolute()}")
    print("\nPress Ctrl+C to stop the server\n")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=False)