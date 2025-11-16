import httpx

def test_regiser(register):
    url = "http://127.0.0.1:8000/api/v1/bookings/"
    headers = {
        "Authorization": "",
        "Content-Type": "application/json"
    }
    payload = {
        "username": "ogenna",
        "password": "0987poiu"
    }
    request = httpx.post(url, headers=headers)

    if request:
        return request.headers
    return False

if __name__ == "__main__":
    print(test_regiser("login"))
