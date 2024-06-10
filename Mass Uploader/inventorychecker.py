import threading
import requests
import random
import time
import os

def getcursordata(cursor, userid):
    itemresponse = requests.get(f"https://inventory.roblox.com/v2/users/{userid}/inventory/13?limit=100&sortOrder=Desc&cursor={cursor}", headers={"Accept": "application/json", "Content-Type": "application/json"}, cookies={".ROBLOSECURITY": cookie})
    if itemresponse.status_code == 200:
        return itemresponse.json()
    print(f"Something went wrong (Retrying). Status Code: {itemresponse.status_code}")
    time.sleep(2.5)
    return getcursordata(cursor)

def saveToFile(content, userId):
    if not os.path.exists("output"):
        os.makedirs("output")
    with open(os.path.join("output", f"user_accepted_{userId}.txt"), 'a') as file:
        file.write(content + '\n')

def getthumbnail(assetIds):
    response = requests.get(f"https://thumbnails.roblox.com/v1/assets?assetIds={','.join(map(str, assetIds))}&size=150x150&format=Webp")
    if response.status_code == 200:
        return response.json()["data"]
    print(f"Something went wrong (Retrying). Status Code: {response.status_code}")
    time.sleep(1)
    return getthumbnail(assetIds)

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
    userId = input("UserId: ")
    accepted = []
    images = []
    cursor = ""
    page = 0
    def convertDecalIdToImageId(decalId):
        time.sleep(random.uniform(0, 8))
        try:
            id = requests.get(f"https://apis.613222.dev/v1/roblox/assets/image/{decalId}").json()["imageId"]
        except Exception as e:
            print("Retrying...")
            time.sleep(random.uniform(2, 15))
            return convertDecalIdToImageId(decalId)
        print(f"Converted ID {decalId} to {id}.")
        images.append(id)
    threads = []
    while True:
        page += 1
        data = getcursordata(cursor, userId)
        for asset in data["data"]:
            assetId = asset["assetId"]
            thread = threading.Thread(target=convertDecalIdToImageId, args=(assetId,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        if data["nextPageCursor"]:
            cursor = data["nextPageCursor"]
        else:
            break
        print(f"Finished page {page}")
        time.sleep(1)
    if not os.path.exists("output"):
        os.makedirs("output")
    if not os.path.exists(os.path.join("output", f"user_accepted_{userId}.txt")):
        with open(os.path.join("output", f"user_accepted_{userId}.txt"), 'w') as file:
            file.write("Accepted decals from a user listed below.\n")

    chunks = separate(images)

    for imageIds in chunks:
        response = getthumbnail(imageIds)
        for thumb in response:
            if thumb["state"] == "Completed":
                print(f"Accepted Image ID: {thumb["targetId"]}")
                accepted.append(thumb["targetId"])
                saveToFile(f"https://www.roblox.com/library/{thumb["targetId"]}", userId)
        time.sleep(0.75)

    print(accepted)
    print(f"Pages of assets (100 assets per page - last page): {page}")
    print(f"Accepted Ids: {len(accepted)}")