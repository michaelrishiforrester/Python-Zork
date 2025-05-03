from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import pty
import os
import subprocess
import select
import termios
import struct
import fcntl
import signal

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store the ptty for the game process
game_fd = None
game_process = None

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")
    global game_process, game_fd
    if game_process:
        try:
            os.kill(game_process.pid, signal.SIGTERM)
        except:
            pass
        game_process = None
        game_fd = None

@socketio.on('terminal_input')
def handle_input(data):
    global game_fd
    if game_fd:
        os.write(game_fd, data['input'].encode())

@socketio.on('resize')
def handle_resize(data):
    global game_fd
    if game_fd:
        rows, cols = data['rows'], data['cols']
        try:
            fcntl.ioctl(game_fd, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))
        except Exception as e:
            print(f"Error resizing terminal: {e}")

@socketio.on('start_game')
def start_game():
    global game_fd, game_process
    
    # Close any existing game
    if game_process:
        try:
            os.kill(game_process.pid, signal.SIGTERM)
        except:
            pass
    
    # Start a new game
    game_fd, slave_fd = pty.openpty()
    game_process = subprocess.Popen(
        ["python", "main.py"],
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        start_new_session=True
    )
    
    os.close(slave_fd)
    
    # Set the pty to non-blocking mode
    fcntl.fcntl(game_fd, fcntl.F_SETFL, os.O_NONBLOCK)
    
    emit('game_started')
    
    # Start reading output
    socketio.start_background_task(read_output)

def read_output():
    global game_fd, game_process
    max_read_bytes = 1024 * 20
    
    while game_process and game_process.poll() is None:
        try:
            # Wait for data to be available
            r, w, e = select.select([game_fd], [], [], 0.1)
            if r:
                output = os.read(game_fd, max_read_bytes).decode(errors="ignore")
                if output:
                    socketio.emit('terminal_output', {'output': output})
        except (OSError, IOError) as e:
            print(f"Error reading from terminal: {e}")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
            
    # Check if the process has ended
    if game_process and game_process.poll() is not None:
        socketio.emit('game_ended', {'exit_code': game_process.returncode})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')