import http.server
import socketserver
import subprocess
import os

PORT = 8000

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Drum Kit Launcher</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #1e1e1e;
            color: white;
            margin: 0;
        }
        .container {
            text-align: center;
        }
        button {
            padding: 15px 30px;
            font-size: 24px;
            background-color: #00ffaa;
            color: #1e1e1e;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: background-color 0.3s;
            font-weight: bold;
        }
        button:hover {
            background-color: #00cc88;
        }
        p#status {
            margin-top: 20px;
            font-size: 18px;
            color: #aaaaaa;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Invisible Drum Kit</h1>
        <button id="startBtn" onclick="startApp()">Start AI Drum Kit</button>
        <p id="status">Ready to play!</p>
    </div>

    <script>
        function startApp() {
            document.getElementById('status').innerText = 'Starting... Check your desktop!';
            document.getElementById('startBtn').disabled = true;
            document.getElementById('startBtn').style.backgroundColor = '#555';
            
            fetch('/start', { method: 'POST' })
                .then(response => {
                    if (response.ok) {
                        document.getElementById('status').innerText = 'App is running!';
                        setTimeout(() => {
                            document.getElementById('startBtn').disabled = false;
                            document.getElementById('startBtn').style.backgroundColor = '#00ffaa';
                            document.getElementById('status').innerText = 'Ready to play again!';
                        }, 5000);
                    } else {
                        document.getElementById('status').innerText = 'Failed to start the app.';
                    }
                })
                .catch(err => {
                    document.getElementById('status').innerText = 'Error connecting to launcher.';
                });
        }
    </script>
</body>
</html>
"""

class LauncherHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/start':
            print("Starting app.py...")
            subprocess.Popen(["python", "app.py"])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Started")

with socketserver.TCPServer(("", PORT), LauncherHandler) as httpd:
    print(f"Launcher serving at http://localhost:{PORT}")
    print("Open this link in your browser to launch the app.")
    httpd.serve_forever()
