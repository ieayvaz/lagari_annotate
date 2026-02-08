# UAV Pose Estimation Annotation Tool 🛩️

A web-based collaborative annotation tool for your Lagari UAV team to easily annotate fixed-wing UAV poses with 4 keypoints: Head, Tail, Right Wing, and Left Wing.

## ✨ Features

- **Easy Setup**: Works on both Linux and Windows with just Python and a browser
- **No Installation Required for Annotators**: Team members just open a browser
- **Real-time Collaboration**: 20+ people can annotate simultaneously
- **Instant Sync**: Annotations are sent to your PC immediately (no Telegram spam!)
- **Local Network**: Works on your WiFi - no internet needed
- **Beautiful UI**: Clean, intuitive interface with keyboard shortcuts
- **Progress Tracking**: See team progress in real-time
- **Auto-save**: Never lose work

## 🚀 Quick Start

### On Your PC (Server)

1. **Install Python** (if not already installed)
   - Download from python.org
   - Make sure Python 3.7+ is installed

2. **Install Dependencies**
   ```bash
   # On Linux/Mac
   pip3 install -r requirements.txt
   
   # On Windows
   pip install -r requirements.txt
   ```

3. **Add Your Images**
   - Create an `images` folder in the same directory as `annotation_server.py`
   - Put all your UAV images in this folder (supports .jpg, .jpeg, .png, .bmp)

4. **Start the Server**
   ```bash
   # On Linux/Mac
   python3 annotation_server.py
   
   # On Windows
   python annotation_server.py
   ```

5. **Share the URL**
   - The server will show you a URL like: `http://192.168.1.100:5000`
   - Share this URL with your team members
   - They just need to open it in any browser!

### For Team Members (Annotators)

1. Open the URL shared by the server admin in your browser
2. Enter your name
3. Start annotating!

## 📝 How to Annotate

1. **Select an image** from the list on the left
2. **Click 4 points** on the image in this order:
   - 🔴 Red: Head (nose of the UAV)
   - 🔵 Blue: Tail
   - 🟢 Green: Right Wing Tip
   - 🟡 Yellow: Left Wing Tip
3. **Save** using the Save button or press `S`
4. Move to the next image!

### Keyboard Shortcuts ⌨️

- `→` - Next image
- `←` - Previous image
- `S` - Save and move to next
- `R` - Reset points on current image

## 📁 Project Structure

```
uav-annotation-tool/
├── annotation_server.py    # Server (runs on your PC)
├── templates/
│   └── annotator.html      # Web interface
├── requirements.txt        # Python dependencies
├── images/                 # Put your UAV images here
├── annotations/            # Annotations are saved here (auto-created)
├── annotators.json         # Team member tracking (auto-created)
└── README.md              # This file
```

## 💾 Annotation Format

Annotations are saved as JSON files in the `annotations/` folder:

```json
{
  "image_name": "uav_001.jpg",
  "annotator_id": "annotator_1",
  "annotator_name": "John Doe",
  "timestamp": "2026-02-08T10:30:00",
  "points": [
    {"x": 320.5, "y": 180.2},  // Head
    {"x": 520.8, "y": 185.4},  // Tail
    {"x": 420.3, "y": 120.6},  // Right Wing
    {"x": 420.1, "y": 240.8}   // Left Wing
  ]
}
```

## 📊 Export Dataset

To export all annotations in a single file:

1. Open your browser and go to: `http://YOUR_IP:5000/api/export`
2. This downloads `dataset_export.json` with all annotations

Or use this Python script:

```python
import json
from pathlib import Path

annotations_folder = Path('./annotations')
dataset = []

for file in annotations_folder.glob('*.json'):
    with open(file) as f:
        dataset.append(json.load(f))

with open('dataset.json', 'w') as f:
    json.dump(dataset, f, indent=2)

print(f"Exported {len(dataset)} annotations!")
```

## 🔧 Troubleshooting

### Server won't start
- Make sure port 5000 is not in use
- Check if Flask is installed: `pip list | grep -i flask`
- Try running with: `python3 annotation_server.py`

### Can't connect from other computers
- Make sure you're all on the same WiFi network
- Check if firewall is blocking port 5000:
  - **Linux**: `sudo ufw allow 5000`
  - **Windows**: Add firewall rule for port 5000
- Verify the IP address shown by the server is correct

### Images not loading
- Make sure images are in the `images/` folder
- Supported formats: .jpg, .jpeg, .png, .bmp
- Check file permissions (files should be readable)

### Annotations not saving
- Check write permissions on the `annotations/` folder
- Look at server console for error messages
- Make sure annotator is registered (entered name)

## 🎯 Tips for Efficient Annotation

1. **Use keyboard shortcuts** - Much faster than clicking buttons
2. **Zoom in** - Most browsers support Ctrl+Scroll to zoom
3. **Be consistent** - Always annotate in the same order
4. **Take breaks** - Annotating is tiring for the eyes
5. **Check your work** - You can reload any image to verify points

## 🔒 Data Privacy

- All data stays on your local network
- No data is sent to the internet
- Only people on your WiFi can access the tool

## 📈 Monitoring Progress

Visit `http://YOUR_IP:5000/api/stats` to see:
- Total images
- Total annotations
- Per-annotator statistics

## 🤝 Team Coordination

**Recommended workflow:**
1. Divide images among team members
2. Each person annotates their assigned batch
3. Cross-validate: have someone else check 10% of annotations
4. Export and merge all annotations

## 🆘 Support

If you encounter issues:
1. Check the server console for error messages
2. Check the browser console (F12) for errors
3. Make sure all team members are using modern browsers (Chrome, Firefox, Edge)

## 📄 License

Free to use for the Lagari UAV team and educational purposes.

---

**Built for the Lagari UAV Team** 🚀

Good luck with your dataset collection!
