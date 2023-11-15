from flask import Flask, abort, make_response, render_template, request, url_for, redirect
import csv

def validate_voter_id(voter_id):
    try:
        vid = int(voter_id)
        return voter_id
    except Exception as e:
        raise e

def startup():
    with open('votes.csv', 'w') as fh:
        fh.write("Voter_ID, Preferred Candidate\n")


app = Flask(__name__)
app.before_request_funcs = [(None, startup())]


# Render the welcome screen. This should ask for a voter ID.
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        # Get the votes from the json.
        req = request.form["voter_id"]

        # I don't know what this request is. Break.
        if req is None:
            return abort(
                400, "No voter_id key found in request."
            )

        try:
            voter_id = validate_voter_id(req)
            return redirect(url_for('show_candidates', voter_id=voter_id))
        except Exception as e:
            return abort(
                400, "Voter ID not accepted."
            )

# Render the voting options
@app.route("/show_candidates/<voter_id>")
def show_candidates(voter_id):
    return render_template("candidates.html", voter_id=voter_id)


# Thank the user
@app.route("/thanks")
def thanks():
    return render_template("thanks.html")


# Submit vote. This is only set up for single option voting. #MURICA
@app.route("/vote", methods=["POST"])
def vote():
    # Get the votes from the json.
    req = request.json.get("candidate_name")
    voter_id = request.json.get("voter_id")

    # I don't know what this request is. Break.
    if req is None or voter_id is None:
        return abort(
            400, "No candidate_name or voter_id key found in request."
        )

    if req == "" or voter_id == "":
        return abort(
            400, "No value for candidate_name or voter_id."
        )

    try:
        vid = validate_voter_id(voter_id)
    except Exception as e:
        return abort(
            400, "Invalid voter_id."
        )

    # Save the response to the CSV
    with open('votes.csv', 'a') as csvfile:
        csvfile.write("%s, %s\n" % (voter_id, req))

    # Return a response to the application
    response = make_response("OK")
    response.mime_type = "text/json"

    return response

# This is meant to generate the final CSV used for sending to a central location to tally votes
@app.route("/culminate", methods=["POST"])
def culminate():
    with open('votes.csv', 'r') as votescsv:
        # Read all the votes and tally up the results
        candidates = {}
        csvreader = csv.reader(votescsv)
        headerRow = True

        for vote in csvreader:
            if headerRow:
                headerRow = False
                continue
            if vote[1] in candidates:
                candidates[vote[1]] += 1
            else:
                candidates[vote[1]] = 1

        with open('totals.csv', 'w') as totalscsv:
            # Write vote tallies to CSV
            for candidate in candidates: # TODO Sort the candidates
                totalscsv.write("%s, %s\n" % (candidate,candidates[candidate]))

    return "OK"


# Main func
if __name__ == "__main__":

    app.run(debug=True, port=5001)
