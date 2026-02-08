# 🛩️ UAV Annotation Tool - Quick Reference Card

## 🚀 Quick Start (Server Admin)

```bash
# Linux
./start_server.sh

# Windows
Double-click start_server.bat
```

Share this URL with your team: `http://YOUR_IP:5000`

---

## 👥 Quick Start (Annotators)

1. Open URL in browser
2. Enter your name
3. Click image → Place 4 points → Press S
4. Repeat!

---

## 🎯 The 4 Keypoints (in order)

| # | Keypoint | Color | Description |
|---|----------|-------|-------------|
| 1 | Head | 🔴 Red | Front/Nose of UAV |
| 2 | Tail | 🔵 Blue | Back of UAV |
| 3 | Right Wing | 🟢 Green | Right wing tip |
| 4 | Left Wing | 🟡 Yellow | Left wing tip |

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `→` | Next image |
| `←` | Previous image |
| `S` | Save & next |
| `R` | Reset points |

---

## 💾 Export Dataset

```bash
python3 export_annotations.py
```

Creates: CSV, COCO, YOLO, JSON formats

---

## 🔧 Troubleshooting

**Can't connect?**
- Check server is running
- Same WiFi network?
- Firewall: `sudo ufw allow 5000` (Linux)

**No images?**
- Put images in `images/` folder
- Restart server

**Can't save?**
- Place all 4 points first
- Check server terminal for errors

---

## 📊 File Structure

```
images/          ← PUT YOUR IMAGES HERE
annotations/     ← Saved annotations
annotators.json  ← Team tracking
```

---

## 💡 Pro Tips

✅ Use keyboard shortcuts (3x faster!)
✅ Zoom in with Ctrl+Scroll
✅ Be consistent with point placement
✅ Take 5-min breaks every 25 min
✅ Cross-check 10% of annotations

---

## 📈 Expected Performance

- Time per image: ~30 seconds
- 20 people can annotate 1000 images in ~25 minutes
- Quality control adds ~10 minutes

---

## 🆘 Need Help?

1. Check server terminal
2. Press F12 in browser (console)
3. Read COMPLETE_GUIDE.md
4. Ask your team lead

---

**URL Format:** `http://192.168.1.XXX:5000`

Replace XXX with your server's IP address

---

*Print this card and keep it handy during annotation sessions!*
