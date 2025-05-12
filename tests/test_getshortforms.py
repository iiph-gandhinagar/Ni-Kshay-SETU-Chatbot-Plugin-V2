import pandas as pd
from unittest.mock import patch

def test_get_short_forms_found(mocker):
    # Patch BEFORE importing the function
    fake_df = pd.DataFrame([{
        "title": "dvdms",
        "abbreviation": "DVDMS",
        "full_form": "Drug Vaccine Distribution Management System",
        "pattern1": "Drug Vaccine Distribution Management System",
    }])

    with patch("app.tasks.short_to_full_form.full_forms", return_value=fake_df):
        from app.tasks.short_to_full_form import get_short_forms  # Import happens inside the patch context
        result = get_short_forms("dvdms")
        assert result == ["Drug Vaccine Distribution Management System"]
