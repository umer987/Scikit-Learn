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

    print_line()
    print(f"{user['name']}, Career: {career_name}")
    print(f"Required Skills: {skills}")
    print(f"Result: {result}")

    user["history"].append(("Career", career_name, result))

# -------------------------------
# Budget Planner
# -------------------------------

def budget_planner(user):
    print_line()
    print("💰 Budget Planner")

    income = get_int_input("Enter your monthly income: ")
    expenses = []

    while True:
        exp = get_int_input("Enter expense (0 to stop): ")
        if exp == 0:
            break
        expenses.append(exp)

    total_expense = sum(expenses)
    savings = income - total_expense

    print_line()
    print(f"Total Expense: {total_expense}")
    print(f"Savings: {savings}")

    if savings > 0:
        print("✅ Good financial management")
    else:
        print("⚠️ You are overspending!")

    user["history"].append(("Budget", savings))

# -------------------------------
# Study Strategy
# -------------------------------

def study_strategy(user):
    print_line()
    print("📚 Study Strategy")

    subjects = ["Math", "Programming", "Physics", "English"]
    weak_subjects = []

    for sub in subjects:
        level = get_int_input(f"Rate your level in {sub} (1-10): ")
        if level < 5:
            weak_subjects.append(sub)

    if weak_subjects:
        print("⚠️ Focus more on:", weak_subjects)
    else:
        print("🔥 You're doing great!")

    user["history"].append(("Study", weak_subjects))

# -------------------------------
# Daily Routine Optimizer
# -------------------------------

def routine_optimizer(user):
    print_line()
    print("⏰ Routine Optimizer")

    sleep = get_int_input("Hours of sleep: ")
    study = get_int_input("Hours of study: ")
    exercise = get_int_input("Exercise hours: ")

    score = sleep + study + exercise

    if score >= 15:
        print("🔥 Excellent routine")
    elif score >= 10:
        print("⚠️ متوسط routine")
    else:
        print("❌ Poor routine")

    user["history"].append(("Routine", score))

# -------------------------------
# Recursive Future Projection
# -------------------------------

def future_growth(years, growth):
    """Recursive function"""
    if years == 0:
        return 0
    return growth + future_growth(years - 1, growth)

def future_simulation(user):
    print_line()
    print("🔮 Future Prediction")

    years = get_int_input("Enter number of years: ")
    growth = get_int_input("Enter yearly growth score: ")

    result = future_growth(years, growth)

    print(f"📈 Total Growth after {years} years: {result}")

    user["history"].append(("Future", result))

# -------------------------------
# View History
# -------------------------------

def view_history(user):
    print_line()
    print("📜 Your Decision History")

    for item in user["history"]:
        print(item)

# -------------------------------
# Main Menu
# -------------------------------

def main():
    print("🌟 Welcome to Smart Life Decision Simulator 🌟")

    user = create_profile()

    while True:
        print_line()
        print("1. Career Simulator")
        print("2. Budget Planner")
        print("3. Study Strategy")
        print("4. Routine Optimizer")
        print("5. Future Prediction")
        print("6. View History")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            career_simulation(user)
        elif choice == "2":
            budget_planner(user)
        elif choice == "3":
            study_strategy(user)
        elif choice == "4":
            routine_optimizer(user)
        elif choice == "5":
            future_simulation(user)
        elif choice == "6":
            view_history(user)
        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

# -------------------------------
# Run Program
# -------------------------------

if __name__ == "__main__":
    main()