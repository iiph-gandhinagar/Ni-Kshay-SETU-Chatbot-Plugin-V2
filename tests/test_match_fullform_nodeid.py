import pandas as pd
from unittest.mock import patch

def test_match_full_form_with_node_id(mocker):
    full_forms = ["Tuberculosis", "DOTS"]

    fake_df = pd.DataFrame([
        {"node_title": "Tuberculosis is a serious disease", "node_id": "N1"},
        {"node_title": "Introduction to DOTS treatment", "node_id": "N2"},
        {"node_title": "Random text", "node_id": "N3"}
    ])

    with patch("app.tasks.short_to_full_form.full_forms", return_value=fake_df):
        from app.tasks.short_to_full_form import match_full_form_with_node_id  # Import happens inside the patch context
        result = match_full_form_with_node_id(full_forms, fake_df)
        assert isinstance(result, list)  # ✅ First, make sure it's a list
        assert set(result) == {"N1", "N2"}
