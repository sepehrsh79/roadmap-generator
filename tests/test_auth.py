import asyncio
from typing import Any, Dict, List

import pytest
from httpx import AsyncClient, Response
from pyotp import TOTP


@pytest.mark.asyncio
class TestAuth:
    username = "string"
    password = "string"
    headers: Dict[str, str] | None = None
    access_token: Any = None
    refresh_token: Any = None
    gauth: Any = None

    @property
    def data(self):
        return {"username": TestAuth.username, "password": TestAuth.password}

    async def test_register(self, http_client: AsyncClient):
        response = await http_client.post("/auth/register", json=self.data)
        assert response.status_code == 200
        response_data = response.json()
        TestAuth.gauth = response_data.get("gauth")
        response = await http_client.post("/auth/register", json=self.data)
        assert response.status_code == 400

    async def test_login_not_registered_user(self, http_client: AsyncClient):
        corrupted_data = self.data.copy()
        corrupted_data["username"] = corrupted_data["username"] + "fake"
        response = await http_client.post("/auth/login", json=corrupted_data)
        assert response.status_code == 400

    async def test_login_not_verified_user(self, http_client: AsyncClient):
        response = await http_client.post("/auth/login", json=self.data)
        assert response.status_code == 200
        assert response.cookies.get("Refresh-Token") is not None

        response_data = response.json()
        TestAuth.access_token = response_data.get("access_token")
        TestAuth.refresh_token = response_data.get("refresh_token")

        http_client.cookies.update(
            {
                "Access-Token": TestAuth.access_token,
                "Refresh-Token": TestAuth.refresh_token,
            }
        )

    async def test_verify_user(self, http_client: AsyncClient):
        totp = TOTP(TestAuth.gauth)
        current_totp = totp.now()
        response = await http_client.post(
            f"/auth/verify?code={current_totp}",
            json={"refresh_token": TestAuth.refresh_token},
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data.get("message") == "user verify successfully"

    async def test_login_verified_user(self, http_client: AsyncClient):
        response = await http_client.post("/auth/login", json=self.data)
        assert response.status_code == 200
        assert response.cookies.get("Access-Token") is not None
        response_data = response.json()
        TestAuth.access_token = response_data.get("access_token")
        TestAuth.refresh_token = response_data.get("refresh_token")
        TestAuth.headers = {"Authorization": "Bearer " + TestAuth.access_token}
        http_client.cookies.update(
            {
                "Access-Token": TestAuth.access_token,
                "Refresh-Token": TestAuth.refresh_token,
            }
        )

    async def test_refresh_token(self, http_client: AsyncClient):
        response = await http_client.post(
            "/auth/refresh", json={"refresh_token": TestAuth.refresh_token}
        )
        assert response.status_code == 200
        response_data = response.json()
        new_access_token = response_data.get("access_token")
        new_refresh_token = response_data.get("refresh_token")
        assert new_access_token is not None
        assert new_refresh_token is not None

        TestAuth.headers = {"Authorization": "Bearer " + TestAuth.access_token}
        http_client.cookies.update(
            {"Access-Token": new_access_token, "Refresh-Token": new_refresh_token}
        )

    async def test_auth_and_tokens(self, http_client: AsyncClient):
        response = await http_client.get("/auth/me", headers=TestAuth.headers)
        assert response.status_code == 200
        assert TestAuth.username == response.json()["username"]

        bad_header = {"Authorization": "Bearer " + TestAuth.refresh_token}
        response = await http_client.get("/auth/me", headers=bad_header)
        assert response.status_code == 403

        bad_header = {"Authorization": TestAuth.access_token}
        response = await http_client.get("/auth/me", headers=bad_header)
        assert response.status_code == 403
