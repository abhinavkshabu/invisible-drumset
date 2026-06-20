import cv2
import time
import sys
import os
import numpy as np
import pygame
import mediapipe as mp

# PyInstaller frozen-app support: ensure working directory is beside the .exe
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

from config import (
    CAMERA_SOURCE, CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_ROTATION,
    SMOOTHING_ALPHA,
    TAP_Y_HISTORY_SIZE,
    WINDOW_NAME, HUD_FONT_SCALE, HUD_THICKNESS,
    DRUM_PADS, DRUM_PAD_ALPHA, DRUM_VELOCITY_THRESHOLD, DRUM_COOLDOWN
)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

INDEX_TIP = mp_hands.HandLandmark.INDEX_FINGER_TIP
INDEX_DIP = mp_hands.HandLandmark.INDEX_FINGER_DIP

def generate_drum_sounds():
    """Generates synthetic drum sounds using NumPy arrays."""
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    sounds = {}
    
    def make_stereo(wave_1d):
        return np.column_stack((wave_1d, wave_1d))
    
    t = np.linspace(0, 0.15, int(44100 * 0.15), False)
    kick_freq = np.linspace(150, 40, len(t))
    kick_wave = np.sin(2 * np.pi * kick_freq * t)
    kick_wave = (kick_wave * np.exp(-t * 30) * 32767).astype(np.int16)
    sounds["kick"] = pygame.sndarray.make_sound(make_stereo(kick_wave))
    
    t_snare = np.linspace(0, 0.2, int(44100 * 0.2), False)
    noise = np.random.uniform(-1, 1, len(t_snare))
    pop = np.sin(2 * np.pi * 200 * t_snare) * np.exp(-t_snare * 50)
    snare_wave = ((noise + pop) * np.exp(-t_snare * 20) * 30000).astype(np.int16)
    sounds["snare"] = pygame.sndarray.make_sound(make_stereo(snare_wave))
    
    t_hat = np.linspace(0, 0.05, int(44100 * 0.05), False)
    noise_hat = np.random.uniform(-1, 1, len(t_hat))
    hat_wave = (noise_hat * np.exp(-t_hat * 100) * 28000).astype(np.int16)
    sounds["hihat"] = pygame.sndarray.make_sound(make_stereo(hat_wave))
    
    t_crash = np.linspace(0, 1.5, int(44100 * 1.5), False)
    noise_crash = np.random.uniform(-1, 1, len(t_crash))
    crash_wave = (noise_crash * np.exp(-t_crash * 3) * 30000).astype(np.int16)
    sounds["crash"] = pygame.sndarray.make_sound(make_stereo(crash_wave))
    
    t_ht = np.linspace(0, 0.25, int(44100 * 0.25), False)
    ht_freq = np.linspace(250, 150, len(t_ht))
    ht_wave = np.sin(2 * np.pi * ht_freq * t_ht)
    ht_wave = (ht_wave * np.exp(-t_ht * 15) * 32767).astype(np.int16)
    sounds["hightom"] = pygame.sndarray.make_sound(make_stereo(ht_wave))
    
    t_mt = np.linspace(0, 0.3, int(44100 * 0.3), False)
    mt_freq = np.linspace(180, 100, len(t_mt))
    mt_wave = np.sin(2 * np.pi * mt_freq * t_mt)
    mt_wave = (mt_wave * np.exp(-t_mt * 12) * 32767).astype(np.int16)
    sounds["midtom"] = pygame.sndarray.make_sound(make_stereo(mt_wave))
    
    t_ft = np.linspace(0, 0.4, int(44100 * 0.4), False)
    ft_freq = np.linspace(120, 60, len(t_ft))
    ft_wave = np.sin(2 * np.pi * ft_freq * t_ft)
    ft_wave = (ft_wave * np.exp(-t_ft * 10) * 32767).astype(np.int16)
    sounds["floortom"] = pygame.sndarray.make_sound(make_stereo(ft_wave))
    
    t_ride = np.linspace(0, 1.0, int(44100 * 1.0), False)
    ride_noise = np.random.uniform(-1, 1, len(t_ride))
    ride_ping = np.sin(2 * np.pi * 800 * t_ride) * np.exp(-t_ride * 10)
    ride_wave = ((ride_noise * 0.3 + ride_ping) * np.exp(-t_ride * 4) * 30000).astype(np.int16)
    sounds["ride"] = pygame.sndarray.make_sound(make_stereo(ride_wave))
    
    return sounds

class GestureState:
    def __init__(self):
        self.stick_y_history = {0: [], 1: []}
        self.last_strike_time = {0: 0.0, 1: 0.0}
        self.smoothed_sticks = {0: None, 1: None}
        self.active_pads = {}
        self.trails = {0: [], 1: []}
        self.max_trail = 12
        self.last_action = ""
        self.last_action_time = 0.0

    def set_action(self, label: str):
        self.last_action = label
        self.last_action_time = time.time()

    def add_trail(self, idx, point):
        self.trails[idx].append(point)
        if len(self.trails[idx]) > self.max_trail:
            self.trails[idx].pop(0)

def detect_strike(y_history, current_y, now, last_strike_time,
                  cooldown=DRUM_COOLDOWN, threshold=DRUM_VELOCITY_THRESHOLD):

    y_history.append(current_y)
    if len(y_history) > TAP_Y_HISTORY_SIZE:
        y_history.pop(0)

    if len(y_history) == TAP_Y_HISTORY_SIZE:
        if now - last_strike_time < cooldown:
            return False

        y_delta = y_history[-1] - y_history[0]

        if y_delta > threshold:
            y_history.clear()
            return True
    return False

def draw_drum_pads(frame, state, w, h):
    overlay = frame.copy()
    now = time.time()

    for pad in DRUM_PADS:
        px = int(pad["rect"][0] * w)
        py = int(pad["rect"][1] * h)
        pw = int(pad["rect"][2] * w)
        ph = int(pad["rect"][3] * h)

        color = pad["color"]
        if pad["name"] in state.active_pads and now - state.active_pads[pad["name"]] < 0.15:
            t = (now - state.active_pads[pad["name"]]) / 0.15
            flash = tuple(int(c + (255 - c) * (1 - t)) for c in color)
            color = flash
            ring_radius = int(min(pw, ph) // 2 + 20 * t)
            ring_alpha = int(180 * (1 - t))
            cv2.circle(frame, (px + pw // 2, py + ph // 2), ring_radius, (255, 255, 255), 2)

        cx, cy = px + pw // 2, py + ph // 2
        radius = min(pw, ph) // 2

        cv2.circle(overlay, (cx, cy), radius, color, -1)
        cv2.circle(frame, (cx, cy), radius, (255, 255, 255), 2)

        text_size = cv2.getTextSize(pad["name"], cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        cv2.putText(frame, pad["name"], (cx - text_size[0] // 2, cy + text_size[1] // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.addWeighted(overlay, DRUM_PAD_ALPHA, frame, 1 - DRUM_PAD_ALPHA, 0, frame)


def process_drums(frame, state, fingertips, frame_w, frame_h, drum_sounds):

    now = time.time()
    draw_drum_pads(frame, state, frame_w, frame_h)

    for idx, (cx, cy) in enumerate(fingertips):
        if idx > 1:
            break 

        alpha = SMOOTHING_ALPHA
        if state.smoothed_sticks[idx] is None:
            state.smoothed_sticks[idx] = (cx, cy)

        prev_x, prev_y = state.smoothed_sticks[idx]
        smooth_x = alpha * cx + (1 - alpha) * prev_x
        smooth_y = alpha * cy + (1 - alpha) * prev_y
        state.smoothed_sticks[idx] = (smooth_x, smooth_y)

        ix, iy = int(smooth_x), int(smooth_y)

        state.add_trail(idx, (ix, iy))

        for pad in DRUM_PADS:
            px = pad["rect"][0] * frame_w
            py = pad["rect"][1] * frame_h
            pw = pad["rect"][2] * frame_w
            ph = pad["rect"][3] * frame_h

            if px < ix < px + pw and py < iy < py + ph:
                if detect_strike(state.stick_y_history[idx], iy, now,
                                 state.last_strike_time[idx],
                                 DRUM_COOLDOWN, DRUM_VELOCITY_THRESHOLD):
                    drum_sounds[pad["sound"]].play()
                    state.active_pads[pad["name"]] = now
                    state.set_action(f"HIT {pad['name'].upper()}")
                    state.last_strike_time[idx] = now

        trail = state.trails[idx]
        for i in range(1, len(trail)):
            t = i / len(trail)  # 0→1
            thickness = int(2 + 6 * t)
            color_l = (0, int(200 * t), 255) if idx == 0 else (255, int(200 * t), 0)
            cv2.line(frame, trail[i - 1], trail[i], color_l, thickness)

        cv2.circle(frame, (ix, iy), 22, (0, 100, 180) if idx == 0 else (180, 100, 0), 2)
        cv2.circle(frame, (ix, iy), 14, (0, 220, 255) if idx == 0 else (255, 180, 0), -1)
        cv2.circle(frame, (ix, iy), 14, (255, 255, 255), 2)
        label = "L" if idx == 0 else "R"
        cv2.putText(frame, label, (ix - 6, iy + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 2)

def draw_hud(frame, state, hand_count, fps):
    h, w, _ = frame.shape
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 80), (15, 15, 15), -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

    if hand_count >= 1:
        mode_color = (0, 255, 120)
        mode_text = f"DRUM KIT — {hand_count} hand{'s' if hand_count > 1 else ''} detected"
    else:
        mode_color = (0, 140, 255)
        mode_text = "Show your hands to start!"

    cv2.circle(frame, (30, 40), 10, mode_color, -1)
    cv2.putText(frame, mode_text, (50, 35),
                cv2.FONT_HERSHEY_SIMPLEX, HUD_FONT_SCALE, mode_color, HUD_THICKNESS)

    cv2.putText(frame, f"Hands: {hand_count}", (50, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
    
    autoplay_status = "ON" if getattr(state, "autoplay_active", False) else "OFF"
    cv2.putText(frame, f"Autoplay Beat [b]: {autoplay_status}", (50, 85),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255) if autoplay_status == "ON" else (150, 150, 150), 1)
                
    cv2.putText(frame, f"FPS: {int(fps)}", (w - 130, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 100), 1)

    if state.last_action and (time.time() - state.last_action_time < 0.6):
        action_alpha = max(0, 1.0 - (time.time() - state.last_action_time) / 0.6)
        color_intensity = int(255 * action_alpha)
        action_color = (0, color_intensity, color_intensity)

        text_size = cv2.getTextSize(state.last_action, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
        cv2.putText(frame, state.last_action,
                    ((w - text_size[0]) // 2, h - 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, action_color, 3)

    cv2.putText(frame, "Flick down to strike | Press 'b' for autoplay beat | 'q' to quit",
                (10, h - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)

def main():
    print("=" * 60)
    print("  INVISIBLE DRUM KIT v5 — MediaPipe Hands")
    print("=" * 60)

    drum_sounds = generate_drum_sounds()
    print("[INFO] Drum sounds loaded.")

    source = CAMERA_SOURCE
    if source is None:
        print("\nSelect Camera Source:")
        print(" [0] Default Webcam")
        print(" [1] Second USB Camera")
        print(" [2] Enter IP Camera URL (e.g., http://192.168.1.x:4747/video)")
        choice = input("\nEnter choice (0-2) or paste IP address [0]: ").strip()

        if choice == "1":
            source = 1
        elif choice == "2":
            url = input("Enter full camera URL or just the IP (e.g. 192.168.1.8): ").strip()
            if url and not url.startswith("http") and not url.startswith("rtsp"):
                source = f"http://{url}:4747/video" if ":" not in url else f"http://{url}/video"
            else:
                source = url
        elif choice and "." in choice:
            if not choice.startswith("http") and not choice.startswith("rtsp"):
                source = f"http://{choice}:4747/video" if ":" not in choice else f"http://{choice}/video"
            else:
                source = choice
        else:
            source = 0

    print(f"[INFO] Connecting to camera: {source}")
    cap = cv2.VideoCapture(source)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FPS, 60)

    if isinstance(source, int):
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    if not cap.isOpened():
        print(f"[ERROR] Could not open camera {source}.")
        sys.exit(1)

    cv2.namedWindow(WINDOW_NAME)

    state = GestureState()
    state.autoplay_active = False
    
    prev_frame_time = time.time()
    reconnect_attempts = 0
    
    last_beat_time = 0
    beat_interval = 0.25 
    beat_step = 0

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.5,
        model_complexity=0 
    )

    print("[INFO] MediaPipe Hands ready. Show your hands and start drumming!")
    print("[INFO] Flick your index finger DOWN fast over a drum pad to strike.\n")

    while True:
        success, frame = cap.read()
        if not success:
            reconnect_attempts += 1
            if reconnect_attempts > 5:
                print("[INFO] Reconnecting to camera...")
                cap.release()
                cap = cv2.VideoCapture(source)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                cap.set(cv2.CAP_PROP_FPS, 60)
                reconnect_attempts = 0
            time.sleep(0.05)
            continue

        reconnect_attempts = 0

        frame = cv2.flip(frame, 1)

        if CAMERA_ROTATION == 90:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif CAMERA_ROTATION == 180:
            frame = cv2.rotate(frame, cv2.ROTATE_180)
        elif CAMERA_ROTATION == 270:
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        h, w, _ = frame.shape

        now = time.time()
        fps = 1.0 / max(now - prev_frame_time, 0.001)
        prev_frame_time = now

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        fingertips = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_styles.get_default_hand_landmarks_style(),
                    mp_styles.get_default_hand_connections_style()
                )

                tip = hand_landmarks.landmark[INDEX_TIP]
                px = int(tip.x * w)
                py = int(tip.y * h)
                fingertips.append((px, py))

        fingertips = sorted(fingertips, key=lambda p: p[0])

        process_drums(frame, state, fingertips, w, h, drum_sounds)
        if state.autoplay_active:
            if now - last_beat_time > beat_interval:
                last_beat_time = now
                if beat_step % 2 == 0:
                    drum_sounds["hihat"].play()
                if beat_step == 0 or beat_step == 4:
                    drum_sounds["kick"].play()
                    state.active_pads["Kick"] = now
                if beat_step == 2 or beat_step == 6:
                    drum_sounds["snare"].play()
                    state.active_pads["Snare"] = now
                    
                beat_step = (beat_step + 1) % 8

        draw_hud(frame, state, len(fingertips), fps)

        cv2.imshow(WINDOW_NAME, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\n[INFO] Shutting down...")
            break
        elif key == ord('b'):
            state.autoplay_active = not state.autoplay_active
            print(f"\n[INFO] Autoplay Beat {'ON' if state.autoplay_active else 'OFF'}")

    hands.close()
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Goodbye.")


if __name__ == "__main__":
    main()