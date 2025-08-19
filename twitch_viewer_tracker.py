import time
import json
import datetime as dt
import requests

CLIENT_ID = "<CLIENT-ID>"
CLIENT_SECRET = "<CLIENT_SECRET"
USER_ID = "USER_ID"
ACCESS_TOKEN = "ACCESS_TOKEN"
REFRESH_TOKEN = "REFRESH_TOKEN"

BASE = "https://api.twitch.tv/helix"

def HEADERS(token):
    return {"Client-Id": CLIENT_ID, "Authorization": f"Bearer {token}"}

def refresh_token():
    global ACCESS_TOKEN, REFRESH_TOKEN
    r = requests.post(
        "https://id.twitch.tv/oauth2/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )
    r.raise_for_status()
    tok = r.json()
    ACCESS_TOKEN = tok["access_token"]
    REFRESH_TOKEN = tok.get("refresh_token", REFRESH_TOKEN)

def get_chatters_page(after=None, first=1000):
    params = {"broadcaster_id": USER_ID, "moderator_id": USER_ID, "first": first}
    if after:
        params["after"] = after
    r = requests.get(f"{BASE}/chat/chatters", headers=HEADERS(ACCESS_TOKEN), params=params)
    if r.status_code == 401:  
        refresh_token()
        r = requests.get(f"{BASE}/chat/chatters", headers=HEADERS(ACCESS_TOKEN), params=params)
    r.raise_for_status()
    return r.json()

def snapshot_all_chatters():
    seen = []
    after = None
    while True:
        data = get_chatters_page(after)
        seen.extend(data.get("data", []))
        after = data.get("pagination", {}).get("cursor")
        if not after:
            break
    return seen

def poll_until_stop(interval_sec=60):
    outfile = f"chatters_{dt.date.today().isoformat()}.jsonl"
    index = {}
    try:
        while True:
            start = time.time()
            chatters = snapshot_all_chatters()
            now = dt.datetime.now(dt.timezone.utc).isoformat()
            for u in chatters:
                uid = u["user_id"]
                rec = index.get(
                    uid,
                    {"user_id": uid, "user_login": u["user_login"], "first_seen": now, "last_seen": now}
                )
                rec["last_seen"] = now
                index[uid] = rec
            with open(outfile, "a", encoding="utf-8") as f:
                f.write(json.dumps({"ts": now, "count": len(chatters)}) + "\n")
            elapsed = time.time() - start
            time.sleep(max(0, interval_sec - elapsed))
    except KeyboardInterrupt:
        print("\nManual stop detected. Saving final roster...")

    
    roster_file = outfile.replace(".jsonl", "_roster.json")
    with open(roster_file, "w", encoding="utf-8") as f:
        json.dump(sorted(index.values(), key=lambda x: x["user_login"].lower()), f, indent=2)
    print(f"Final roster saved to {roster_file}")

if __name__ == "__main__":
    poll_until_stop(interval_sec=60)
