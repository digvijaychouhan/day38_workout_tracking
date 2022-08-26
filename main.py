import os
import requests
from datetime import datetime

GENDER = os.environ["GENDER"]
WEIGHT_KG = os.environ["WEIGHT_KG"]
HEIGHT_CM = os.environ["HEIGHT_CM"]
AGE = os.environ["AGE"]

APP_ID = os.environ["APP_ID"]
APP_KEY = os.environ["APP_KEY"]
S_TOKEN = os.environ["S_TOKEN"]

user_input = input("Tell me which exercises you did: ")

sheet_ep = os.environ["SHEET_EP"]
sheet_header = {"Authorization": f"Bearer {S_TOKEN}"}
exercise_ep = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY
}

exercise_params = {
    "query": user_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=exercise_ep, json=exercise_params, headers=exercise_headers)
result = response.json()

today = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_params = {
        "workout": {
            "date": today,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
          }
    }
    sheet_response = requests.post(url=sheet_ep, json=sheet_params, headers=sheet_header)

    print(sheet_response.text)
