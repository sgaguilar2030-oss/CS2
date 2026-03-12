import json
import os

# -----------------------------
# JSON file setup
# -----------------------------
DATA_FILE = "grades.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {}

# -----------------------------
# Helper Functions
# -----------------------------
def get_valid_number(prompt, min_val, max_val):
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"ERROR: Value must be between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_valid_grade(prompt):
    while True:
        try:
            grade = float(input(prompt))
            if 0 <= grade <= 100:
                return grade
            else:
                print("ERROR: Grade must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# -----------------------------
# Assessment Calculations
# -----------------------------
def calculate_assessment(assessment_name, max_count):
    print(f"\n{assessment_name} assessments")

    count = get_valid_number(
        f"Enter how many {assessment_name.lower()} assessments you took: ", 0, max_count
    )

    if count == 0:
        return 0, 0

    weight = get_valid_number(
        f"Enter total weight of {assessment_name.lower()} assessments to your final GWA (%): ", 0, 100
    )

    total = 0
    for i in range(count):
        grade = get_valid_grade(
            f"Enter grade for {assessment_name.lower()} assessment #{i + 1}: "
        )
        total += grade

    average = total / count
    contribution = average * (weight / 100)

    return contribution, weight

def calculate_exam(exam_name):
    take_exam = get_valid_number(
        f"Did you take a {exam_name} exam? (1 = yes, 2 = no): ", 1, 2
    )

    if take_exam == 1:
        weight = get_valid_number(
            f"Enter weight of {exam_name} exam (%): ", 0, 100
        )

        score = get_valid_grade(
            f"Enter your score in the {exam_name} exam: "
        )

        contribution = score * (weight / 100)

        return contribution, weight

    return 0, 0

# -----------------------------
# Subject Calculation
# -----------------------------
def calculate_subject_gwa(subject_name):
    print(f"\n--- Calculating {subject_name} ---")

    total_contribution = 0
    total_weight = 0

    fa_contrib, fa_weight = calculate_assessment("Formative", 10)
    total_contribution += fa_contrib
    total_weight += fa_weight

    aa_contrib, aa_weight = calculate_assessment("Alternative", 7)
    total_contribution += aa_contrib
    total_weight += aa_weight

    midterm_contrib, midterm_weight = calculate_exam("Midterm")
    total_contribution += midterm_contrib
    total_weight += midterm_weight

    final_contrib, final_weight = calculate_exam("Final")
    total_contribution += final_contrib
    total_weight += final_weight

    bonus = float(input("Enter bonus points for this subject (0 if none): "))
    total_contribution += bonus

    if total_weight > 100:
        print("\nWARNING: Total weights exceed 100%! Adjusting final GWA accordingly.")

    gwa = total_contribution

    print(f"\nYour GWA percentage for {subject_name} is: {gwa:.2f}%")
    print("Status:", "PASSED ✅" if gwa >= 60 else "FAILED ❌")

    return gwa

# -----------------------------
# GWA Table
# -----------------------------
def show_gwa_table():
    GWA = [
        ["96-100", "1.00"],
        ["90-95", "1.25"],
        ["84-89", "1.50"],
        ["78-83", "1.75"],
        ["72-77", "2.00"],
        ["66-71", "2.25"],
        ["60-65", "2.50"],
        ["55-59", "2.75"],
        ["Below 55", "3.00 or below"],
    ]

    print("\n===== PISAY GWA TABLE =====")
    print("{:<15} {:<15}".format("Percentage", "GWA"))
    print("-" * 30)

    for row in GWA:
        print("{:<15} {:<15}".format(row[0], row[1]))

    print("-" * 30)

# -----------------------------
# Desired Grade Calculator
# -----------------------------
def calculate_required_score(current_grade, desired_grade, weight_remaining):

    if weight_remaining <= 0:
        print("No remaining weight to compute.")
        return

    needed = (desired_grade - current_grade) / (weight_remaining / 100)

    if needed > 100:
        print("Unfortunately, it's not possible to reach your desired grade.")
    elif needed < 0:
        print("You have already surpassed your desired grade!")
    else:
        print(f"You need {needed:.2f}% on the remaining assessments to reach your desired grade.")

# -----------------------------
# Save Grades
# -----------------------------
def save_grade_json(user_id, user_name, quarter, subjects, overall_gwa):

    if user_id not in data:
        data[user_id] = {"name": user_name, "quarters": {}}

    data[user_id]["quarters"][quarter] = {
        "subjects": subjects,
        "overall_gwa": overall_gwa
    }

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\nGrades saved for {user_name} ({user_id}) in {quarter}.")

# -----------------------------
# Show Saved Grades
# -----------------------------
def show_saved_grades_json():

    if not data:
        print("No grades saved yet.")
        return

    print("\n===== SAVED GRADES =====")

    for user_id, user_data in data.items():
        print(f"\nUser: {user_data['name']} (ID: {user_id})")

        for quarter, details in user_data["quarters"].items():

            print(f" Quarter: {quarter}")

            for subj in details["subjects"]:
                print(f"  - {subj['name']}: {subj['gwa']:.2f}%")

            print(f" Overall GWA: {details['overall_gwa']:.2f}%")

# -----------------------------
# Search User
# -----------------------------
def search_user():

    user_id = input("Enter user ID to search: ")

    if user_id in data:

        user_data = data[user_id]

        print(f"Found user: {user_data['name']} (ID: {user_id})")

        for quarter, details in user_data["quarters"].items():

            print(f" Quarter: {quarter}")

            for subj in details["subjects"]:
                print(f"  - {subj['name']}: {subj['gwa']:.2f}%")

            print(f" Overall GWA: {details['overall_gwa']:.2f}%")

    else:
        print("User not found.")

# -----------------------------
# Main Program Loop
# -----------------------------
print("Reminder: Please enter grades in percentage form (0-100).")

while True:

    print("\n===== GWA CALCULATOR =====")

    user_name = input("Enter your full name: ")
    user_id = input("Enter your ID: ")

    if user_id in data:
        print(f"Welcome back, {user_name}!")

        search_choice = get_valid_number(
            "Do you want to view your previous grades? (1 = yes, 2 = no): ",
            1,
            2
        )

        if search_choice == 1:
            search_user()

    num_sub = get_valid_number("Enter number of subjects: ", 1, 15)

    subjects = []

    for i in range(num_sub):

        print(f"\nSubject #{i+1}")

        subject_name = input("Enter subject name: ")

        gwa = calculate_subject_gwa(subject_name)

        subjects.append({
            "name": subject_name,
            "gwa": gwa
        })

    overall_gwa = sum(subj['gwa'] for subj in subjects) / len(subjects)

    print(f"\nYour overall GWA for this quarter: {overall_gwa:.2f}%")

    quarter = input("Enter quarter (e.g., Q1, Q2, Q3, Q4): ")

    save_grade_json(
        user_id,
        user_name,
        quarter,
        subjects,
        overall_gwa
    )

    show_table = get_valid_number(
        "Show GWA table? (1 = yes, 2 = no): ",
        1,
        2
    )

    if show_table == 1:
        show_gwa_table()

    check_desired = get_valid_number(
        "Do you want to calculate required score for desired grade? (1 = yes, 2 = no): ",
        1,
        2
    )

    if check_desired == 1:

        current_grade = float(input("Enter your current grade: "))
        desired_grade = float(input("Enter your desired final grade: "))
        weight_remaining = float(input("Enter remaining weight (%): "))

        calculate_required_score(
            current_grade,
            desired_grade,
            weight_remaining
        )

    show_saved = get_valid_number(
        "Do you want to view all saved grades? (1 = yes, 2 = no): ",
        1,
        2
    )

    if show_saved == 1:
        show_saved_grades_json()

    loop_choice = get_valid_number(
        "Do you want to calculate again? (1 = yes, 2 = no): ",
        1,
        2
    )

    if loop_choice == 2:
        print("\nThank you for using the GWA calculator! (｡･∀･)ﾉﾞ")
        break
