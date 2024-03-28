import pytest
import requests

from pydantic import BaseModel
from pydantic import ValidationError
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    gender: str
    age: int
    city: str
    registrationDate: str


class ApiResponse(BaseModel):
    errorCode: int
    errorMessage: Optional[str] = None
    isSuccess: bool
    result: Optional[User] = None


BASE_URL = 'https://hr-challenge.dev.tapyou.com/api/test/user/'


@pytest.mark.parametrize("id_param", [0, 10, 'ugf'])
def test_get_user_by_id(id_param):
    response = requests.get(f'{BASE_URL}/{id_param}')

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    json_data = response.json()

    # Validate the JSON data structure and data types using Pydantic
    try:
        response_model = ApiResponse(**json_data)
        assert response_model.isSuccess is True
        assert response_model.errorCode == 0
        assert response_model.errorMessage is None
        print("Validation successful!")

    except ValidationError as e:
        print(f"Validation error: {e}")
