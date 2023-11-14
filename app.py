import socket

from flask import Flask, abort, make_response, render_template, request

from pyquocca import get_flag

app = Flask(__name__)

KB = ("kb", 5000)
# KB doesn't have access to the student's username, so if KB sends back this, we replace it with a flag from flaganizer.
FLAGS = [
    "FLAG{REPLACE_ME_91273891273891278397123}",
    "FLAG{REPLACE_ME_12409785870107150782350}",
    "FLAG{REPLACE_ME_68979026908360930503094}"
]
DEFAULT_REQ = """GET / HTTP/1.1
Host: kb.quoccabank.com
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: http://haas.quoccabank.com/
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
Origin: http://haas.quoccabank.com
Connection: keep-alive

"""


@app.route("/")
def index():
    return render_template("index.html", placeholder=DEFAULT_REQ)


@app.route("/", methods=["POST"])
def send():
    req = request.form.get("requestBox")
    if req is None:
        return abort(
            400, "No requestBox value found in POST data. You need to submit a request!"
        )

    if req == "":
        req = DEFAULT_REQ

    # Send payload to kb.quoccabank.com
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(KB)
    sock.send(req.encode("utf-8"))

    # Return the output
    received = sock.recv(4096) + sock.recv(4096)  # Headers
    sock.close()

    text = received.decode()
    if FLAGS[0] in text:
        text = text.replace(FLAGS[0], get_flag('haas_simple'))
    elif FLAGS[1] in text:
        text = text.replace(FLAGS[1], get_flag('haas_deep'))
    elif FLAGS[2] in text:
        text = text.replace(FLAGS[2], get_flag('haas_calculator'))

    response = make_response(text)
    response.mimetype = "text/plain"

    return response


if __name__ == "__main__":
    app.run(debug=True, port=5001)
