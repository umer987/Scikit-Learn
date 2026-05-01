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
