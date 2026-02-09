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
    """Get list of all images, optionally filtered by subfolder"""
    subfolder = request.args.get('subfolder', '')
    
    images = []
    search_path = IMAGE_FOLDER / subfolder if subfolder else IMAGE_FOLDER
    
    if not search_path.exists():
        return jsonify({'images': [], 'error': 'Subfolder not found'})
    
    for img_file in search_path.glob('*'):
        if img_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
            # Store relative path if subfolder is used
            if subfolder:
                images.append(f"{subfolder}/{img_file.name}")
            else:
                images.append(img_file.name)
    
    images.sort()
    return jsonify({'images': images})

@app.route('/api/subfolders', methods=['GET'])
def get_subfolders():
    """Get list of all subfolders in images directory"""
    subfolders = ['']  # Empty string represents root folder
    
    for item in IMAGE_FOLDER.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            subfolders.append(item.name)
    
    subfolders.sort()
    return jsonify({'subfolders': subfolders})

@app.route('/api/image/<path:filename>')
def serve_image(filename):
    """Serve an image file (supports subfolders)"""
    # Handle subfolders in path
    file_path = IMAGE_FOLDER / filename
    if not file_path.exists():
        return jsonify({'error': 'Image not found'}), 404
    
    # Get the directory and filename
    directory = file_path.parent
    file_name = file_path.name
    
    return send_from_directory(directory, file_name)

@app.route('/api/annotations/<filename>', methods=['GET'])
def get_annotation(filename):
    """Get existing annotation for an image"""
    annotation_file = ANNOTATIONS_FOLDER / f"{Path(filename).stem}.json"
    
    if annotation_file.exists():
        with open(annotation_file, 'r') as f:
            return jsonify(json.load(f))
    
    return jsonify({'exists': False})

@app.route('/api/lock/<filename>', methods=['POST'])
def lock_image(filename):
    """Lock an image for editing by a specific annotator"""
    data = request.json
    annotator_id = data.get('annotator_id')
    annotator_name = data.get('annotator_name')
    
    lock_file = ANNOTATIONS_FOLDER / f".lock_{filename}"
    
    # Check if already locked
    if lock_file.exists():
        with open(lock_file, 'r') as f:
            lock_data = json.load(f)
            
        # Check if lock is stale (older than 5 minutes)
        lock_time = datetime.fromisoformat(lock_data['locked_at'])
        if (datetime.now() - lock_time).total_seconds() < 300:  # 5 minutes
            # Image is locked by someone else
            if lock_data['annotator_id'] != annotator_id:
                return jsonify({
                    'locked': True,
                    'locked_by': lock_data['annotator_name'],
                    'locked_at': lock_data['locked_at']
                })
    
    # Lock the image
    lock_data = {
        'annotator_id': annotator_id,
        'annotator_name': annotator_name,
        'locked_at': datetime.now().isoformat()
    }
    
    with open(lock_file, 'w') as f:
        json.dump(lock_data, f)
    
    return jsonify({'locked': False, 'success': True})

@app.route('/api/unlock/<filename>', methods=['POST'])
def unlock_image(filename):
    """Unlock an image"""
    lock_file = ANNOTATIONS_FOLDER / f".lock_{filename}"
    
    if lock_file.exists():
        lock_file.unlink()
    
    return jsonify({'success': True})

@app.route('/api/locks', methods=['GET'])
def get_all_locks():
    """Get all currently locked images"""
    locks = {}
    
    for lock_file in ANNOTATIONS_FOLDER.glob('.lock_*'):
        try:
            with open(lock_file, 'r') as f:
                lock_data = json.load(f)
            
            # Check if lock is stale
            lock_time = datetime.fromisoformat(lock_data['locked_at'])
            if (datetime.now() - lock_time).total_seconds() < 300:  # 5 minutes
                image_name = lock_file.name.replace('.lock_', '')
                locks[image_name] = lock_data
            else:
                # Remove stale lock
                lock_file.unlink()
        except:
            pass
    
    return jsonify(locks)

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
    
    # Unlock the image after saving
    lock_file = ANNOTATIONS_FOLDER / f".lock_{image_name}"
    if lock_file.exists():
        lock_file.unlink()
    
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