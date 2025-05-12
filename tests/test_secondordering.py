import pandas as pd
from app.ordering.second_ordering import second_ordering

def test_second_ordering_prioritizes_cadre_ids():
    # Inputs
    first_ordering_node_ids = ["N3", "N1", "N2"]
    cadre = 3

    # Fake DataFrame
    df = pd.DataFrame([
        {"node_id": "N1", "cadre_id": "3,5"},  # ✅ Should be prioritized
        {"node_id": "N2", "cadre_id": "4"},    # ❌ Not matching
        {"node_id": "N3", "cadre_id": ""}      # ❌ Empty
    ])

    result = second_ordering(first_ordering_node_ids, cadre, df)

    # Expected: N1 first because it matches cadre, followed by the rest in original order
    assert result == ["N1", "N3", "N2"]
