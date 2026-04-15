import json
import os

# -----------------------------
# JSON file setup
# -----------------------------
DATA_FILE = "grades.json"

if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = {}
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

def check_weight(total_contribution, total_weight, remaining_weight, subject_name):
    if remaining_weight == 0:
        gwa = (total_contribution / total_weight) * 100 if total_weight > 0 else 0
        print("All weights have been assigned.")
        print(f"\nYour GWA percentage for {subject_name} is: {gwa:.2f}%")
        print("Status:", "PASSED ✅" if gwa >= 60 else "FAILED ❌")
        return gwa
    return None

# -----------------------------
# Assessment Calculations
# -----------------------------
def calculate_assessment(assessment_name, max_count, remaining_weight):
    print(f"\n{assessment_name} assessments")
    count = get_valid_number(
        f"Enter how many {assessment_name.lower()} assessments you took: ", 0, max_count
    )
    if count == 0:
        return 0, 0
    weight = get_valid_number(
    f"Enter weight (remaining {remaining_weight}%): ",
    0,
    remaining_weight
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

def calculate_optional_exam(exam_name, remaining_weight):
    take_exam = get_valid_number(
        f"Did you take any {exam_name}? (1 = yes, 2 = no): ", 1, 2
    )
    if take_exam == 2:
        return 0, 0
    count = get_valid_number(f"How many {exam_name} did you take?: ", 1, 10)
    weight = get_valid_number(
    f"Enter weight (remaining {remaining_weight}%): ",
    0,
    remaining_weight
)
    total = 0
    for i in range(count):
        grade = get_valid_grade(f"Enter score for {exam_name} #{i+1}: ")
        total += grade
    average = total / count
    contribution = average * (weight / 100)
    return contribution, weight

def calculate_exam(exam_name, remaining_weight):
    take_exam = get_valid_number(
        f"Did you take a {exam_name} exam? (1 = yes, 2 = no): ", 1, 2
    )
    if take_exam == 2:
        return 0, 0
    weight = get_valid_number(
    f"Enter weight (remaining {remaining_weight}%): ",
    0,
    remaining_weight
)
    score = get_valid_grade(f"Enter your score in the {exam_name} exam: ")
    contribution = score * (weight / 100)
    return contribution, weight

# -----------------------------
# Subject Calculation
# -----------------------------
def calculate_subject_gwa(subject_name):
    print(f"\n--- Calculating {subject_name} ---")
    total_contribution = 0
    total_weight = 0
    remaining_weight = 100

    fa_contrib, fa_weight = calculate_assessment("Formative", 10, remaining_weight)
    remaining_weight -= fa_weight
    
    total_contribution += fa_contrib
    total_weight += fa_weight

    result = check_weight(total_contribution, total_weight, remaining_weight, subject_name)
    if result is not None:
        return result

    aa_contrib, aa_weight = calculate_assessment("Alternative", 7, remaining_weight)
    remaining_weight -= aa_weight
    
    total_contribution += aa_contrib
    total_weight += aa_weight

    result = check_weight(total_contribution, total_weight, remaining_weight, subject_name)
    if result is not None:
        return result

    lt_contrib, lt_weight = calculate_optional_exam("Long Test", remaining_weight)
    remaining_weight -= lt_weight
    
    total_contribution += lt_contrib
    total_weight += lt_weight

    result = check_weight(total_contribution, total_weight, remaining_weight, subject_name)
    if result is not None:
        return result

    pr_contrib, pr_weight = calculate_optional_exam("Practical Exam", remaining_weight)
    remaining_weight -= pr_weight
    
    total_contribution += pr_contrib
    total_weight += pr_weight

    result = check_weight(total_contribution, total_weight, remaining_weight, subject_name)
    if result is not None:
        return result

    midterm_contrib, midterm_weight = calculate_optional_exam("Midterm", remaining_weight)
    remaining_weight -= midterm_weight
    
    total_contribution += midterm_contrib
    total_weight += midterm_weight

    result = check_weight(total_contribution, total_weight, remaining_weight, subject_name)
    if result is not None:
        return result

    final_contrib, final_weight = calculate_exam("Final", remaining_weight)
    remaining_weight -= final_weight
    
    total_contribution += final_contrib
    total_weight += final_weight

    result = check_weight(total_contribution, total_weight, remaining_weight, subject_name)
    if result is not None:
        return result

    bonus = get_valid_grade("Enter bonus points for this subject (0 if none): ")
    bonus = min(bonus, 5)
    total_contribution += bonus

    if total_weight > 100:
        print("\nWARNING: Total weights exceed 100%! Adjusting final GWA accordingly.")

    if total_weight > 0:
        gwa = (total_contribution / total_weight) * 100
    else:
        gwa = 0

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
# GWA Errors
# -----------------------------
def cap_gwa(overall_gwa):
    if overall_gwa > 100:
        print("\nERROR: Your GWA exceeded 100%.")
        print("Capping final GWA to 100%.\n")
        return 100
    return overall_gwa

# -----------------------------
# Desired Grade Calculator
# -----------------------------
def calculate_required_score(current_grade, desired_grade, weight_remaining):
    if weight_remaining <= 0:
        print("No remaining weight to compute.")
        return
    print("NOTE: Enter your CURRENT WEIGHTED grade.")
    needed = (desired_grade - current_grade) / (weight_remaining / 100)
    if needed > 100:
        print("Unfortunately, it's not possible to reach your desired grade.")
    elif needed < 0:
        print("You have already surpassed your desired grade!")
    else:
        print(f"You need {needed:.2f}% on the remaining assessments to reach your desired grade.")

# -----------------------------
# 1/3 2/3 feature
# -----------------------------
def get_previous_quarter_grade(user_id, quarter):
    order = ["Q1" , "Q2" , "Q3" , "Q4"]
    if user_id not in data:
        return None
    if quarter not in order:
        return None
    idx = order.index(quarter)
    if idx == 0:
        return None
    prev_quarter = order[idx - 1]

    if "quarters" in data[user_id] and prev_quarter in data[user_id]["quarters"]:
        return data[user_id]["quarters"][prev_quarter]["overall_gwa"]
    return None

def apply_carry(previous_gwa, current_gwa):
    final_gwa = (previous_gwa * (1/3)) + (current_gwa * (2/3))
    if final_gwa > 100:
        final_gwa = 100
    return final_gwa

# -----------------------------
# Save Grades
# -----------------------------
def save_grade_json(user_id, user_name, grade_level, section, quarter, subjects, overall_gwa):
    if user_id in data and data[user_id]["name"] != user_name:
        print("WARNING: Name does not match existing user!")

    if user_id not in data:
        data[user_id] = {"name": user_name, "grade_level": grade_level, "section": section, "quarters": {}}

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
        print(f"Grade Level: {user_data.get('grade_level','N/A')}, Section: {user_data.get('section','N/A')}")
        for quarter, details in user_data.get("quarters", {}).items():
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
        print(f"Grade Level: {user_data.get('grade_level','N/A')}, Section: {user_data.get('section','N/A')}")
        for quarter, details in user_data.get("quarters", {}).items():
            print(f" Quarter: {quarter}")
            for subj in details["subjects"]:
                print(f"  - {subj['name']}: {subj['gwa']:.2f}%")
            print(f" Overall GWA: {details['overall_gwa']:.2f}%")
    else:
        print("User not found.")

# -----------------------------
# Show GWA
# -----------------------------
def convert_to_GWA(gwa):
    if 96.00 <= gwa and gwa <= 100.00:
        return "1.00"
    elif 90.00 <= gwa and gwa <= 95.00:
        return "1.25"
    elif 84.00 <= gwa and gwa <= 89.00:
        return "1.50"
    elif 78.00 <= gwa and gwa <= 83.00:
        return "1.75"
    elif 72.00 <= gwa and gwa <= 77.00:
        return "2.00"
    elif 66.00 <= gwa and gwa <= 71.00:
        return "2.25"
    elif 60.00 <= gwa and gwa <= 65.00:
        return "2.50"
    elif 55.00 <= gwa and gwa <= 59.00:
        return "2.75"
    else:
        return "3.00 or below"
    
# -----------------------------
# Main Program Loop
# -----------------------------
print("Reminder: Please enter grades in percentage form (0-100).")

while True:
    print("\n===== GWA CALCULATOR =====")
    user_name = input("Enter your full name: ")
    user_id = input("Enter your ID: ")

    grade_level = input("Enter your grade level: ")
    section = input("Enter your section: ")

    if user_id in data:
        print(f"Welcome back, {user_name}!")
        search_choice = get_valid_number(
            "Do you want to view your previous grades? (1 = yes, 2 = no): ",
            1, 2
        )
        if search_choice == 1:
            search_user()

    num_sub = get_valid_number("Enter number of subjects: ", 1, 15)
    subjects = []

    for i in range(num_sub):
        print(f"\nSubject #{i+1}")
        subject_name = input("Enter subject name: ")
        gwa = calculate_subject_gwa(subject_name)
        subjects.append({"name": subject_name, "gwa": gwa})

    current_gwa = sum(subj['gwa'] for subj in subjects) / len(subjects)
    current_gwa = cap_gwa(current_gwa)

    quarter = input("Enter quarter (e.g., Q1, Q2, Q3, Q4): ").upper()
    previous_gwa = get_previous_quarter_grade(user_id, quarter)

    if previous_gwa is not None:
        overall_gwa = apply_carry(previous_gwa, current_gwa)
        print(f"\nFinal GWA with 1/3-2/3 carry-over: {overall_gwa:.2f}%")
    else:
        overall_gwa = current_gwa
        print(f"\nYour overall GWA for this quarter: {overall_gwa:.2f}%")

    save_grade_json(user_id, user_name, grade_level, section, quarter, subjects, overall_gwa)

    direct_conversion = get_valid_number("Would you like to convert the percentage into GWA? (1 = yes, 2 = no): ", 1, 2)
    if direct_conversion == 1:
        gwa_equivalent = convert_to_GWA(overall_gwa)
        print(f"GWA Equivalent: {gwa_equivalent}")

    show_table = get_valid_number("Show GWA table? (1 = yes, 2 = no): ", 1, 2)
    if show_table == 1:
        show_gwa_table()

    check_desired = get_valid_number("Do you want to calculate required score for desired grade? (1 = yes, 2 = no): ", 1, 2)
    if check_desired == 1:
        current_grade = float(input("Enter your current grade: "))
        desired_grade = float(input("Enter your desired final grade: "))
        weight_remaining = float(input("Enter remaining weight (%): "))
        calculate_required_score(current_grade, desired_grade, weight_remaining)

    show_saved = get_valid_number("Do you want to view all saved grades? (1 = yes, 2 = no): ", 1, 2)
    if show_saved == 1:
        show_saved_grades_json()

    loop_choice = get_valid_number("Do you want to calculate again? (1 = yes, 2 = no): ", 1, 2)
    if loop_choice == 2:
        print("\nThank you for using the GWA calculator! (｡･∀･)ﾉﾞ")
        break
