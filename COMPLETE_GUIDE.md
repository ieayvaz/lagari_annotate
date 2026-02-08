# 🛩️ UAV Pose Annotation Tool - Complete Setup Guide

## Quick Overview

This is a **web-based annotation tool** designed specifically for your 20-person Lagari UAV team. It allows everyone to annotate UAV poses simultaneously without spam messages!

### What You Get:
- ✅ Server runs on your PC
- ✅ Team members use any web browser (Chrome, Firefox, Edge)
- ✅ Works on both Linux and Windows
- ✅ All data stays on your local WiFi network
- ✅ Instant synchronization of annotations
- ✅ Beautiful, easy-to-use interface
- ✅ Progress tracking for the whole team
- ✅ Export to multiple formats (COCO, YOLO, CSV, JSON)

---

## 📋 System Requirements

### Your PC (Server):
- Python 3.7 or higher
- 2GB RAM minimum
- WiFi connection
- Linux or Windows

### Team Members (Annotators):
- Any modern web browser
- Connected to same WiFi network
- That's it! No installation needed!

---

## 🚀 Installation Guide

### Option 1: Automatic Setup (Recommended)

#### On Linux:
```bash
chmod +x setup.sh
./setup.sh
```

#### On Windows:
Double-click `setup.bat`

### Option 2: Manual Setup

#### Step 1: Install Python
- **Windows**: Download from https://python.org
- **Linux**: Usually pre-installed, or use `sudo apt install python3 python3-pip`

#### Step 2: Install Dependencies
```bash
# Linux/Mac
pip3 install -r requirements.txt

# Windows
pip install -r requirements.txt
```

#### Step 3: Prepare Your Images
1. Create a folder named `images` in the same directory as the scripts
2. Copy all your UAV images into this folder
3. Supported formats: .jpg, .jpeg, .png, .bmp

---

## 🎬 Starting the Server

### Option 1: Quick Start Scripts

#### Linux:
```bash
./start_server.sh
```

#### Windows:
Double-click `start_server.bat`

### Option 2: Manual Start
```bash
# Linux/Mac
python3 annotation_server.py

# Windows
python annotation_server.py
```

### What You'll See:
```
============================================================
UAV POSE ANNOTATION SERVER
============================================================

Server starting on:
  Local:   http://localhost:5000
  Network: http://192.168.1.100:5000

Share the Network URL with your team members!

Images folder: /path/to/images
Annotations folder: /path/to/annotations

Press Ctrl+C to stop the server
============================================================
```

**Important**: Copy the Network URL (e.g., `http://192.168.1.100:5000`) and share it with your team!

---

## 👥 For Team Members - How to Start Annotating

### Step 1: Open the Tool
1. Open your web browser (Chrome, Firefox, or Edge)
2. Go to the URL shared by the server admin (e.g., `http://192.168.1.100:5000`)

### Step 2: Register
1. Enter your name in the welcome screen
2. Click "Start Annotating"

### Step 3: Start Annotating!
1. Select an image from the list on the left
2. Click on the image to place 4 points in order:
   - 🔴 **Red** - Head (nose/front of UAV)
   - 🔵 **Blue** - Tail (back of UAV)
   - 🟢 **Green** - Right Wing Tip
   - 🟡 **Yellow** - Left Wing Tip
3. Click "Save" or press `S` to save
4. Move to next image!

---

## ⌨️ Keyboard Shortcuts (Super Useful!)

| Key | Action |
|-----|--------|
| `→` | Next image |
| `←` | Previous image |
| `S` | Save annotation and move to next |
| `R` | Reset points on current image |

**Pro Tip**: Use keyboard shortcuts to annotate 3x faster!

---

## 📊 Monitoring Progress

### Real-time Stats
- The left sidebar shows total progress
- Green markers indicate annotated images
- Progress bar shows percentage complete

### Detailed Statistics
Visit `http://YOUR_SERVER_IP:5000/api/stats` to see:
- Total images
- Total annotations
- Per-annotator statistics

---

## 💾 Exporting Your Dataset

### Method 1: Using the Export Script (Recommended)

```bash
# Linux/Mac
python3 export_annotations.py

# Windows
python export_annotations.py
```

This creates:
- `annotations.csv` - CSV format for Excel/Pandas
- `coco_annotations.json` - COCO format for deep learning
- `yolo_annotations/` - YOLO format text files
- `annotations_all.json` - Raw JSON format
- `annotation_stats.txt` - Team statistics

### Method 2: Direct Download
Visit: `http://YOUR_SERVER_IP:5000/api/export`

This downloads a JSON file with all annotations.

---

## 📁 Project Structure Explained

```
uav-annotation-tool/
├── annotation_server.py      # Main server (run this on your PC)
├── templates/
│   └── annotator.html        # Web interface (opens in browser)
├── requirements.txt          # Python dependencies
├── export_annotations.py     # Export to various formats
├── setup.sh                  # Linux setup script
├── setup.bat                 # Windows setup script
├── start_server.sh           # Linux start script
├── start_server.bat          # Windows start script
├── config.json               # Configuration (advanced)
├── README.md                 # Documentation
│
├── images/                   # PUT YOUR UAV IMAGES HERE
├── annotations/              # Saved annotations (auto-created)
├── annotators.json           # Team tracking (auto-created)
└── exports/                  # Exported datasets (auto-created)
```

---

## 🔧 Troubleshooting

### Problem: "Connection refused" or "Can't connect to server"

**Solutions:**
1. Make sure the server is running (check the terminal)
2. Verify you're on the same WiFi network
3. Check firewall settings:
   - **Linux**: `sudo ufw allow 5000`
   - **Windows**: Control Panel → Firewall → Allow an app → Add port 5000
4. Try using the server's IP address directly

### Problem: "No images found"

**Solutions:**
1. Make sure images are in the `images/` folder
2. Check supported formats: .jpg, .jpeg, .png, .bmp
3. Restart the server after adding images

### Problem: Annotations not saving

**Solutions:**
1. Check the server console for error messages
2. Make sure you entered your name when registering
3. Verify you placed all 4 points before saving
4. Check write permissions on the `annotations/` folder

### Problem: Port 5000 already in use

**Solution:** Edit `annotation_server.py` and change the port:
```python
app.run(host='0.0.0.0', port=5001, debug=False)  # Changed to 5001
```

### Problem: Images are too large/slow to load

**Solutions:**
1. Resize images before uploading (recommended: max 1920x1080)
2. Use JPG format instead of PNG for smaller file size
3. Ensure good WiFi signal strength

---

## 💡 Best Practices for Your Team

### Before Starting:
1. **Create a naming convention** for images (e.g., `uav_001.jpg`, `uav_002.jpg`)
2. **Test with 5-10 images** first to ensure everything works
3. **Brief your team** on the 4 keypoint locations
4. **Assign batches** to avoid duplicate work

### During Annotation:
1. **Be consistent** - always annotate in the same order
2. **Take breaks** - eye strain is real!
3. **Use keyboard shortcuts** - much faster
4. **Double-check** - you can review any image by clicking it again

### Quality Control:
1. Have 2-3 people cross-validate 10% of annotations
2. Export statistics regularly to track progress
3. Review outliers (images that took unusually long)

### Coordination:
1. Use a shared spreadsheet to assign image batches
2. Set daily/hourly targets
3. Celebrate milestones! 🎉

---

## 📈 Workflow Recommendation

### For 20 People Annotating 1000 Images:

**Setup (5 minutes):**
1. Server admin: Start the server
2. Share the URL with team

**Annotation (depends on team):**
- Divide 1000 images into 20 batches (50 images each)
- Each person annotates their batch
- Average time: ~30 seconds per image
- Total time: ~25 minutes per person

**Quality Control (10 minutes):**
- 3 people review 100 random images (10%)
- Fix any errors

**Export (2 minutes):**
- Run export script
- Share dataset with team

**Total Time: ~45 minutes for 1000 images with 20 people!**

---

## 🔒 Security & Privacy

- ✅ All data stays on your local network
- ✅ No internet connection required
- ✅ No data sent to external servers
- ✅ Only people on your WiFi can access the tool
- ✅ All annotations saved locally on your PC

---

## 🎯 Tips for Efficient Annotation

### Speed Tips:
1. **Use keyboard shortcuts** - Can double your speed
2. **Zoom strategically** - Ctrl+Scroll to zoom in browser
3. **Start with easy images** - Build momentum
4. **Work in focused sessions** - 25 min work, 5 min break

### Accuracy Tips:
1. **Consistent reference points** - Always use the same spot for each keypoint
2. **Check scale** - Make sure image is properly sized on screen
3. **Review before saving** - Quick visual check of all 4 points
4. **Take breaks** - Fatigue leads to errors

### Team Tips:
1. **Compare annotations** - Show each other your work
2. **Share difficult cases** - Discuss ambiguous images
3. **Track personal stats** - Friendly competition can help!
4. **Give feedback** - Help improve the tool

---

## 📊 Understanding the Annotation Format

### Coordinate System:
- Origin (0,0) is top-left corner of image
- X increases to the right
- Y increases downward
- Coordinates are in pixels

### JSON Structure:
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

---

## 🚀 Advanced Usage

### Custom Configuration:
Edit `config.json` to customize:
- Port number
- Colors for keypoints
- Point radius
- Auto-advance behavior

### Adding More Keypoints:
Modify the `POINT_LABELS` array in `annotator.html` to add additional points.

### Batch Processing:
Use the Python scripts in `exports/` to process annotations for training.

---

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs**: Look at the server terminal for error messages
2. **Browser console**: Press F12 to see browser errors
3. **Test connectivity**: Try `ping YOUR_SERVER_IP` from another computer
4. **Restart everything**: Stop server, close all browsers, restart
5. **Check the FAQ**: Common issues are documented in this guide

---

## 📞 Contact & Support

For the Lagari UAV Team:
- Keep this documentation handy
- Share issues with your team lead
- Suggest improvements!

---

## ✅ Pre-flight Checklist

Before your annotation session:

- [ ] Server is running and showing the correct IP
- [ ] All images are in the `images/` folder
- [ ] Team members can access the URL in their browsers
- [ ] Everyone has registered with their name
- [ ] Test annotation works (try 1-2 images)
- [ ] Keyboard shortcuts are working
- [ ] Firewall allows port 5000
- [ ] All team members know the 4 keypoint locations

---

## 🎉 You're Ready!

Good luck with your dataset collection for the Lagari UAV project!

**Remember:** Consistency is more important than speed. Take your time, stay focused, and help each other out.

Happy Annotating! 🛩️✨

---

*Built with ❤️ for the Lagari UAV Team*
*Last Updated: February 2026*
