import requests

cid = [
    "00000000402b5328",
    "fe72edc2-3a6f-4280-90e8-e2beb64ce7e1"
    ]

def secretStr(string):
    a = string[0:2]
    b = string[len(string)-2:len(string)]
    return a + "*" * (len(string)-4) + b

def refreshtoken(re_token):
    Reurl = "https://login.live.com/oauth20_token.srf"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _cid = cid.copy()
    for i in _cid:
        try:
            data = {
                "client_id": i,
                "grant_type": "refresh_token",
                "refresh_token": re_token,
                "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
                "scope": "XboxLive.signin offline_access",
            }
            res = requests.post(Reurl, data=data, headers=headers)
            acc_ = res.json()["access_token"]
            ref_ = res.json()["refresh_token"]
            print("[Gtoken: def: refreshtoken] Used the Client ID:", secretStr(i), end="\t\t\t\t\t\t\t\t\t\t\t\r")
            return acc_, ref_
        except Exception:
            print(f"[Gtoken: def: refreshtoken] The Client ID: {secretStr(i)}, is not the truth.", end="\t\t\t\t\t\t\t\t\t\t\t\r")
            cid.remove(i)
            continue


# microsoft OAuth2 Token
def get_microsoft_token(code):
    url = "https://login.live.com/oauth20_token.srf"
    headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "client_id": cid[0],
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "https://login.live.com/oauth20_desktop.srf"
    }
    response = requests.post(url, data=data, headers=headers)
    print("[Gtoken: def: get_microsoft_token] Used the Client ID:", secretStr(cid[0]), end="\t\t\t\t\t\t\t\t\t\t\t\r")
    return response.json()["access_token"], response.json()["refresh_token"]


# Xbox Live
def get_xbox_token(ms_token):
    url = "https://user.auth.xboxlive.com/user/authenticate"
    headers = {"Content-Type": "application/json"}
    data = {
        "Properties": {"AuthMethod": "RPS", "SiteName": "user.auth.xboxlive.com", "RpsTicket": f"d={ms_token}"},
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["Token"], response.json()["DisplayClaims"]["xui"][0]["uhs"]

# XSTS Token
def get_xsts_token(xbox_token):
    url = "https://xsts.auth.xboxlive.com/xsts/authorize"
    headers = {"Content-Type": "application/json"}
    data = {
        "Properties": {"SandboxId": "RETAIL", "UserTokens": [xbox_token]},
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["Token"]

# Minecraft
def get_minecraft_token(xsts_token, userhash):
    url = "https://api.minecraftservices.com/authentication/login_with_xbox"
    headers = {"Content-Type": "application/json"}
    data = {"identityToken": f"XBL3.0 x={userhash};{xsts_token}"}
    response = requests.post(url, headers=headers, json=data)
    return response.json()["access_token"]

# 检查游戏所有权
'''
def check_ownership(mc_token):
    url = "https://api.minecraftservices.com/entitlements/mcstore"
    headers = {"Authorization": f"Bearer {mc_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

# 获取玩家 Profile
def get_player_profile(mc_token):
    url = "https://api.minecraftservices.com/minecraft/profile"
    headers = {"Authorization": f"Bearer {mc_token}"}
    response = requests.get(url, headers=headers)
    return response.json()
'''
def start(ms_token):

    # Xbox Live
    xbox_token, userhash = get_xbox_token(ms_token)
    xsts_token = get_xsts_token(xbox_token)

    # Minecraft token
    mc_token = get_minecraft_token(xsts_token, userhash)

    return mc_token