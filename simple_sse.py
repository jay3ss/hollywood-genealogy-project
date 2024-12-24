import http.server
import threading
import time

# A simple HTTP server to serve an SSE endpoint and a basic web page.
class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the web page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <!DOCTYPE html>
                <html>
                <body>
                    <h1>Streaming Updates</h1>
                    <div id="output"></div>
                    <script>
                        const output = document.getElementById('output');
                        const eventSource = new EventSource('/stream');
                        eventSource.onmessage = function(event) {
                            const div = document.createElement('div');
                            div.textContent = event.data;
                            output.appendChild(div);
                        };
                    </script>
                </body>
                </html>
            """)
        elif self.path == '/stream':
            # Stream updates via SSE
            self.send_response(200)
            self.send_header('Content-type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()

            # Stream updates continuously
            for i in range(1, 11):  # Example: Stream 10 messages
                time.sleep(1)  # Simulate work
                message = f"Update {i}\n"
                self.wfile.write(f"data: {message}\n\n".encode('utf-8'))
                self.wfile.flush()

            # Close the connection after streaming
            return
        else:
            self.send_error(404)

# Run the server
def run_server():
    server = http.server.HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    print("Serving on http://localhost:8000")
    server.serve_forever()

# Run the server in a separate thread
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nServer stopped.")

