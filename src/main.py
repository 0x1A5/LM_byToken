import gettoken.Gtoken as Gtoken
import json
import Launch.launch as launch


def savetokens(tokens_data, token_file="./tokens.json"):
    '''
    tokens_w = open(token_file, "w")
    json.dump(tokens_data, tokens_w)
    tokens_w.close()
    '''
    with open(token_file, 'w', encoding='utf-8') as f:
        json.dump(tokens_data, f, indent=4, ensure_ascii=False)

def _gettoken(options):
    from urllib.parse import urlparse, parse_qs
    print("请访问以下 URL 获取 code：")
    print("https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?client_id=00000000402b5328&response_type=code&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=XboxLive.Signin%20offline_access&prompt=select_account")
    url = input("请输入跳转后的网址: ")
    p_url = urlparse(url)
    qp = parse_qs(p_url.query)
    code = qp["code"][0]
    A, B = Gtoken.get_microsoft_token(code)
    A = Gtoken.start(A)
    if options['gettoken_thenEchotoken']:
        print("Access Token: " + A)
        print("Refresh Token: " + B)
    return A, B

def launchMinecraft(dir, versions, acc_token, username, uuid):
    launcher = launch.Launch(dir, versions, acc_token, username, uuid)
    launcher.launchMinecraft()

def checkDir(t):
    if t["Dirs"]["versionDir"] == '' or t["Dirs"]["assetsDir"] == '' or t["Dirs"]["javaDir"] == '':
        return False
    return True

def refreshToken(t, userIndex, options):
    acc_token, ref_token = Gtoken.refreshtoken(t["user"][userIndex]["ref_token"])
    acc_token = Gtoken.start(acc_token)
    t["user"][userIndex]["acc_token"] = acc_token
    t["user"][userIndex]["ref_token"] = ref_token
    if options['gettoken_thenEchotoken']:
        print("Access Token: " + t["user"][userIndex]["acc_token"])
        print("Refresh Token: " + t["user"][userIndex]["ref_token"])
    if options['gettoken_thenSaveToken']:
        savetokens(t)
    return t

def checkTokens(t, userIndex, options):
    if t["user"][userIndex]["ref_token"] != "":
        if t["user"][userIndex]["acc_token"] != '':
            if options['always_refreshToken']:
                t = refreshToken(t, userIndex, options)
            return t
        else:
            t = refreshToken(t, options)
            return t
    else:
        if t["user"][userIndex]["acc_token"] != '':
            return t
        else:
            acc_token, ref_token = _gettoken(options)
            t["user"][userIndex]["acc_token"] = acc_token
            t["user"][userIndex]["ref_token"] = ref_token

            if options['gettoken_thenSaveToken']:
                savetokens(t)
            return t

def getTokensJson():
    tokens = open("./tokens.json", "r")
    tokens_data = json.load(tokens)
    tokens.close()
    return tokens_data

def getOptionsJson():
    options = open("./options.json", "r")
    options_data = json.load(options)
    options.close()
    return options_data

def checkUser(t):
    if not (t["user"][0]["name"] and t["user"][0]["uuid"]):
        return False
    return True

def chooseVersion(versions):
    print()
    if len(versions) == 1:
        return versions[0]
    else:
        for i in range(len(versions)):
            print(f"Type [{i}] to open {versions[i]}")
        choice = int(input("Please choose the version index: "))
        return versions[choice]
    
def chooseUser(users):
    if len(users) == 1:
        return 0
    else:
        for i in range(len(users)):
            print(f"Type [{i}] to open {users[i]['name']}")
        choice = int(input("Please choose the user index: "))
        return choice


if __name__ == "__main__":
    
    tokens_data = getTokensJson()
    options_data = getOptionsJson()

    if not checkUser(tokens_data):
        print("No Username and Useruuid found.")
        exit(2)

    userIndex = chooseUser(tokens_data["user"])
    userInfo = tokens_data["user"][userIndex]

    if not checkDir(tokens_data):
        print("Game Directory not set. Please set gameDir in tokens.json")
        exit(2)

    if tokens_data["gameVersions"] == []:
        print("No game versions found. Please set gameVersions in tokens.json")
        exit(2)

    tokens_data = checkTokens(tokens_data, userIndex, options_data)

    #opthions

    

    if options_data['gettoken_thenLaunch']:
        
        launchMinecraft(tokens_data["Dirs"],
                        chooseVersion(tokens_data["gameVersions"]),
                        userInfo["acc_token"],
                        userInfo["name"],
                        userInfo["uuid"])
        
    if options_data['launch_thenCleanbat']:
        bat_clean = open(".\Launch\launch.bat", "w")
        bat_clean.write("")
        bat_clean.close()
            
    if options_data['launch_thenRefreshToken']:
        tokens_data["acc_token"], tokens_data["ref_token"] = _gettoken(options_data)
        savetokens(tokens_data)


        

        