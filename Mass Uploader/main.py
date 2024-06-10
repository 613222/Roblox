from modules import Drawing
from faker import Faker
import threading
import requests
import random
import time
import json
import os

# Credits to NPD hehe :3
# Free source py -BitsProxy

# Please read these terms and do not use this service for any of these purposes
# We are not responsible for any legal actions taken against YOU and YOU only
# ORIGINAL TERMS: https://cdn.bitsproxy.dev/au-terms.txt

# Just don't upload shit that the police would get involved, INCLUDING THREATENING SCHOOLS OR PEOPLE.

configuration = json.load(open("config.json"))
accountsettings = configuration["accountsettings"]
assetconfiguration = configuration["assetconfiguration"]
userId = 0
imageIds = []
APIKEYS = []
active = True

def getproxies():
    proxylist = []
    try:
        with open("proxies.txt", "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                proxy = line.strip()
                proxies = {'http': proxy, 'https': proxy}
                proxylist.append(proxies)
    except FileNotFoundError:
        try:
            proxy_response = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=85000&country=all&ssl=all&anonymity=elite')
            proxy_response.raise_for_status()
            lines = proxy_response.text.splitlines()
            for line in lines:
                proxy_url = line.strip()
                proxies = {'http': proxy_url, 'https': proxy_url}
                proxylist.append(proxies)
            return proxylist
        except Exception as e:
            raise ConnectionError(e)
    if not proxylist:
        raise AssertionError("Proxies not appended!")
    return proxylist

def getcsrftoken(cookie):
    response = requests.post("https://friends.roblox.com/v1/users/6089365305/request-friendship", cookies={'.ROBLOSECURITY': cookie})
    return response.headers.get("x-csrf-token")

def fake():
    name = f"{Faker().first_name()} ({random.randint(100, 999)})"
    return name

def pywait():
    time.sleep(random.uniform(0.15, 0.85))

def getUserInfo(cookie):
    response = requests.get("https://www.roblox.com/MobileAPI/UserInfo", cookies={".ROBLOSECURITY": cookie}).json()
    return response

def getapikeys(cookie, csrf):
    response = requests.post("https://apis.roblox.com/cloud-authentication/v1/apiKeys", headers={"Accept": "application/json", "Content-Type": "application/json", "X-Csrf-Token": csrf}, cookies={".ROBLOSECURITY": cookie}, json={
        "cursor": "",
        "limit": 100,
        "reverse": False
    })
    if response.status_code == 200:
        return response.json()["cloudAuthInfo"]
    return {}

def deleteapikey(cookie, csrf, id):
    response = requests.delete(f"https://apis.roblox.com/cloud-authentication/v1/apiKey/{id}", headers={"Accept": "application/json", "Content-Type": "application/json", "X-Csrf-Token": csrf}, cookies={".ROBLOSECURITY": cookie})
    return response

def createapikey(cookie, csrf):
    response = requests.post("https://apis.roblox.com/cloud-authentication/v1/apiKey", headers={"Accept": "application/json", "Content-Type": "application/json", "X-Csrf-Token": csrf}, cookies={".ROBLOSECURITY": cookie}, json={
        "cloudAuthUserConfiguredProperties": {
            "name": fake(),
            "description": "",
            "isEnabled": True,
            "allowedCidrs": ["0.0.0.0/0"],
            "scopes": [
                {
                    "scopeType": "asset",
                    "targetParts": ["U"],
                    "operations": ["read", "write"]
                }
            ]
        }
    })
    if response.status_code == 200:
        data = response.json()
        APIKEYS.append(data["apikeySecret"])
        return {
            "secret": data["apikeySecret"],
            "id": data["cloudAuthInfo"]["id"],
            "userId": data["cloudAuthInfo"]["ownerId"],
            "created": data["cloudAuthInfo"]["createdTime"],
            "updated": data["cloudAuthInfo"]["updatedTime"],
            "enabled": data["cloudAuthInfo"]["cloudAuthUserConfiguredProperties"]["isEnabled"],
            "name": data["cloudAuthInfo"]["cloudAuthUserConfiguredProperties"]["name"],
            "description": data["cloudAuthInfo"]["cloudAuthUserConfiguredProperties"]["description"],
        }
    return None

def getAssetDetails(cookie, csrf, assetIds):
    response = requests.post("https://itemconfiguration.roblox.com/v1/creations/get-asset-details", headers={"Accept": "application/json", "Content-Type": "application/json", "X-Csrf-Token": csrf}, cookies={".ROBLOSECURITY": cookie}, json={
        "assetIds": assetIds
    })
    return response

def saveToFile(content, userId):
    if not os.path.exists("output"):
        os.makedirs("output")
    with open(os.path.join("output", f"ids_{userId}.txt"), 'a') as file:
        file.write(content + '\n')

def saveImagesToFile(cookie):
    try:
        CSRF = getcsrftoken(cookie)
    except Exception as e:
        print("Failed to save images to file (X-CSRF-TOKEN missing). (Script Error)")
    response = requests.get("https://itemconfiguration.roblox.com/v1/creations/get-assets?assetType=Image&isArchived=false&limit=100", headers={"Accept": "application/json", "Content-Type": "application/json", "X-Csrf-Token": CSRF}, cookies={".ROBLOSECURITY": cookie})
    if response.status_code == 200:
        data = response.json()
        for asset in data["data"]:
            assetId = asset["assetId"]
            if assetId not in imageIds:
                saveToFile(f"https://www.roblox.com/library/{assetId}", userId)
                imageIds.append(assetId)
        return True
    return False

def setWebTheme(cookie, csrf, theme):
    response = requests.patch("https://accountsettings.roblox.com/v1/themes/user", headers={"X-Csrf-Token": csrf}, cookies={".ROBLOSECURITY": cookie}, json={"themeType": theme})
    return response

def reactivateAccount(cookie, csrf):
    data = requests.get("https://usermoderation.roblox.com/v1/not-approved", headers={"Accept": "application/json", "Content-Type": "application/json", "X-Csrf-Token": csrf}, cookies={".ROBLOSECURITY": cookie}).json()
    if data["punishmentTypeDescription"] == "Warn":
        response = requests.post("https://usermoderation.roblox.com/v1/not-approved/reactivate", headers={"Accept": "application/json", "Content-Type": "application/json", "X-Csrf-Token": csrf}, cookies={".ROBLOSECURITY": cookie})
        if response.ok or response.status_code == 429:
            return True, {}
    return False, data["messageToUser"]

def createAsset(apiKeys, userId, assetType, displayName, description, imageContent, proxies, cookie):
    try:
        fileContent = {'fileContent': ("dd33f515-1912-4cb6-bae4-10608f3a33f7.dll", imageContent, "image/png")}
        payload = {
            "request": '{"assetType": "' + assetType + '", "displayName": "' + displayName + '", "description": "' + description + '", "creationContext": {"creator": {"userId": "' + str(userId) + '"}}}'
        }
        response = requests.post("https://apis.roblox.com/assets/v1/assets", headers={"x-api-key": random.choice(apiKeys)}, data=payload, files=fileContent, proxies=random.choice(proxies))
        if response.status_code == 200:
            print("Successfully uploaded asset!")
        else:
            if response.status_code == 401 or response.status_code == 403:
                reactivationStatus, data = reactivateAccount(cookie, csrf)
                if reactivationStatus == True:
                    pywait()
                else:
                    active = False
                    return print(f"Account is moderated for \"[{data}\"")
            pywait()
            return createAsset(apiKeys, userId, assetType, displayName, description, imageContent, proxies, cookie)
    except Exception as e:
        pywait()
        return createAsset(apiKeys, userId, assetType, displayName, description, imageContent, proxies, cookie)

if __name__ == "__main__":
    if input("Mass Uploading (y/n): ").lower().startswith("y"):
        global csrf
        active = True
        uploads = input("Upload threads: ")

        try:
            uploads = int(uploads)
        except ValueError:
            uploads = 300
            print("set default to 300 uploading threads.")

        assetType = input("Asset Type (Image / TShirt / Decal): ")

        assetType = assetType.lower()
        if assetType.startswith("d") or assetType == "3":
            assetType = "Decal"
        elif assetType.startswith("t") or assetType == "2":
            assetType = "TShirt"
        else:
            assetType = "Image"

        filePath = input("FilePath ( HTTP(s) / DISK C:/... C:\\... ): ")
        fileType = input("FileType ( JPG / PNG ): ")
        try:
            if filePath.startswith("http"):
                imageContent = Drawing.GetImageContentFromURL(filePath)
            else:
                imageContent = Drawing.ReadFileByFilePath(filePath)

            if fileType.lower().startswith("j"):
                fileType = "JPG"
            else:
                fileType = "PNG"

            ROBLOSEC = input(".ROBLOSECURITY: ")

            try:
                userId = getUserInfo(ROBLOSEC)["UserID"]
                if not os.path.exists("output"):
                    os.makedirs("output")
                if not os.path.exists(os.path.join("output", f"ids_{userId}.txt")):
                    with open(os.path.join("output", f"ids_{userId}.txt"), 'w') as file:
                        file.write("assets here are saved from the upload, not all assets are.\n")
                images = []
                imgthreads = []
                delthreads = []
                keythreads = []
                uplthreads = []
                def manipulateImage():
                    if fileType == "JPG":
                        newImageContent = Drawing.ManipulateJPGImage(imageContent)
                    else:
                        newImageContent = Drawing.ManipulatePNGImage(imageContent)
                    images.append(newImageContent)
                    print(f"Manipulated image {i} / {uploads}")
                
                for i in range(uploads):
                    thread = threading.Thread(target=manipulateImage)
                    thread.start()
                    imgthreads.append(thread)
                
                for thread in imgthreads:
                    thread.join()

                csrf = getcsrftoken(ROBLOSEC)
                if accountsettings["autochangetheme"] == True:
                    setWebTheme(ROBLOSEC, csrf, "Dark")
                    print("Web theme set to Dark mode.")
                apikeys = getapikeys(ROBLOSEC, csrf)
                if apikeys:
                    for key in apikeys:
                        thread = threading.Thread(target=deleteapikey, args=(ROBLOSEC, csrf, key["id"]))
                        thread.start()
                        delthreads.append(thread)

                    for thread in delthreads:
                        thread.join()
                    print("Deleted all API Keys.")
                        
                csrf = getcsrftoken(ROBLOSEC)
                for i in range(random.randint(20, 40)):
                    thread = threading.Thread(target=createapikey, args=(ROBLOSEC, csrf))
                    thread.start()
                    keythreads.append(thread)

                for thread in keythreads:
                    thread.join()

                def check_decals():
                    while active:
                        time.sleep(3)
                        if saveImagesToFile(ROBLOSEC) == False:
                            break
                        if not active:
                            break
                decalChecking = threading.Thread(target=check_decals)
                decalChecking.start()
                proxies = getproxies()
                if proxies:
                    for imagecontent in images:
                        upload = threading.Thread(target=createAsset, args=(APIKEYS, userId, assetType, assetconfiguration["displayName"], assetconfiguration["description"], imagecontent, proxies, ROBLOSEC))
                        upload.start()
                        imgthreads.append(upload)

                    for thread in imgthreads:
                        thread.join()

                    print("Finished upload threading assets.")
                else:
                    print("Invalid proxies. (API Error)")
            
            except Exception as e:
                print(f"Failed to upload, {e}")
        
        except Exception as e:
            print("Invalid file retry again.")