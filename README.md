# Invisible Drum Kit

ever wanted to play drums but you're broke and your parents said no? same. so i built this instead lmao — just wave your hands in front of your webcam and it actually plays drum sounds. no real drums needed. your neighbours will thank you

## just download and run it (no coding needed)

[![Download Latest Release](https://img.shields.io/github/v/release/abhinavkshabu/invisible-drumset?label=Download%20.exe&style=for-the-badge&color=brightgreen)](https://github.com/abhinavkshabu/invisible-drumset/releases/latest)

1. **grab it** → [`InvisibleDrumKit-v1.0.1-windows.zip`](https://github.com/abhinavkshabu/invisible-drumset/releases/download/v1.0.1/InvisibleDrumKit-v1.0.1-windows.zip)
2. **unzip** it somewhere (desktop works)
3. **open** the `InvisibleDrumKit` folder
4. **double click** `InvisibleDrumKit.exe`
5. **allow camera** if windows asks
6. start drumming 🥁🔥

##!IMPORTANT
> **dont move the exe out of its folder!!** it needs the `_internal` folder right next to it or it wont work. just run it from inside the folder you extracted

> ##!TIP
> windows smartscreen might freak out and block it. just click **"More info"** → **"Run anyway"**. its safe i promise, its just not signed because im broke lol

## what it does

- uses your **webcam + AI** to track your hands in real time
- **7 drum pads** on screen — kick, snare, hi-hat, crash, toms, ride, floor tom
- **flick your finger down** over a pad and boom it makes the sound
- all the sounds are **made with math** — no audio files at all, pure code 🤓
- press `b` for a sick **auto beat** if you just wanna vibe
- works with laptop cam, USB webcam, or even your **phone camera** (DroidCam etc)

## demo

just download it and start flicking your fingers over the pads. trust me bro it works

## controls

| what to do | what happens |
|------------|-------------|
| flick finger down on a pad | plays that drum sound |
| press `b` | turns autoplay beat on/off |
| press `q` | quit |

thats it. thats all the controls lol

## it doesnt work!! 😡

chill. check this:

| problem | fix |
|---------|-----|
| **windows blocks it** | click "More info" → "Run anyway" (its safe bro) |
| **antivirus goes crazy** | add the folder to exclusions — its a false positive, pyinstaller does that |
| **"camera not found"** | close zoom/teams/whatever is hogging your webcam |
| **black screen** | wrong camera selected. find `config.py` in the `_internal` folder and change `CAMERA_SOURCE = 0` to `1` |
| **laggy af** | close chrome (yes all 47 tabs) the AI needs cpu |
| **crashes instantly** | did you actually extract the zip?? dont run it from inside the zip. also check for `crash_log.txt` next to the exe |
| **error popup shows up** | read it lol. also check `crash_log.txt` — it has all the details |

> ##!TIP
> if it crashes it saves a `crash_log.txt` right next to the exe. send me that file and ill figure out whats wrong

## wanna run from source?

if you have python:

```bash
pip install -r requirements.txt
python app.py
```

thats literally it. two commands. done.

## how it works (nerd stuff)

1. **mediapipe** (google's AI) tracks your hand through the webcam
2. the app watches your index fingertip for a fast downward flick
3. if you flick over a drum pad → sound plays
4. the sounds are all **synthesized with numpy** (sine waves + noise + envelopes)
5. **pygame** plays the audio, **opencv** handles camera + drawing
6. its basically math pretending to be music

## build the exe yourself

```bash
python build.py
```

spits out `dist/InvisibleDrumKit/InvisibleDrumKit.exe`. zip that folder and you got a portable drumkit

## project files

```
app.py           — all the magic happens here
config.py        — tweak settings (camera, pads, sensitivity)
hand_tracker.py  — hand tracking template i started with
build.py         — one click exe builder
build.spec       — pyinstaller config (dont touch unless you know what ur doing)
```

## built with

- **opencv** — camera go brr
- **mediapipe** — google's hand tracking AI
- **numpy** — math for sound synthesis
- **pygame** — plays the sounds

## you need

- python 3.10+ (only if running from source)
- a webcam
- hands (preferably 2 but 1 works too)
- mass hysteria (optional)

---

if you liked this give it a star
