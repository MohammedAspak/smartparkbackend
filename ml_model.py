import random

def predict_availability():
    return {
        "availability": random.choice(["High", "Medium", "Low"])
    }

def predict_peak_hours():
    return {
        "peak_hours": ["10 AM - 12 PM", "6 PM - 8 PM"]
    }

def suggest_best_time():
    return {
        "best_time": "2 PM - 4 PM"
    }
