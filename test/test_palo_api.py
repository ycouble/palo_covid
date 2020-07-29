import requests

import pytest

URL = "http://127.0.0.1:5000"

@pytest.mark.parametrize(
    "endpoint", [
        "/", 
        "/covid", 
        "/covid/datasets",
        "/covid/countries/France", 
        "/covid/countries/France/latest",
        "/covid/countries/France/2020-21-02",
        "/covid/countries/France/2000-21-02",
        "/covid/world", 
        "/covid/world/latest",
        "/covid/world/2020-21-02",
        "/covid/world/2000-21-02",
    ]
)
def test_should_200_ok(endpoint):
    resp = requests.get(f"{URL}{endpoint}")
    assert (resp.status_code == 200)
