from flask import Flask, abort, make_response, render_template, request

app = Flask(__name__)

# Render the welcome screen. This should ask for a voter ID.
@app.route("/")
def index():
    return render_template("index.html", placeholder=DEFAULT_REQ)

# Render the voting options
@app.route("/vote")
def show_candidates():
    return render_template("candidates.html")


# Submit vote. This is only set up for single option voting. #MURICA
@app.route("/vote", methods=["POST"])
def send():
    # Get the votes from the json.
    req = request.form.get("requestBox") # TODO

    if req is None:
        return abort(
            400, "No requestBox value found in POST data. You need to submit a request!"
        )

    # I don't know what this request is. Break.
    if req == "":
        return abort(
            400, "No requestBox value found in POST data. You need to submit a request!" # TODO Throw a useful error
        )

    # Save the response to the CSV
    with open('votes.csv', 'a') as csvfile:
        csvfile.write(voter_id, vote)

    # Return a response to the application
    response = make_response() # TODO

    return response


# Main func
if __name__ == "__main__":
    app.run(debug=True, port=5001)
