# 🥁 Invisible Drum Kit

ever wanted to play drums but you're broke and your parents said no? same. so i built this — just wave your hands in front of your webcam and it actually plays drum sounds. no drums needed lol

## ⬇️ download & run (no python needed)

[![Download Latest Release](https://img.shields.io/github/v/release/abhinavkshabu/invisible-drumset?label=Download%20.exe&style=for-the-badge&color=brightgreen)](https://github.com/abhinavkshabu/invisible-drumset/releases/latest)

1. **Download** → [`InvisibleDrumKit-v1.0.0-windows.zip`](https://github.com/abhinavkshabu/invisible-drumset/releases/download/v1.0.0/InvisibleDrumKit-v1.0.0-windows.zip)
2. **Extract** the zip to any folder
3. **Open** the extracted `InvisibleDrumKit` folder
4. **Double-click** `InvisibleDrumKit.exe` to launch
5. **Allow webcam access** if Windows asks
6. Show your hands and start drumming! 🎶

> [!IMPORTANT]
> **Do NOT move `InvisibleDrumKit.exe` out of its folder.** It needs the `_internal` folder next to it to work. Always run it from inside the extracted folder.

> [!TIP]
> If Windows SmartScreen pops up, click **"More info"** → **"Run anyway"**. The app is safe — it just isn't code-signed.

## what it does

- uses your **webcam + AI hand tracking** to detect your fingers in real time
- there are **8 drum pads** on screen (kick, snare, hi-hat, crash, toms, ride)
- just **flick your index finger down** over a pad and it makes the sound
- the drum sounds are **generated with code** — no audio files needed at all
- press `b` for an **autoplay beat** if you just wanna vibe
- works with your laptop webcam, USB cam, or even your phone camera (DroidCam etc)

## demo

just run it and start flicking your fingers over the pads. trust me it works

## controls

| do this | what happens |
|---------|-------------|
| flick finger down over a pad | plays the drum sound |
| press `b` | toggles autoplay beat on/off |
| press `q` | quit |

## troubleshooting

| problem | fix |
|---------|-----|
| **Windows SmartScreen blocks it** | click "More info" → "Run anyway" |
| **Antivirus flags the exe** | add the extracted folder to your antivirus exclusions — it's a false positive from PyInstaller |
| **"Camera not found" error** | make sure no other app is using the webcam (close Zoom, Teams, etc) |
| **Black screen / no video** | try a different camera — edit `config.py` and change `CAMERA_SOURCE = 0` to `1` |
| **Laggy / low FPS** | close other heavy apps; the AI hand tracking needs some CPU |
| **exe crashes immediately** | make sure you extracted the full zip — don't run the exe from inside the zip |

## how to run from source

if you have python and wanna run it directly:

```bash
pip install -r requirements.txt
python app.py
```

thats literally it

## how it works (for the nerds)

1. **MediaPipe** detects your hand landmarks through the webcam
2. the app tracks your index fingertip and watches for a fast downward flick
3. if the flick happens over a drum pad → boom, sound plays
4. all the sounds are synthesized using **numpy** (sine waves, noise, envelopes etc)
5. **pygame** handles audio playback, **opencv** handles the camera + drawing

## build an exe yourself

if you wanna build it from source:

```bash
python build.py
```

gives you `dist/InvisibleDrumKit/InvisibleDrumKit.exe`

## files

```
app.py           — the main thing, all the logic lives here
config.py        — settings (camera, pad layout, thresholds)
hand_tracker.py  — basic hand tracking template i started with
build.py         — builds the exe with pyinstaller
build.spec       — pyinstaller config
```

## built with

- opencv
- mediapipe
- numpy
- pygame

## requirements (for running from source)

- python 3.10+
- a webcam
- hands (preferably 2)

---

made by [@abhinavkshabu](https://github.com/abhinavkshabu) :P
