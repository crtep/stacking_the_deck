import http.server
import socketserver
import json
import time
import random
import sys

from game import run_game

# Data to be updated
data = {"v_numbers": [], "vc_numbers": [], "vc_indices": [], "outcome": "", "win_indices": [], "chooser_name": "", "arranger_name": ""}

# Custom handler to serve HTML and respond to updates
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args):
        pass  # Suppress logging

    def do_GET(self):
        if self.path == "/data":  # Endpoint for data updates
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:  # Serve HTML for other requests
            super().do_GET()

def update_data_periodically():
    """Update data periodically in the background."""
    if len(sys.argv) < 4:
        while True:
            try:
                inp = input("Program names: ")
                if inp == "a": # again
                    fnames = [fnames[0], fnames[1]]                
                if inp == "s": # swap
                    fnames = [fnames[1], fnames[0]]
                else:
                    fnames = inp.split()
                data["chooser_name"] = f"({fnames[0]})"
                data["arranger_name"] = f"({fnames[1]})"

                run_game(8, int(sys.argv[1]), fnames[0], fnames[1], data)
            except IndexError:
                print("Usage: <chooser> <arranger>")
                pass

    else:
        run_game(8, int(sys.argv[1]), sys.argv[2], sys.argv[3], data)

# Run the server and update loop
if __name__ == "__main__":
    import threading
    PORT = 8000
    # Start the periodic update in a separate thread
    threading.Thread(target=update_data_periodically, daemon=True).start()
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            httpd.server_close()
