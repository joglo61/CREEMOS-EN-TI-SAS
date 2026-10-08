def test_dashboard(client):
    r = client.get("/api/v1/dashboard")
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
