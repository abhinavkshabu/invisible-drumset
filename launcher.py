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
    <title>Invisible Drum Kit</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #111;
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            text-align: center;
        }
        .box {
            max-width: 500px;
            padding: 40px;
        }
        h1 { font-size: 2rem; margin-bottom: 10px; }
        p { color: #aaa; margin-bottom: 30px; }
        a.btn {
            display: inline-block;
            padding: 14px 28px;
            background: #00e5ff;
            color: #000;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 1rem;
        }
        a.btn:hover { background: #00b8d4; }
        .github { margin-top: 20px; }
        .github a { color: #00e5ff; text-decoration: none; }
        .github a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="box">
        <h1>Invisible Drum Kit</h1>
        <p>Play drums in the air using AI hand tracking. Download and run on your computer with a webcam.</p>
        <a class="btn" href="https://github.com/abhinavkshabu/invisible-drumset/archive/refs/heads/main.zip">Download App</a>
        <div class="github">
            <a href="https://github.com/abhinavkshabu/invisible-drumset" target="_blank">View on GitHub</a>
        </div>
    </div>
</body>
</html>
"""


class LauncherHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode('utf-8'))


with socketserver.TCPServer(("", PORT), LauncherHandler) as httpd:
    print(f"Serving at http://0.0.0.0:{PORT}")
    httpd.serve_forever()
