import httpx
import pytest


@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "pepe10121",
        "email": "pepe@platzi.com",
        "password": "pepe2109",
        "image": "http://image.com"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    test_response = {"message": "User created succesfully."}

    response = await default_client.post("/users/signup",
                                         json=payload,
                                         headers=headers)
    print(response.json().get("detail"))
    assert response.status_code == 201
    assert response.json() == test_response
