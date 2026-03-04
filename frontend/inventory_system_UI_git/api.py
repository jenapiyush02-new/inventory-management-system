import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BACKEND_URL")


def login(username, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": username, "password": password},
    )
    return response


def get_warehouses(token):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(f"{BASE_URL}/items/warehouse", headers=headers)


def get_inventory(token, warehouse_id):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(
        f"{BASE_URL}/items/warehouse/{warehouse_id}",
        headers=headers,
    )


def update_stock(token, payload):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.post(
        f"{BASE_URL}/items/stock",
        headers=headers,
        json=payload,
    )
    
def safe_json(response):
    try:
        return response.json()
    except:
        return {"error": response.text}