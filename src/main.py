import gettoken.Gtoken as Gtoken
import json
import Launch.launch as launch



def getFile_TokensJson():
    tokens = open("./tokens.json", "r")
    tokens_data = json.load(tokens)
    tokens.close()
    return tokens_data
def getFile_OptionsJson():
    options = open("./options.json", "r")
    options_data = json.load(options)
    options.close()
    return options_data

def savetokens(tokens_data, token_file="./tokens.json"):
    '''
    tokens_w = open(token_file, "w")
    json.dump(tokens_data, tokens_w)
    tokens_w.close()
    '''
    with open(token_file, 'w', encoding='utf-8') as f:
        json.dump(tokens_data, f, indent=4, ensure_ascii=False)

# if the user have no token(any), login. 
def addToken(options):
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



def refreshToken(tokensJson, userIndex, options):
    acc_token, ref_token = Gtoken.refreshtoken(tokensJson["user"][userIndex]["ref_token"])
    acc_token = Gtoken.start(acc_token)
    tokensJson["user"][userIndex]["acc_token"] = acc_token
    tokensJson["user"][userIndex]["ref_token"] = ref_token
    if options['gettoken_thenEchotoken']:
        print("Access Token: " + tokensJson["user"][userIndex]["acc_token"])
        print("Refresh Token: " + tokensJson["user"][userIndex]["ref_token"])
    if options['gettoken_thenSaveToken']:
        savetokens(tokensJson)
    return tokensJson

def checkTokens(tokensJson, userIndex, options):
    # Check if the user has a refresh token
    if tokensJson["user"][userIndex]["ref_token"] != "":
        # If the user has a refresh token
        if tokensJson["user"][userIndex]["acc_token"] != '':
            if options['always_refreshToken']:
                tokensJson = refreshToken(tokensJson, userIndex, options)
            return tokensJson
        else:
            tokensJson = refreshToken(tokensJson, userIndex, options)
            return tokensJson
    else:
        if tokensJson["user"][userIndex]["acc_token"] != '':
            return tokensJson
        else:
            acc_token, ref_token = addToken(options)
            tokensJson["user"][userIndex]["acc_token"] = acc_token
            tokensJson["user"][userIndex]["ref_token"] = ref_token

            if options['gettoken_thenSaveToken']:
                savetokens(tokensJson)
            return tokensJson



def checkUser(tokensJson):
    if not (tokensJson["user"][0]["name"] and tokensJson["user"][0]["uuid"]):
        print("No Username and Useruuid found.")
        exit(2)
def checkDir(tokensJson):
    if tokensJson["Dirs"]["versionDir"] == '' or tokensJson["Dirs"]["assetsDir"] == '' or tokensJson["Dirs"]["javaDir"] == '':
        print("Game Directory not set. Please set gameDir in tokens.json")
        exit(2)
def checkVersion(tokensJson):
    if tokensJson["gameVersions"] == []:
        print("No game versions found. Please set gameVersions in tokens.json")
        exit(2)

def chooseVersion(versions):
    if len(versions) == 1:
        return versions[0]
    else:
        print()
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
    
def afterLaunch(tokenJson, options):
    if options['launch_thenCleanbat']:
            bat_clean = open(".\Launch\launch.bat", "w")
            bat_clean.write("")
            bat_clean.close()
    if options['launch_thenRefreshToken']:
        tokenJson["acc_token"], tokenJson["ref_token"] = addToken(options)
        savetokens(tokenJson)


if __name__ == "__main__":
    
    # tokens.json
    tokens_data = getFile_TokensJson()
    #options.json
    options_data = getFile_OptionsJson()

    # checks
    checkUser(tokens_data)
    checkDir(tokens_data)
    checkVersion(tokens_data)
        
    #choose user
    userIndex = chooseUser(tokens_data["user"])
    userInfo = tokens_data["user"][userIndex]

    tokens_data = checkTokens(tokens_data, userIndex, options_data)

    #opthions
    if options_data['gettoken_thenLaunch']:
        launchMinecraft(tokens_data["Dirs"],
                        chooseVersion(tokens_data["gameVersions"]),
                        userInfo["acc_token"],
                        userInfo["name"],
                        userInfo["uuid"])
        afterLaunch(tokens_data, options_data)
    
    


        

        