from flask import Flask, request, jsonify
import traceback
import os

from geo.factor_builder import build_factors
from geo.arable_classifier import is_arable_land
from engine.rule_engine import evaluate_rules
from engine.erosion_risk_engine import compute_erosion_risk

app = Flask(__name__)

# --------------------------------------------------
# Paths (ICAR rule table)
# --------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
ICAR_RULE_FILE = os.path.join(
    BASE_DIR,
    "rules",
    "icar_table_4_1_mechanical_measures.json"
)

# --------------------------------------------------
# Health check
# --------------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200


# --------------------------------------------------
# Main DSS endpoint
# --------------------------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(force=True)

        lat = data.get("lat")
        lon = data.get("lon")
        land_use = data.get("land_use")

        if lat is None or lon is None or land_use is None:
            return jsonify({
                "status": "ERROR",
                "message": "Required fields: lat, lon, land_use"
            }), 400

        # --------------------------------------------------
        # 1. Build raw geophysical factors
        # --------------------------------------------------
        factors = build_factors(lat, lon, land_use)

        # --------------------------------------------------
        # 2. ICAR arability check (LOCKED LOGIC)
        # --------------------------------------------------
        is_arable, reason = is_arable_land(
            lat=factors.latitude,
            lon=factors.longitude,
            slope_percent=factors.slope_percent
        )

        if not is_arable:
            return jsonify({
                "status": "NON_ARABLE",
                "reason": reason,
                "message": "System works only for arable agricultural land"
            }), 200

        # --------------------------------------------------
        # 3. Apply ICAR mechanical rules (Table 4.1)
        # --------------------------------------------------
        rule_result = evaluate_rules(
            factors=factors,
            rule_file=ICAR_RULE_FILE
        )

        mode = rule_result["mode"]
        measures = rule_result["measures"]

        # --------------------------------------------------
        # 4. Compute erosion risk
        # --------------------------------------------------
        erosion_risk = compute_erosion_risk(factors)

        # --------------------------------------------------
        # 5. Final DSS response
        # --------------------------------------------------
        return jsonify({
            "status": "OK",
            "mode": mode,
            "arability": "ARABLE",
            "location": {
                "latitude": factors.latitude,
                "longitude": factors.longitude
            },
            "land_use": factors.land_use,
            "factors": {
                "slope_percent": factors.slope_percent,
                "rainfall_mm": factors.rainfall_mm,
                "soil_depth": factors.soil_depth,
                "drainage": factors.drainage
            },
            "erosion_risk": erosion_risk,
            "recommended_measures": measures
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "status": "ERROR",
            "error": str(e)
        }), 500


# --------------------------------------------------
# Render-safe entry point
# --------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
