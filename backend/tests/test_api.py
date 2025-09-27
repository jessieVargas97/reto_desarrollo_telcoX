import os, requests
API = os.getenv("API_URL", "http://localhost:8000/api")

def test_health():
    r = requests.get(API.replace("/api", "") + "/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_consumption_not_found():
    r = requests.get(f"{API}/consumption", params={"msisdn": "000"})
    assert r.status_code in (404, 500)