from unittest.mock import patch
import pandas as pd
from app.ordering.first_ordering import first_ordering

def test_first_ordering_sorting_logic():
    # Inputs
    unique_node_ids = ["N2", "N1"]
    query = "TB treatment"

    df = pd.DataFrame([
        {"node_id": "N1", "node_title": "Introduction to TB"},
        {"node_id": "N2", "node_title": "TB treatment protocol"},
    ])

    with patch("app.ordering.first_ordering.extract_intent_keywords", return_value=["TB", "treatment"]), \
         patch("app.ordering.first_ordering.score_relevance") as mock_score_relevance:

        # Mock the relevance score manually
        def side_effect(title, keywords):
            if "protocol" in title:
                return 0.9
            return 0.4

        mock_score_relevance.side_effect = side_effect

        result = first_ordering(unique_node_ids, query, df)

        # Should return node_ids sorted by score: N2 (0.9), then N1 (0.4)
        assert result == ["N2", "N1"]
