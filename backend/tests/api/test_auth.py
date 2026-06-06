async def test_register_login_and_me(client) -> None:
    register = await client.post(
        "/auth/register",
        json={"email": "auth-api@exemplo.com", "password": "senhaSegura123"},
    )
    assert register.status_code == 201

    login = await client.post(
        "/auth/jwt/login",
        data={"username": "auth-api@exemplo.com", "password": "senhaSegura123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = await client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "auth-api@exemplo.com"


async def test_me_without_token_returns_401(client) -> None:
    response = await client.get("/users/me")
    assert response.status_code == 401
