CAMERA_SOURCE = 0

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_ROTATION = 180
SMOOTHING_ALPHA = 0.3

TAP_Y_HISTORY_SIZE = 5
TAP_VELOCITY_THRESHOLD = 15
TAP_COOLDOWN = 0.35

WINDOW_NAME = "invisible peripheral suite v2"
show_landmarks = True
HUD_FONT_SCALE = 0.7
HUD_THICKNESS = 2

DRUM_PADS = [
    {"name" : "Crash", "color": (255,200,0), "rect" : (0.05,0.1,0.2,0.3), "sound": "crash"},
    {"name" : "Hi-Tom", "color": (0,200,255), "rect": (0.30, 0.1,0.2,0.3), "sound": "hightom"},
    {"name" : "Mid Tom", "color": (200,150,0), "rect": (0.80,0.1,0.2,0.3), "sound": "ride"},

    {"name" : "Hi-Hat", "color": (200,255,0), "rect": (0.05,0.5,0.2,0.3), "sound": "hihat"},
    {"name" : "Snare", "color" : (0,255,255), "rect" : (0.30,0.5,0.2,0.3), "sound": "snare"},
    {"name" : "Kick", "color" : (200,0,255), "rect" : (0.55,0.5,0.2,0.3), "sound" : "kick"},
    {"name" : "Floor Tom", "color": (150,0,255),"rect":(0.80,0.5,0.2,0.3), "sound": "floortom"}

]
DRUM_PAD_ALPHA = 0.4
DRUM_VELOCITY_THRESHOLD = 28
DRUM_COOLDOWN = 0.05
