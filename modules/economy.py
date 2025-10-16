import json
from typing import Dict
USERS_FILE = "users.json"

def load_users() -> Dict:
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(u: Dict):
    with open(USERS_FILE, "w") as f:
        json.dump(u, f, indent=2)

def ensure_user(u: Dict, uid: str):
    if uid not in u:
        u[uid] = {"paid": False, "banned": False, "balance": 0, "ref": None}
    return u

def credit_balance(uid: str, amount: int):
    u = load_users()
    ensure_user(u, uid)
    u[uid]["balance"] += amount
    save_users(u)

def spend_balance(uid: str, amount: int) -> bool:
    u = load_users()
    ensure_user(u, uid)
    if u[uid]["balance"] >= amount:
        u[uid]["balance"] -= amount
        save_users(u)
        return True
    return False
