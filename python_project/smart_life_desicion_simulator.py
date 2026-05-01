# ===============================
# Smart Life Decision Simulator
# ===============================

import random

# -------------------------------
# Utility Functions
# -------------------------------

def get_int_input(prompt):
    """Safely get integer input"""
    while True:
        try:
            return int(input(prompt))
        except:
            print("❌ Invalid input. Enter a number.")

def print_line():
    print("=" * 50)

# -------------------------------
# User Profile
# -------------------------------

def create_profile():
    print_line()
    print("👤 Create Your Profile")
    name = input("Enter your name: ")
    age = get_int_input("Enter your age: ")
    return {"name": name, "age": age, "history": []}

# -------------------------------
# Career Simulation
# -------------------------------

def career_simulation(user):
    print_line()
    print("💼 Career Simulator")

    careers = {
        "1": ("Software Engineer", ["coding", "logic", "projects"]),
        "2": ("Doctor", ["biology", "practice", "patience"]),
        "3": ("Businessman", ["risk", "communication", "strategy"])
    }

    for key, value in careers.items():
        print(f"{key}. {value[0]}")

    choice = input("Choose career: ")

    if choice not in careers:
        print("❌ Invalid choice")
        return

    career_name, skills = careers[choice]

    study_hours = get_int_input("Study hours per day (1-10): ")
    consistency = get_int_input("Consistency level (1-10): ")

    score = (study_hours * 2) + (consistency * 3)

    if score >= 40:
        result = "🔥 High Success"
    elif score >= 25:
        result = "⚠️ Moderate Success"
    else:
        result = "❌ Low Success"
