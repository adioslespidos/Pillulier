from flask import Flask, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__)
DATA_FILE = "pillulier.json"

def charger_etat():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def sauvegarder_etat(etat):
    with open(DATA_FILE, "w") as f:
        json.dump(etat, f)

@app.route("/")
def index():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/get", methods=["GET"])
def get_pillulier():
    return jsonify(charger_etat())

@app.route("/toggle", methods=["POST"])
def toggle_pillule():
    data = request.json
    etat = charger_etat()
    key = f"{data['jour']}-{data['periode']}"
    etat[key] = not etat.get(key, False)
    sauvegarder_etat(etat)
    return jsonify({"success": True, "new_state": etat[key]})

@app.route("/reset", methods=["POST"])
def reset_pillulier():
    sauvegarder_etat({})
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
