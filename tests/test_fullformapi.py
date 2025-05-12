import os# tests/test_fullform_api.py

import pandas as pd
from app.tasks.full_form_api import full_forms

def test_full_forms_success(mocker):
    # Sample fake JSON response structure
    fake_json_response = {
        "data": [
            {
                "_id": "1",
                "abbreviation": "TB",
                "full_form": "Tuberculosis",
                "patterns": ["T.B.", "T B"],
                "createdAt": "2023-01-01T00:00:00Z",
                "updatedAt": "2023-01-01T00:00:00Z",
                "__v": 0
            }
        ]
    }

    # Create a mock response object
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_json_response

    # Patch requests.get to return this mock
    mocker.patch("app.tasks.full_form_api.requests.get", return_value=mock_response)

    # Call your actual function
    df = full_forms()

    # Assert it's a DataFrame and has the expected columns
    assert isinstance(df, pd.DataFrame)
    assert "abbreviation" in df.columns
    assert "full_form" in df.columns
    assert "pattern1" in df.columns
    assert "pattern2" in df.columns




