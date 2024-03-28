from wsgiref.validate import validator

import pytest
import requests
from typing import List, Optional
from pydantic import BaseModel, ValidationError


class ApiResponse(BaseModel):
    isSuccess: bool
    errorCode: int
    errorMessage: Optional[str] = None
    idList: List[int]


@pytest.mark.parametrize("gender", ["male", "female", "any"])
def test_get_users_by_different_gender(gender):
    url = f'https://hr-challenge.dev.tapyou.com/api/test/users?gender={gender}'
    response = requests.get(url)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    json_data = response.json()
    print(json_data)

    # Validate JSON data against ApiResponse model
    try:
        response_model = ApiResponse(**json_data)
        assert response_model.isSuccess is True
        assert response_model.errorCode == 0
        assert response_model.errorMessage is None
        print("Validation successful!")
    except ValidationError as e:
        print(f"Validation error: {e}")


