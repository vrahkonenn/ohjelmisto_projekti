import json
import os

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
        data = {
                "highscore": 0,
                "currency": 0,
                "jumpboost": [
                    0,
                    0
                ],
                "jumpboost_str": [
                    0,
                    0
                ],
                "jetpack": [
                    0,
                    0
                ],
                "jetpack_dur": [
                    0,
                    0
                ],
                "shoes": [
                    0,
                    0
                ],
                "extra_jumps": [
                    0,
                    0
                ],
                "umbrella": [
                    0,
                    0
                ],
                "umbrella_dur": [
                    0,
                    0
                ]
             }
        with open("data.json", "w") as f:
            json.dump(data, f, indent=2)
            f.close()
        data = open_data()
    
    return data

def reset_json():
    if os.path.exists("data.json"):
        os.remove("data.json")     
    data = get_data()
    return data