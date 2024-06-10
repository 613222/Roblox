import requests
import time
import os

def getcursordata(cursor):
    itemresponse = requests.get(f"https://itemconfiguration.roblox.com/v1/creations/get-assets?assetType=Image&isArchived=false&limit=100&cursor={cursor}", headers={"Accept": "application/json", "Content-Type": "application/json"}, cookies={".ROBLOSECURITY": cookie})
    if itemresponse.status_code == 200:
        return itemresponse.json()
    print(f"Something went wrong (Retrying). Status Code: {itemresponse.status_code}")
    time.sleep(2.5)
    return getcursordata(cursor)

def saveToFile(content, userId):
    if not os.path.exists("output"):
        os.makedirs("output")
    with open(os.path.join("output", f"selfuser_accepted_{userId}.txt"), 'a') as file:
        file.write(content + '\n')

def getassetdetails(csrf, assetIds):
    response = requests.post("https://itemconfiguration.roblox.com/v1/creations/get-asset-details", headers={"Accept": "application/json", "Content-Type": "application/json", "X-Csrf-Token": csrf}, cookies={".ROBLOSECURITY": cookie}, json={"assetIds": assetIds})
    if response.status_code == 200:
        return response.json()
    print(f"Something went wrong (Retrying). Status Code: {response.status_code}")
    time.sleep(0.75)
    return getassetdetails(csrf, assetIds)

def separate(array):
    num_chunks = (len(array) + 99) // 100
    chunks = []
    for i in range(num_chunks):
        start_index = i * 100
        end_index = min((i + 1) * 100, len(array))
        chunks.append(array[start_index:end_index])
    return chunks

if __name__ == "__main__":
    cookie = input("Cookie: ")
    userId = requests.get("https://www.roblox.com/MobileApi/UserInfo", cookies={".ROBLOSECURITY": cookie}).json()["UserID"]
    accepted = []
    assets = []
    cursor = ""
    page = 0
    while True:
        page += 1
        data = getcursordata(cursor)
        for asset in data["data"]:
            assets.append(asset["assetId"])
        if data["nextPageCursor"]:
            cursor = data["nextPageCursor"]
        else:
            break
        print(f"Finished page {page}")
        time.sleep(0.75)
    if not os.path.exists("output"):
        os.makedirs("output")
    if not os.path.exists(os.path.join("output", f"selfuser_accepted_{userId}.txt")):
        with open(os.path.join("output", f"selfuser_accepted_{userId}.txt"), 'w') as file:
            file.write("Accepted decals from yourself is listed below.\n")
    csrfrecheck = 0
    chunks = separate(assets)
    csrf = requests.post("https://friends.roblox.com/v1/users/6089365305/request-friendship", cookies={'.ROBLOSECURITY': cookie}).headers.get("x-csrf-token")
    for assets in chunks:
        if csrfrecheck == 4:
            csrf = requests.post("https://friends.roblox.com/v1/users/6089365305/request-friendship", cookies={".ROBLOSECURITY": cookie}).headers.get("x-csrf-token")
            csrfrecheck = 0
        response = getassetdetails(csrf, assets)
        for asset in response:
            if asset["status"] == "ReviewApproved":
                print(f"Accepted Image ID: {asset["assetId"]}")
                accepted.append(asset["assetId"])
        csrfrecheck += 1
        time.sleep(0.75)

    print(accepted)
    print(f"Pages of assets (100 assets per page - last page): {page}")
    print(f"Accepted Ids: {len(accepted)}")