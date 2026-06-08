import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 8000))

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invisible Drum Kit — AI-Powered Air Drumming</title>
    <meta name="description" content="Play drums in the air using hand tracking and AI. No physical drums needed — just your hands and a webcam.">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: rgba(255, 255, 255, 0.04);
            --text-primary: #f0f0f5;
            --text-secondary: #8888a0;
            --accent-cyan: #00e5ff;
            --accent-magenta: #e040fb;
            --accent-green: #00ffaa;
            --accent-orange: #ffab40;
            --glow-cyan: rgba(0, 229, 255, 0.3);
            --glow-magenta: rgba(224, 64, 251, 0.3);
        }

        body {
            font-family: 'Outfit', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            overflow-x: hidden;
            line-height: 1.6;
        }

        /* Animated background */
        .bg-grid {
            position: fixed;
            inset: 0;
            z-index: 0;
            background-image:
                linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
            background-size: 60px 60px;
            animation: gridMove 20s linear infinite;
        }

        @keyframes gridMove {
            0% { transform: translate(0, 0); }
            100% { transform: translate(60px, 60px); }
        }

        .bg-glow {
            position: fixed;
            width: 600px;
            height: 600px;
            border-radius: 50%;
            filter: blur(150px);
            opacity: 0.15;
            z-index: 0;
            pointer-events: none;
        }

        .bg-glow.cyan {
            background: var(--accent-cyan);
            top: -200px;
            right: -100px;
            animation: floatGlow 8s ease-in-out infinite;
        }

        .bg-glow.magenta {
            background: var(--accent-magenta);
            bottom: -200px;
            left: -100px;
            animation: floatGlow 10s ease-in-out infinite reverse;
        }

        @keyframes floatGlow {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(40px, -30px) scale(1.15); }
        }

        /* Layout */
        .content {
            position: relative;
            z-index: 1;
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 24px;
        }

        /* Navigation */
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 24px 0;
        }

        .logo {
            font-size: 1.3rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-magenta));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }

        .nav-links a {
            color: var(--text-secondary);
            text-decoration: none;
            margin-left: 32px;
            font-size: 0.95rem;
            font-weight: 400;
            transition: color 0.3s;
        }

        .nav-links a:hover {
            color: var(--text-primary);
        }

        /* Hero */
        .hero {
            text-align: center;
            padding: 100px 0 80px;
        }

        .badge {
            display: inline-block;
            padding: 6px 18px;
            border-radius: 100px;
            background: rgba(0, 229, 255, 0.1);
            border: 1px solid rgba(0, 229, 255, 0.25);
            color: var(--accent-cyan);
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 28px;
            animation: badgePulse 3s ease-in-out infinite;
        }

        @keyframes badgePulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(0, 229, 255, 0.15); }
            50% { box-shadow: 0 0 20px 4px rgba(0, 229, 255, 0.1); }
        }

        .hero h1 {
            font-size: clamp(2.8rem, 7vw, 5rem);
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 24px;
            letter-spacing: -2px;
        }

        .hero h1 .gradient-text {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-magenta));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero p {
            font-size: 1.2rem;
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto 48px;
            font-weight: 300;
        }

        .hero-buttons {
            display: flex;
            gap: 16px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 16px 32px;
            border-radius: 14px;
            font-size: 1.05rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s ease;
            cursor: pointer;
            border: none;
            font-family: 'Outfit', sans-serif;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--accent-cyan), #0099cc);
            color: #000;
            box-shadow: 0 4px 25px rgba(0, 229, 255, 0.25);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 40px rgba(0, 229, 255, 0.4);
        }

        .btn-secondary {
            background: var(--bg-card);
            color: var(--text-primary);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.08);
            transform: translateY(-3px);
            border-color: rgba(255, 255, 255, 0.2);
        }

        .btn svg {
            width: 20px;
            height: 20px;
        }

        /* Drum Visual */
        .drum-visual {
            display: flex;
            justify-content: center;
            gap: 20px;
            padding: 60px 0 40px;
            flex-wrap: wrap;
        }

        .drum-pad {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: 600;
            color: #000;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
            animation: drumFloat 3s ease-in-out infinite;
        }

        .drum-pad::after {
            content: '';
            position: absolute;
            inset: -4px;
            border-radius: 50%;
            border: 2px solid rgba(255, 255, 255, 0.15);
            transition: all 0.3s;
        }

        .drum-pad:hover {
            transform: scale(1.15);
        }

        .drum-pad:hover::after {
            inset: -10px;
            border-color: rgba(255, 255, 255, 0.3);
        }

        .drum-pad:nth-child(1) { background: #ffcc00; animation-delay: 0s; }
        .drum-pad:nth-child(2) { background: #00e5ff; animation-delay: 0.3s; }
        .drum-pad:nth-child(3) { background: #e040fb; animation-delay: 0.6s; }
        .drum-pad:nth-child(4) { background: #00ffaa; animation-delay: 0.9s; }
        .drum-pad:nth-child(5) { background: #ff6e40; animation-delay: 1.2s; }
        .drum-pad:nth-child(6) { background: #7c4dff; animation-delay: 1.5s; }
        .drum-pad:nth-child(7) { background: #ff4081; animation-delay: 1.8s; }

        @keyframes drumFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-8px); }
        }

        .drum-pad.hit {
            animation: drumHit 0.3s ease-out;
        }

        @keyframes drumHit {
            0% { transform: scale(1.3); box-shadow: 0 0 40px currentColor; }
            100% { transform: scale(1); box-shadow: none; }
        }

        /* Section */
        section {
            padding: 80px 0;
        }

        .section-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--accent-cyan);
            font-weight: 600;
            margin-bottom: 12px;
        }

        section h2 {
            font-size: 2.4rem;
            font-weight: 700;
            margin-bottom: 16px;
            letter-spacing: -1px;
        }

        section > .content > p {
            color: var(--text-secondary);
            font-size: 1.1rem;
            margin-bottom: 48px;
            max-width: 600px;
        }

        /* Feature cards */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }

        .feature-card {
            background: var(--bg-card);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 20px;
            padding: 36px 32px;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }

        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
            opacity: 0;
            transition: opacity 0.4s;
        }

        .feature-card:hover {
            background: rgba(255, 255, 255, 0.06);
            transform: translateY(-4px);
            border-color: rgba(255, 255, 255, 0.12);
        }

        .feature-card:hover::before {
            opacity: 1;
        }

        .feature-icon {
            font-size: 2.2rem;
            margin-bottom: 20px;
            display: block;
        }

        .feature-card h3 {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .feature-card p {
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.7;
        }

        /* How it works */
        .steps {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 32px;
            counter-reset: step;
        }

        .step {
            text-align: center;
            position: relative;
        }

        .step-number {
            width: 56px;
            height: 56px;
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(0, 229, 255, 0.15), rgba(224, 64, 251, 0.15));
            border: 1px solid rgba(0, 229, 255, 0.2);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--accent-cyan);
            margin-bottom: 20px;
        }

        .step h3 {
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .step p {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        /* Tech stack */
        .tech-pills {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
            margin-top: 32px;
        }

        .tech-pill {
            padding: 10px 22px;
            border-radius: 100px;
            background: var(--bg-card);
            border: 1px solid rgba(255, 255, 255, 0.08);
            font-size: 0.9rem;
            font-weight: 500;
            color: var(--text-secondary);
            transition: all 0.3s;
        }

        .tech-pill:hover {
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
            background: rgba(0, 229, 255, 0.05);
        }

        /* CTA section */
        .cta-section {
            text-align: center;
            padding: 80px 0 100px;
        }

        .cta-box {
            background: linear-gradient(135deg, rgba(0, 229, 255, 0.08), rgba(224, 64, 251, 0.08));
            border: 1px solid rgba(0, 229, 255, 0.15);
            border-radius: 28px;
            padding: 60px 40px;
        }

        .cta-box h2 {
            font-size: 2.2rem;
            margin-bottom: 16px;
        }

        .cta-box p {
            color: var(--text-secondary);
            font-size: 1.1rem;
            margin-bottom: 36px;
        }

        /* Footer */
        footer {
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            padding: 40px 0;
            text-align: center;
        }

        footer p {
            color: var(--text-secondary);
            font-size: 0.85rem;
        }

        footer a {
            color: var(--accent-cyan);
            text-decoration: none;
        }

        footer a:hover {
            text-decoration: underline;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero { padding: 60px 0 40px; }
            .hero h1 { font-size: 2.4rem; letter-spacing: -1px; }
            .nav-links { display: none; }
            .drum-pad { width: 70px; height: 70px; font-size: 0.65rem; }
            .features-grid { grid-template-columns: 1fr; }
            .cta-box { padding: 40px 24px; }
        }
    </style>
</head>
<body>
    <div class="bg-grid"></div>
    <div class="bg-glow cyan"></div>
    <div class="bg-glow magenta"></div>

    <div class="content">
        <nav>
            <div class="logo">🥁 Invisible Drum Kit</div>
            <div class="nav-links">
                <a href="#features">Features</a>
                <a href="#how-it-works">How It Works</a>
                <a href="#download">Download</a>
                <a href="https://github.com/abhinavkshabu/invisible-drumset" target="_blank">GitHub</a>
            </div>
        </nav>
    </div>

    <!-- Hero -->
    <section class="hero">
        <div class="content">
            <div class="badge">✨ AI-Powered Music</div>
            <h1>Play Drums<br><span class="gradient-text">In Thin Air</span></h1>
            <p>Use your hands as drumsticks. Our AI tracks your movements through your webcam and plays real drum sounds — no physical instrument needed.</p>
            <div class="hero-buttons">
                <a href="https://github.com/abhinavkshabu/invisible-drumset/archive/refs/heads/main.zip" class="btn btn-primary" id="download-btn">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
                    Download App
                </a>
                <a href="https://github.com/abhinavkshabu/invisible-drumset" target="_blank" class="btn btn-secondary" id="github-btn">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.605-.015 2.896-.015 3.286 0 .315.21.694.825.576C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12z"/></svg>
                    View Source
                </a>
            </div>
        </div>

        <!-- Drum pad visual -->
        <div class="drum-visual">
            <div class="drum-pad" onclick="hitDrum(this)">Crash</div>
            <div class="drum-pad" onclick="hitDrum(this)">Hi-Hat</div>
            <div class="drum-pad" onclick="hitDrum(this)">High Tom</div>
            <div class="drum-pad" onclick="hitDrum(this)">Snare</div>
            <div class="drum-pad" onclick="hitDrum(this)">Mid Tom</div>
            <div class="drum-pad" onclick="hitDrum(this)">Kick</div>
            <div class="drum-pad" onclick="hitDrum(this)">Floor Tom</div>
        </div>
    </section>

    <!-- Features -->
    <section id="features">
        <div class="content">
            <div class="section-label">Features</div>
            <h2>Why It's Awesome</h2>
            <p>Built with cutting-edge AI hand tracking for a magical drumming experience.</p>

            <div class="features-grid">
                <div class="feature-card">
                    <span class="feature-icon">🤖</span>
                    <h3>AI Hand Tracking</h3>
                    <p>MediaPipe detects your hand landmarks in real-time at 60 FPS. Just show your hands to the camera and start playing.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🎵</span>
                    <h3>8 Drum Sounds</h3>
                    <p>Kick, snare, hi-hat, crash, ride, high tom, mid tom, and floor tom — all synthesized in real-time with NumPy.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">👐</span>
                    <h3>Two-Hand Support</h3>
                    <p>Both hands are tracked simultaneously with independent strike detection — just like real drumming with two sticks.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">⚡</span>
                    <h3>Velocity Detection</h3>
                    <p>Flick your finger downward to strike. The motion tracking detects the speed and direction of your movement.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🎨</span>
                    <h3>Visual Feedback</h3>
                    <p>Color-coded drum pads, motion trails, hit animations, and a real-time HUD make the experience feel alive.</p>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🔄</span>
                    <h3>Autoplay Beat</h3>
                    <p>Press 'B' to toggle an automatic backing beat — perfect for jamming along or testing the system.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- How It Works -->
    <section id="how-it-works">
        <div class="content">
            <div class="section-label">How It Works</div>
            <h2>Get Started in 3 Steps</h2>
            <p>No special hardware needed. Just a computer with a webcam.</p>

            <div class="steps">
                <div class="step">
                    <div class="step-number">1</div>
                    <h3>Download & Install</h3>
                    <p>Download the project, install Python 3.10+, and run <code>pip install -r requirements.txt</code></p>
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    <h3>Launch the App</h3>
                    <p>Run <code>python app.py</code> and point your webcam at your hands.</p>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <h3>Start Drumming!</h3>
                    <p>Flick your index fingers downward over the drum pads to play. Rock on! 🤘</p>
                </div>
            </div>

            <!-- Tech stack -->
            <div style="text-align: center; margin-top: 64px;">
                <div class="section-label">Built With</div>
                <div class="tech-pills">
                    <span class="tech-pill">🐍 Python</span>
                    <span class="tech-pill">👁️ OpenCV</span>
                    <span class="tech-pill">🤖 MediaPipe</span>
                    <span class="tech-pill">🔢 NumPy</span>
                    <span class="tech-pill">🎮 Pygame</span>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA -->
    <section class="cta-section" id="download">
        <div class="content">
            <div class="cta-box">
                <h2>Ready to Drum? 🥁</h2>
                <p>Download the Invisible Drum Kit and start making music with nothing but your hands.</p>
                <div class="hero-buttons">
                    <a href="https://github.com/abhinavkshabu/invisible-drumset/archive/refs/heads/main.zip" class="btn btn-primary" id="cta-download-btn">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg>
                        Download Now — Free
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="content">
            <p>Made with ❤️ by <a href="https://github.com/abhinavkshabu" target="_blank">abhinavkshabu</a> · <a href="https://github.com/abhinavkshabu/invisible-drumset" target="_blank">View on GitHub</a></p>
        </div>
    </footer>

    <script>
        function hitDrum(el) {
            el.classList.remove('hit');
            void el.offsetWidth;
            el.classList.add('hit');
            setTimeout(() => el.classList.remove('hit'), 300);
        }

        // Smooth scroll for nav links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) target.scrollIntoView({ behavior: 'smooth' });
            });
        });

        // Intersection Observer for fade-in animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.feature-card, .step').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
    </script>
</body>
</html>
"""


class LauncherHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[WEB] {args[0]}")


with socketserver.TCPServer(("", PORT), LauncherHandler) as httpd:
    print(f"=== Invisible Drum Kit Website ===")
    print(f"Serving at http://0.0.0.0:{PORT}")
    httpd.serve_forever()
