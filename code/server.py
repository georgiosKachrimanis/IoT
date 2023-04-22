from flask import Flask, request

app = Flask(__name__)

@app.route('/start_camera', methods=['POST'])
def start_camera():
    # Code to start camera recording goes here
    return 'Camera recording started'

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    # Code to stop camera recording goes here
    return 'Camera recording stopped'

@app.route('/')
def home():
    return """
        <h1>Camera Control</h1>
        <form action="/start_camera" method="POST">
            <input type="submit" value="Start Camera">
        </form>
        <form action="/stop_camera" method="POST">
            <input type="submit" value="Stop Camera">
        </form>
    """

# Start the server on all network interfaces
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
