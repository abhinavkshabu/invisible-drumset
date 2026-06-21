# Invisible Drum Kit

ever wanted to play drums but you're broke and your parents said no? same. so i built this — just wave your hands in front of your webcam and it actually plays drum sounds. no drums needed lol

## what it does

- uses your **webcam + AI hand tracking** to detect your fingers in real time
- there are **8 drum pads** on screen (kick, snare, hi-hat, crash, toms, ride)
- just **flick your index finger down** over a pad and it makes the sound
- the drum sounds are **generated with code** — no audio files needed at all
- press `b` for an **autoplay beat** if you just wanna vibe
- works with your laptop webcam, USB cam, or even your phone camera (DroidCam etc)

## demo

just run it and start flicking your fingers over the pads. trust me it works

## how to run

```bash
pip install -r requirements.txt
python app.py
```

thats literally it

## controls

do this what happens
| flick finger down over a pad plays the drum sound
| press `b` toggles autoplay beat on/off
| press `q` quit

## how it works (for the nerds)

1. **MediaPipe** detects your hand landmarks through the webcam
2. the app tracks your index fingertip and watches for a fast downward flick
3. if the flick happens over a drum pad → boom, sound plays
4. all the sounds are synthesized using **numpy** (sine waves, noise, envelopes etc)
5. **pygame** handles audio playback, **opencv** handles the camera + drawing

## build an exe

if you wanna share it with someone who doesnt have python:

```bash
python build.py
```

gives you `dist/InvisibleDrumKit/InvisibleDrumKit.exe`

## files

app.py           — the main thing, all the logic lives here
config.py        — settings (camera, pad layout, thresholds)
hand_tracker.py  — basic hand tracking template i started with
build.py         — builds the exe with pyinstaller
build.spec       — pyinstaller config

##Note
***WEBCAM NEEDED***

made by [@abhinavkshabu](https://github.com/abhinavkshabu) ✌️
