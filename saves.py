import json

def save(data, total_coins, coins):
    data["currency"] = total_coins + coins
    with open("data.json", "w") as file:
        json.dump(data, file, indent=2)

def get_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return data
