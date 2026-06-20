# Invisible Drum Kit 🥁

[![Download](https://img.shields.io/github/v/release/abhinavkshabu/invisible-drumset?label=Download%20.exe&style=for-the-badge&color=00e5ff)](https://github.com/abhinavkshabu/invisible-drumset/releases/latest)

Play drums in the air using AI-powered hand tracking. No physical drums needed — just your webcam and your hands.

> **Just want to try it?** Grab the `.exe` from the [latest release](https://github.com/abhinavkshabu/invisible-drumset/releases/latest) — no Python needed!

## Features

- **Real-time hand tracking** using MediaPipe — detects both hands simultaneously
- **8 drum pads** rendered on screen: Crash, Hi-Tom, Ride, Hi-Hat, Snare, Kick, Mid Tom, Floor Tom
- **Strike detection** via downward flick of your index finger over a drum pad
- **Synthesized drum sounds** generated with NumPy — no external audio files needed
- **Autoplay beat** (`b` key) — plays a basic kick-snare-hihat loop
- **Smoothed tracking** with motion trails for a polished visual experience
- **Camera flexibility** — supports webcam, USB cameras, and IP cameras (e.g., DroidCam)

## Requirements

- Python 3.10+
- Webcam or IP camera
- Windows / macOS / Linux

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

## Controls

| Key | Action |
|-----|--------|
| **Flick index finger down** | Strike a drum pad |
| `b` | Toggle autoplay beat |
| `q` | Quit |

## How It Works

1. MediaPipe Hands detects your index fingertips in real-time
2. The app tracks downward flicking motion (velocity-based strike detection)
3. When a flick is detected over a drum pad, the corresponding synthesized sound plays
4. Visual feedback includes pad flash animations, fingertip trails, and an action HUD

## Building a Standalone Executable

```bash
# Builds InvisibleDrumKit.exe using PyInstaller
python build.py
```

The output will be in `dist/InvisibleDrumKit/`.

## Project Structure

```
├── app.py             # Main application — hand tracking + drum logic
├── config.py          # All tunable parameters (camera, pads, thresholds)
├── hand_tracker.py    # Standalone hand-tracking demo/template
├── launcher.py        # Minimal web landing page server
├── build.py           # PyInstaller build automation script
├── build.spec         # PyInstaller spec with MediaPipe/OpenCV bundling
└── requirements.txt   # Python dependencies
```

## Tech Stack

- **OpenCV** — camera capture and rendering
- **MediaPipe** — hand landmark detection
- **NumPy** — synthetic drum sound generation
- **Pygame** — audio playback

## License

MIT
