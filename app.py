from flask import Flask, request, jsonify

from geo.factor_builder import build_factors
from geo.arable_classifier import is_arable_land
from engine.rule_engine import evaluate_rules
from engine.erosion_risk_engine import compute_erosion_risk

RULES_FILE = "rules/icar_table_4_1_mechanical_measures.json"

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "ERROR",
            "message": "Invalid or missing JSON payload"
        }), 400

    lat = data.get("lat")
    lon = data.get("lon")
    land_use = data.get("land_use")

    if lat is None or lon is None or land_use is None:
        return jsonify({
            "status": "ERROR",
            "message": "lat, lon and land_use are required"
        }), 400

    # -----------------------------
    # Build factors (OBJECT)
    # -----------------------------
    factors = build_factors(
        lat=lat,
        lon=lon,
        land_use=land_use
    )

    # -----------------------------
    # Arability check (LOCKED)
    # -----------------------------
    is_arable, reason = is_arable_land(
        lat=lat,
        lon=lon,
        slope_percent=factors.slope_percent
    )

    if not is_arable:
        return jsonify({
            "status": "NON_ARABLE",
            "reason": reason,
            "message": "System works only for arable agricultural land",
            "input": {
                "lat": lat,
                "lon": lon,
                "land_use": land_use
            }
        }), 200

    # -----------------------------
    # ICAR rules
    # -----------------------------
    mechanical_measures = evaluate_rules(
    factors=factors,
    rule_file=RULES_FILE

    )

    # -----------------------------
    # Erosion risk (READ-ONLY)
    # -----------------------------
    erosion_risk = compute_erosion_risk({
        "rainfall_mm": factors.rainfall_mm,
        "slope_percent": factors.slope_percent,
        "soil_depth": factors.soil_depth,
        "drainage": factors.drainage
    })

    # -----------------------------
    # Final response (MANUAL SERIALIZATION)
    # -----------------------------
    return jsonify({
        "status": "OK",
        "input": {
            "lat": lat,
            "lon": lon,
            "land_use": land_use
        },
        "factors": {
            "rainfall_mm": factors.rainfall_mm,
            "slope_percent": factors.slope_percent,
            "soil_depth": factors.soil_depth,
            "drainage": factors.drainage,
            "land_use": land_use
        },
        "mechanical_measures": mechanical_measures,
        "erosion_risk": erosion_risk
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
