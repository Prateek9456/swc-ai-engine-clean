import os
import sys

# Ensure project root is on path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from geo.factor_builder import build_factors
from engine.rule_engine import recommend_mechanical_measures


def test_icar_pipeline_basic():
    """
    End-to-end ICAR DSS test.
    """

    factors = build_factors(
        lat=30.3165,
        lon=78.0322,
        land_use="SMALL_MILLETS",
        overrides={
            "rainfall": "HIGH",
            "slope": "STEEP",
            "soil_depth": "SHALLOW",
            "drainage": "POOR",
        },
    )

    factor_dict = factors.to_dict()

    assert factor_dict["rainfall"] == "HIGH"
    assert factor_dict["slope"] == "STEEP"
    assert factor_dict["soil_depth"] == "SHALLOW"
    assert factor_dict["drainage"] == "POOR"
    assert factor_dict["land_use"] == "SMALL_MILLETS"

    recommendation = recommend_mechanical_measures(factors)

    assert recommendation["recommendation_mode"] in {
        "STRICT_ICAR",
        "LAND_USE_IGNORED",
        "NO_MATCH",
    }
