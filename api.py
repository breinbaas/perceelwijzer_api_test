from cProfile import run
import requests


from api_secrets import URL, AUTH_BEARER


def run_query(query):
    headers = {"Authorization": f"Bearer {AUTH_BEARER}"}
    request = requests.post(URL, json={"query": query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(f"Unexpected status code returned: {request.status_code}")


def get_plots_nearby(lat: float, lon: float, distance: int = 5000):
    q = f"query {{plotsNearby(lat: {lat}, long: {lon}, distance: {distance}) {{nodes{{cropName, geometry}}}}}}"
    r = run_query(q)
    return r["data"]["plotsNearby"]["nodes"]


# small test
if __name__ == "__main__":
    data = get_plots_nearby(51.68407641, 5.289870262)
    print(data)
