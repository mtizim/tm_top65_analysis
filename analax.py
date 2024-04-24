# %%
from requests_ratelimiter import LimiterSession
from time import time
from collections import defaultdict
from requests import Session
import base64
from requests.auth import HTTPBasicAuth

# %%
nbody = {"audience": "NadeoLiveServices"}
nsession = LimiterSession(per_second=10)
nsession.headers["User-Agent"] = (
    "Quick cotd qualifiers top128 scrape by @mtizim on discord mtizim1@gmail.com"
)
basic = HTTPBasicAuth("mtizim1@gmail.com", "notmypasswordlmao")
nadeo_ticket = nsession.post(
    "https://public-ubiservices.ubi.com/v3/profiles/sessions",
    # json=nbody,
    headers={
        "Content-Type": "application/json",
        "Ubi-AppId": "86263886-327a-4328-ac69-527f0d20a237",
    },
    auth=basic,
)

ticket = nadeo_ticket.json()["ticket"]

authres = nsession.post(
    "https://prod.trackmania.core.nadeo.online/v2/authentication/token/ubiservices",
    json=nbody,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"ubi_v1 t={ticket}",
    },
)
token = authres.json()["accessToken"]
nsession.headers["Authorization"] = "nadeo_v1 t={token}"

# %%

# %%
session = LimiterSession(per_minute=38)
session.headers["User-Agent"] = (
    "Quick cotd qualifiers top128 scrape by @mtizim on discord"
)
# %%
cotds = []
i = 0
while True:
    print(i)
    res = session.get(f"https://trackmania.io/api/cotd/{i}")
    i += 1
    if len(res.json()["competitions"]) == 0:
        break
    cotds.extend(res.json()["competitions"])
# %%
cotds_copy = [el for el in cotds]
# %%
cotds = [
    cotd for cotd in cotds if cotd["name"][-2:] != "#2" and cotd["name"][-2:] != "#3"
]


# %%
counter = defaultdict(int)
for i, cotd in enumerate(cotds):
    print(f"{i + 1} / {len(cotds)}, {i + 1 / len(cotds)}%")
    if cotd["players"] < 65:
        continue
    cotdid = cotd["id"]
    challengeid = nsession.get(
        f"https://meet.trackmania.nadeo.club/api/competitions/{cotdid}/rounds",
        headers={"Authorization": f"nadeo_v1 t={token}"},
    ).json()[0]["qualifierChallengeId"]

    leadb_resp = session.get(
        f"https://meet.trackmania.nadeo.club/api/challenges/{challengeid}/leaderboard?length={66}",
        headers={"Authorization": f"nadeo_v1 t={token}"},
    )
    try:
        loser = next(pl for pl in leadb_resp.json()["results"] if pl["rank"] == 65)[
            "player"
        ]
        counter[loser] += 1
    except:
        pass

# %%
import json

s = sorted(counter.items(), key=lambda x: x[1])
with open("out.json", "w") as f:
    f.write(json.dumps(s))
# %%
