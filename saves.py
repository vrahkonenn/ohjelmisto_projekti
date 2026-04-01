import json

def save(data, coins):
    data["currency"] = coins
    with open("data.json", "w") as file:
        json.dump(data, file, indent=2)

def open_data():
    with open("data.json", "r") as f:
            data = json.load(f)
    return data

def get_data():
    try:
        data = open_data()
    except FileNotFoundError:
        data = {"highscore": 0, "currency": 0, "jumpboost": 0, "jetpack": 0, "shoes": 0, "umbrella": 0}
        with open("data.json", "w") as f:
            json.dump(data, f, indent=2)
            f.close()
        data = open_data()
    
    return data