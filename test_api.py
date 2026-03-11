import requests
import time
import concurrent.futures

BASE_URL = "http://localhost:8000"
API_KEY = "LT-vwH99lXG0rRg-gD6S8QuIui0Bw6iM4nJbIKQHydo" # Must match what's in your .env

def test_health():
    print("Testing /health...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Result: {response.json()} | Status: {response.status_code}")

def test_generate_fail():
    print("\nTesting /generate (Wrong Key)...")
    headers = {"X-API-KEY": "wrong-key"}
    response = requests.post(f"{BASE_URL}/generate", json={"prompt": "Hello"}, headers=headers)
    print(f"Result: {response.json()} | Status: {response.status_code} (Should be 403)")

def test_generate_success():
    print("\nTesting /generate (Correct Key)...")
    headers = {"X-API-KEY": API_KEY}
    payload = {"prompt": "The capital of France is", "max_new_tokens": 10}
    response = requests.post(f"{BASE_URL}/generate", json=payload, headers=headers)
    print(f"Result: {response.json()} | Status: {response.status_code}")

def send_request(_):
    headers = {"X-API-KEY": API_KEY}
    requests.post(f"{BASE_URL}/generate", json={"prompt": "Short test"}, headers=headers)
    return True

def test_concurrency():
    print("\nTesting Concurrency (5 simultaneous requests)...")
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(send_request, range(5)))
    end = time.time()
    print(f"Finished 5 requests in {end - start:.2f} seconds. Service is stable!")

if __name__ == "__main__":
    test_health()
    test_generate_fail()
    test_generate_success()
    test_concurrency()