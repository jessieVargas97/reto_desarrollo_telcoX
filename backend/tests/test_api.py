import time

def test_health_ok(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.get_json()
    assert body["status"] == "ok"
    assert "time" in body

def test_list_consumption_returns_two(client):
    r = client.get("/api/consumption")
    assert r.status_code == 200
    body = r.get_json()
    assert "results" in body
    assert len(body["results"]) == 2
    item = body["results"][0]
    for k in ("msisdn", "name", "balance", "data_mb", "minutes", "updated_at"):
        assert k in item

def test_get_by_msisdn_found(client):
    r = client.get("/api/consumption", query_string={"msisdn": "593988877766"})
    assert r.status_code == 200
    b = r.get_json()
    assert b["msisdn"] == "593988877766"
    assert b["name"] == "Zoila Nicole Cueva"
    assert isinstance(b["balance"], (int, float))

def test_get_by_msisdn_not_found(client):
    r = client.get("/api/consumption", query_string={"msisdn": "000000000000"})
    assert r.status_code == 404
    assert "message" in r.get_json()

def test_simulate_partial_update_sets_fields(client):
    # update balance and minutes for the first msisdn
    payload = {
        "msisdn": "593988877766",
        "balance": 12.34,
        "minutes": 199
    }
    r = client.post("/api/consumption/simulate", json=payload)
    assert r.status_code == 200
    assert r.get_json()["updated"] == 1

    # test endpoint per msisdn
    r2 = client.get("/api/consumption", query_string={"msisdn": "593988877766"})
    assert r2.status_code == 200
    b = r2.get_json()
    assert b["balance"] == 12.34
    assert b["minutes"] == 199

def test_simulate_requires_msisdn_when_updating_fields(client):
    # validation fields without msisdn
    r = client.post("/api/consumption/simulate", json={"balance": 9.99})
    assert r.status_code == 400
    assert "msisdn" in r.get_json()["message"]

def test_simulate_random_single_client(client):
    
    before_result = client.get("/api/consumption", query_string={"msisdn": "593987651234"}).get_json()
    # simulate only for that msisdn (no fields -> random mode, filtered)
    r = client.post("/api/consumption/simulate", json={"msisdn": "593987651234"})
    assert r.status_code == 200
    assert r.get_json()["updated"] == 1

    after_result = client.get("/api/consumption", query_string={"msisdn": "593987651234"}).get_json()
    assert after_result["msisdn"] == before["msisdn"]
    assert after_result["balance"] >= 0.0
    assert after_result["data_mb"] >= 0.0
    assert after_result["minutes"] >= 0
    assert after_result["updated_at"] != before["updated_at"]
