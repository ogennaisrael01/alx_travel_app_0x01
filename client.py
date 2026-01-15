import requests

def test_regiser():
    url = "https://api.chapa.co/v1/transaction/verify/chewatatest-6669"
    payload = ''
    headers = {
      'Authorization': 'Bearer '
  }
    response = requests.get(url, headers=headers, data=payload)
    data = response.text
    print(data)
if __name__ == "__main__":
    test_regiser()