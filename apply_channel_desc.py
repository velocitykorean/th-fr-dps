import os, json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

token_path = r"D:\E agy cli\E youtube bots\the-freudian-depths\token.json"
with open(token_path, "r", encoding="utf-8") as f:
    token_data = json.load(f)

creds = Credentials(
    None,
    refresh_token=token_data["refresh_token"],
    token_uri=token_data.get("token_uri", "https://oauth2.googleapis.com/token"),
    client_id=token_data.get("client_id"),
    client_secret=token_data.get("client_secret"),
    scopes=["https://www.googleapis.com/auth/youtube"]
)
creds.refresh(Request())
yt = build("youtube", "v3", credentials=creds)

desc = """Welcome to The Freudian Depths - a sanctuary of psychoanalytic inquiry, intellectual courage, and deep psychological exploration.

Here, we descend beneath the polite surfaces of conscious thought into the uncharted labyrinth of the human mind:
* The Architecture of the Unconscious: Id, Ego, and Superego
* The Interpretation of Dreams and nocturnal symbolism
* Defense Mechanisms: Why we deceive ourselves to survive reality
* Civilization and Its Discontents: The tragic bargain of human order
* Eros and Thanatos: The perpetual conflict of Life and Death drives
* The Shadow of Love, Attachment, and Childhood Desires
* The Art of Sublimation: Transmuting primitive instincts into culture and genius

"The mind is like an iceberg, it floats with one-seventh of its bulk above water."
- Sigmund Freud

Subscribe to join our psychoanalytic circle as we illuminate the hidden motives that govern human destiny.

Official Handle: @thefreudiandepths"""

try:
    res = yt.channels().update(
        part="brandingSettings",
        body={
            "id": "UCFaKh33OLae6KP2I8bLmpxQ",
            "brandingSettings": {
                "channel": {
                    "description": desc
                }
            }
        }
    ).execute()
    print("[SUCCESS] brandingSettings description updated!")
except Exception as e:
    print("[brandingSettings error]:", e)

try:
    res2 = yt.channels().update(
        part="localizations",
        body={
            "id": "UCFaKh33OLae6KP2I8bLmpxQ",
            "localizations": {
                "en": {
                    "title": "The Freudian Depths",
                    "description": desc
                }
            }
        }
    ).execute()
    print("[SUCCESS] localizations description updated!")
except Exception as e:
    print("[localizations error]:", e)
