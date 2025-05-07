#!/usr/bin/env python3
import os
import secrets

import requests
from flask import Flask, request, redirect, abort

app = Flask(__name__)

# Configure these in your environment
API_BASE_URL = os.getenv("ANYTHINGLLM_BASE_URL", "http://anythingllm:3001")
API_TOKEN = os.environ["ANYTHINGLLM_API_TOKEN"]  # your admin API key

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

def get_user_by_email(email: str):
    """Check existing users via the admin endpoint."""
    resp = requests.get(f"{API_BASE_URL}/api/v1/admin/users", headers=HEADERS)
    resp.raise_for_status()
    users = resp.json().get("users", [])
    return next((u for u in users if u.get("username") == email), None)

def create_user(email: str):
    payload = {
        "username": email,
        "password": secrets.token_urlsafe(16),
        "role": "default"
    }
    resp = requests.post(f"{API_BASE_URL}/api/v1/admin/users/new", json=payload, headers=HEADERS)
    resp.raise_for_status()
    user = resp.json()["user"]

    # 1) Add to “shared” workspace
    add_to_shared_resp = requests.post(
        f"{API_BASE_URL}/api/v1/admin/workspaces/shared/manage-users",
        json={"userIds": [user["id"]]},
        headers=HEADERS
    )
    add_to_shared_resp.raise_for_status()

    # 2) Create a new personal workspace for them
    create_new_ws_resp = requests.post(
        f"{API_BASE_URL}/api/v1/workspace/new",
        json={"name": f"{email.replace(".", "-")}"},
        headers=HEADERS
    )
    create_new_ws_resp.raise_for_status()
    new_ws_slug = create_new_ws_resp.json()["workspace"]["slug"]
    app.logger.warning(new_ws_slug)

    # 3) Add user to own personal workspace
    add_to_personal_resp = requests.post(
        f"{API_BASE_URL}/api/v1/admin/workspaces/{new_ws_slug}/manage-users",
        json={"userIds": [user["id"]]},
        headers=HEADERS
    )
    add_to_personal_resp.raise_for_status()
    app.logger.warning(add_to_personal_resp.json())

    return user

def issue_token(user_id: int):
    """Issue a one-time auth token and get back the login path."""
    resp = requests.get(f"{API_BASE_URL}/api/v1/users/{user_id}/issue-auth-token", headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    return data["loginPath"]

@app.route("/", methods=["GET"])
def sso_login():
    # 1. Extract email from header
    email = request.headers.get("X-Token-User-Email")
    if not email:
        abort(400, "Missing X-Token-User-Email header")
    email = email.split("@")[0]

    # 2. Lookup or create user
    user = get_user_by_email(email)
    if user:
        user_id = user["id"]
    else:
        user = create_user(email)
        user_id = user["id"]

    # 3. Issue auth token & build redirect URL
    login_path = issue_token(user_id)
    return redirect(login_path, code=302)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
