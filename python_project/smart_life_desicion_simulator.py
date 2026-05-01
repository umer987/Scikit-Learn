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
