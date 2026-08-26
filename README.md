# Invisible Drum Kit

ever wanted to play drums but you're broke and your parents said no? same. so i built this instead lmao . you need just a webcam and your hands.

## just download and run it

[![Download Latest Release](https://img.shields.io/github/v/release/abhinavkshabu/invisible-drumset?label=Download%20.exe&style=for-the-badge&color=brightgreen)](https://github.com/abhinavkshabu/invisible-drumset/releases/latest)

1. here [`InvisibleDrumKit-v1.0.1-windows.zip`](https://github.com/abhinavkshabu/invisible-drumset/releases/download/v1.0.1/InvisibleDrumKit-v1.0.1-windows.zip)
2. extract it
3. open the `InvisibleDrumKit` folder
4. double click `InvisibleDrumKit.exe`
5. allow camera if windows asks
6. start drumming

> windows smartscreen might freak out and block it. just click **"More info"** → **"Run anyway"**. its safe i promise, its just not signed because im broke lol

## what it does

- uses your **webcam + AI** to track your hands in real time
- **7 drum pads** on screen kick, snare, hi-hat, crash, toms, ride, floor tom
- **flick your finger down** over a pad and boom it makes the sound
- all the sounds are **made with math** no audio files at all, pure code 
- press `b` for a sick **auto beat** if you just wanna vibe

## demo

just download it and start flicking your fingers over the pads. trust me bro it works
<img width="1592" height="892" alt="image" src="https://github.com/user-attachments/assets/d3d5a492-17d5-46d7-9b9c-777d251f87fd" />

## how it works (nerd stuff)

1. **mediapipe** (google's AI) tracks your hand through the webcam
2. the app watches your index fingertip for a fast downward flick
3. if you flick over a drum pad ( sound plays)
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
app.py          all the magic happens here
config.py       tweak settings (camera, pads, sensitivity)
hand_tracker.py hand tracking template i started with
build.py        one click exe builder
build.spec      pyinstaller config (dont touch unless you know what ur doing)

---

if you liked this give it a star
