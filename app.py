from flask import Flask, request, jsonify
import traceback

# Core system import (UNCHANGED)
from geo.factor_builder import build_factors

app = Flask(__name__)

# -------------------------------------------------------------------
# Health check endpoint (SAFE, OPTIONAL, NO LOGIC CHANGE)
# -------------------------------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "UP",
        "service": "SWC AI Engine"
    }), 200


# -------------------------------------------------------------------
# Main analysis endpoint
# -------------------------------------------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # -------------------------------
        # 1. Read input JSON
        # -------------------------------
        data = request.get_json(force=True)

        if not data:
            return jsonify({
                "status": "ERROR",
                "message": "Empty JSON body"
            }), 400

        # -------------------------------
        # 2. Build factors (CORE LOGIC)
        # -------------------------------
        result = build_factors(data)

        # -------------------------------
        # 3. Return result
        # -------------------------------
        return jsonify(result), 200

    except Exception as e:
        # -------------------------------
        # 4. FULL TRACEBACK LOGGING
        # -------------------------------
        traceback.print_exc()

        return jsonify({
            "status": "ERROR",
            "error": str(e)
        }), 500


# -------------------------------------------------------------------
# Application entry point (RENDER SAFE)
# -------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
